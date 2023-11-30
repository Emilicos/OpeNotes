from django.http import Http404, HttpResponse
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
    def get(self, request, id):
        course = Course.objects.get(pk=id)
        course_notes = Notes.objects.filter(course=course)
        notes_list = course_notes.order_by('-created_on')
        form = NotesForm()
        context = {
            'notes_list': notes_list,
            'form': form,
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
    
