from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
    def post(self, request, id):
        print(request.data)
        course = Course.objects.get(pk=id)
        notes = Notes(user=request.user, course=course, body=request.data['isi'], photo=request.data['file'])
        notes.save()
        
        return HttpResponse("Notes berhasil dibuat")

class DetailNotesView(APIView):
    def get(self, request, id1, id2):
        notes = Notes.objects.get(pk=id2)
        if request.user.is_authenticated:
            vote_status = Vote.objects.filter(user=request.user, notes=notes).values_list('status', flat=True).first() or 0
        
        else:
            vote_status = 0
        notes.vote_status = vote_status

        children = Notes.objects.filter(parent=notes)
        for child in children:
            if request.user.is_authenticated:
                vote_status = Vote.objects.filter(user=request.user, notes=child).values_list('status', flat=True).first() or 0
            else:
                vote_status = 0
            child.vote_status = vote_status
        context = {
            'notes': notes,
            'children': children,
            'id_course': notes.course.id,
        }
        return render(request, 'notes_detail.html', context)
    
    def post(self, request, id1, id2):
        print(request.data)
        course = Course.objects.get(pk=id1)
        parent = Notes.objects.get(pk=id2)
        notes = Notes(user=request.user, course=course, body=request.data['isi'], photo=request.data['file'], parent=parent)
        notes.save()
        
        return HttpResponse("Notes berhasil dibuat")
    

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
