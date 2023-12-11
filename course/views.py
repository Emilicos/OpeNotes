from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from course.forms import CourseForm

from course.models import Course
from course.serializers import CourseSerializer
from notes.forms import NotesForm
from notes.models import Notes, Vote

# Create your views here.
class CourseListView(APIView):
    permission_classes = []
    def get(self, request):
        rest = request.GET.get('rest', None)
        form = CourseForm()
        courses = Course.objects.prefetch_related("prerequisites").all()
        serializer = CourseSerializer(courses, many=True)
        
        if(rest):
            return Response({
                "courses": serializer.data,
                "prerequisites": CourseSerializer(Course.objects.prefetch_related("prerequisites").all(), many=True).data,
                "form": form.as_p()
            }, status=status.HTTP_200_OK)
        return render(request, "list.html", {"courses": serializer.data, "form": form})
    
    def post(self, request):
        self.permission_classes = [IsAdminUser]
        
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            if(request.user.is_anonymous or not request.user.is_staff):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            course = serializer.save()
            prerequisites = request.data.getlist('prerequisites')
            for prerequisite in prerequisites:
                try:
                    pre_course = Course.objects.get(pk=prerequisite)
                    course.prerequisites.add(pre_course)
                except Course.DoesNotExist:
                    raise Http404()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CourseDetailView(APIView):
    permission_classes = []
    
    def get_object(self, id):
        try:
            return Course.objects.get(pk=id)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        course = self.get_object(id)
        serializer = CourseSerializer(course)
        
        course_notes = Notes.objects.filter(course=course, parent = None)
        notes_list = course_notes.order_by('-created_on')
        
        for notes in notes_list:
            if request.user.is_authenticated:
                vote_status = Vote.objects.filter(user=request.user, notes=notes).values_list('status', flat=True).first() or 0
            
            else:
                vote_status = 0
            notes.vote_status = vote_status
            
        form = NotesForm()
        context = {
            'notes_list': notes_list,
            'form': form,
            'id_course': id,
            "course": serializer.data
        }
        
        return render(request, "detail.html", context)
    
    def put(self, request, id, format=None):
        self.permission_classes = [IsAdminUser]
        course = self.get_object(id)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            if(request.user.is_anonymous or not request.user.is_staff):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            serializer.save()
            prerequisites_data = []
            prerequisites = request.data.getlist('prerequisites')
            for prerequisite in prerequisites:
                try:
                    pre_course = Course.objects.get(pk=prerequisite)
                    prerequisites_data.append(pre_course)
                    course.prerequisites.set(prerequisites_data)
                except Course.DoesNotExist:
                    raise Http404()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        if(request.user.is_anonymous or not request.user.is_staff):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        self.permission_classes = [IsAdminUser]
        course = self.get_object(id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)