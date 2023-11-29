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