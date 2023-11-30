from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course
from course.serializers import CourseSerializer
from notes.forms import NotesForm
from notes.models import Notes, Vote

# Create your views here.

class NotesListView(APIView):
    def get(self, request):
        notes_list = Notes.objects.all().order_by('-created_on')

        for notes in notes_list:
            vote_status = Vote.objects.filter(user=request.user, notes=notes).values_list('status', flat=True).first() or 0
            notes.vote_status = vote_status
        form = NotesForm()
        context = {
            'notes_list': notes_list,
            'form': form,
        }
        
        return render(request, 'notes_list.html', context)
        # return render(request, 'coba.html', context)
        
    def post(self, request):
        notes_list = Notes.objects.all()
        form = NotesForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_notes = form.save(commit=False)
            new_notes.user = request.user
            new_course = Course.objects.create(name="AAA",code="AAA")
            new_notes.course = new_course
            new_notes.save()

        context = {
            'notes_list': notes_list,
            'form': form,
        }
        
        return render(request, 'notes_list.html', context)
            

class DetailNotesView(APIView):
    def get(self, request, id):
        notes = Notes.objects.get(pk=id)
        context = {
            'notes': notes,
        }
        return render(request, 'notes_detail.html', context)

class VoteView(APIView):
    def post(self, request, id):
        try:
            user = request.user
            note = Notes.objects.get(id=id)
            status_value = request.data.get('status', None)
            if status_value is not None and status_value in [-1, 1]:
                new_vote = Vote(user=user, notes=note, status=status_value)
                new_vote.save()
                return Response({'message': 'Vote saved successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid vote status'}, status=status.HTTP_400_BAD_REQUEST)
        except Notes.DoesNotExist:
            raise Http404
        
    def put(self, request, id):
        try:
            user = request.user

            existing_vote = Vote.objects.get(user=user, notes__id=id)
            existing_vote.status = -existing_vote.status

            existing_vote.save()

            return Response({'message': 'Vote saved successfully'}, status=status.HTTP_200_OK)
        except Notes.DoesNotExist:
            return Response({'message': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
        except Vote.DoesNotExist:
            return Response({'message': 'Vote not found'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, id):
        print("MASUK GAK")
        user = request.user

        try:
            vote = Vote.objects.get(user=user, notes__id=id)
            vote.delete()
            return Response({'message': 'Vote deleted successfully'}, status=status.HTTP_200_OK)

        except Notes.DoesNotExist:
            return Response({'message': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
        except Vote.DoesNotExist:
            return Response({'message': 'Vote not found'}, status=status.HTTP_404_NOT_FOUND)