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

class NotesListView(APIView):
    def get(self, request):
        notes_list = Notes.objects.all().order_by('-created_on')
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
    
