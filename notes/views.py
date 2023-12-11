from django.http import Http404, HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from notes.models import Notes

# Create your views here.
class NotesDetailView(APIView):
    permission_classes = []
    
    def get_object(self, id):
        try:
            return Notes.objects.get(pk=id)
        except Notes.DoesNotExist:
            raise Http404

    def get(self, request, id):
        notes = self.get_object(id)
        context = {
            'notes' : notes
        }
        return render(request, "notes_detail.html", context)
    
    def delete(self, request, id):
        notes = self.get_object(id)
        if notes.user != request.user:
            return HttpResponseForbidden("Anda tidak boleh menghapus Notes ini")

        notes.delete()

        return HttpResponse("BANGGGGG INI DMN")

from course.models import Course
from course.serializers import CourseSerializer
from notes.forms import NotesForm
from notes.models import Notes, Vote

# Create your views here.

class NotesListView(APIView):
    def get(self, request, id):
        course = Course.objects.get(pk=id)
        course_notes = Notes.objects.filter(course=course)
        notes_list = course_notes.order_by('-created_on')
        for notes in notes_list:
            vote_status = Vote.objects.filter(user=request.user, notes=notes).values_list('status', flat=True).first() or 0
            notes.vote_status = vote_status
            
        form = NotesForm()
        context = {
            'notes_list': notes_list,
            'form': form,
            'id_course': id
        }
        
        return render(request, 'notes_list.html', context)
        # return render(request, 'coba.html', context)
        
    def post(self, request):
        print(request.data)
        course = Course.objects.get(pk=1)
        notes = Notes(user=request.user, course=course, body=request.data['isi'], photo=request.data['file'])
        notes.save()
        # notes_list = Notes.objects.all()
        # form = NotesForm(request.POST, request.FILES)
        
        # if form.is_valid():
        #     new_notes = form.save(commit=False)
        #     new_notes.user = request.user
        #     new_course = Course.objects.create(name="AAA",code="AAA")
        #     new_notes.course = new_course
        #     new_notes.save()

        # context = {
        #     'notes_list': notes_list,
        #     'form': form,
        # }
        
        return HttpResponse("notes berhasil dibuat oh yeah")
            

class DetailNotesView(APIView):
    def get(self, request, id1, id2):
        notes = Notes.objects.get(pk=id2)
        context = {
            'notes': notes,
        }
        return render(request, 'notes_detail.html', context)
    

class VoteView(APIView):
    def post(self, request, id1, id2):
        try:
            user = request.user
            note = Notes.objects.get(id=id2)
            status_value = request.data.get('status', None)
            if status_value is not None and status_value in [-1, 1]:
                new_vote = Vote(user=user, notes=note, status=status_value)
                new_vote.save()
                return Response({'message': 'Vote saved successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid vote status'}, status=status.HTTP_400_BAD_REQUEST)
        except Notes.DoesNotExist:
            raise Http404
        
    def put(self, request, id1, id2):
        try:
            user = request.user

            existing_vote = Vote.objects.get(user=user, notes__id=id2)
            existing_vote.status = -existing_vote.status

            existing_vote.save()

            return Response({'message': 'Vote saved successfully'}, status=status.HTTP_200_OK)
        except Notes.DoesNotExist:
            return Response({'message': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
        except Vote.DoesNotExist:
            return Response({'message': 'Vote not found'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, id1, id2):
        print("MASUK GAK")
        user = request.user

        try:
            vote = Vote.objects.get(user=user, notes__id=id2)
            vote.delete()
            return Response({'message': 'Vote deleted successfully'}, status=status.HTTP_200_OK)

        except Notes.DoesNotExist:
            return Response({'message': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
        except Vote.DoesNotExist:
            return Response({'message': 'Vote not found'}, status=status.HTTP_404_NOT_FOUND)
