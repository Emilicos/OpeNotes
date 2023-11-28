from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course
from course.serializers import CourseSerializer
from notes.forms import NotesForm
from notes.models import Notes

# Create your views here.
class CourseListView(APIView):
    permission_classes = []
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return render(request, "list.html", {"courses": serializer.data})
    
    def post(self, request):
        self.permission_classes = [IsAdminUser]
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        return render(request, "detail.html", {"course": serializer.data})
    
    def put(self, request, id, format=None):
        self.permission_classes = [IsAdminUser]
        course = self.get_object(id)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        self.permission_classes = [IsAdminUser]
        course = self.get_object(id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NotesListView(APIView):
    def get(self, request):
        notes_list = Notes.objects.all()
        form = NotesForm()
        context = {
            'notes_list': notes_list,
            'form': form,
        }
        
        # return render(request, 'notes_list.html', context)
        return render(request, 'coba.html', context)
        
    def post(self, request):
        notes_list = Notes.objects.all()
        form = NotesForm(request.POST)
        
        if form.is_valid():
            new_notes = form.save(commit=False)
            new_notes.user = request.user
            new_course = Course.objects.create(name="asu",code="asu")
            new_notes.course = new_course
            new_notes.save()

        context = {
            'notes_list': notes_list,
            'form': form,
        }
        
        return render(request, 'notes_list.html', context)
            

class DetailNotesView(APIView):
    def get(self, request, pk):
        notes = Notes.objects.get(pk=pk)
