from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse

from .forms import FolderFavoriteForm
from .models import FolderFavorite, FolderNotes
from .serializers import FolderFavoriteSerializer, FolderNotesCountSerializer

# Create your views here.
class FolderFavoriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rest = request.GET.get('rest', None)
        if rest:
            user = request.user
            folders = FolderFavorite.objects.filter(user=user)
            serializer = FolderFavoriteSerializer(folders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        form = FolderFavoriteForm()
        return render(request, "folder_list.html", {"form": form})
    
    def post(self, request):
        serializer = FolderFavoriteSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FolderFavoriteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return FolderFavorite.objects.get(pk=id)
        except FolderFavorite.DoesNotExist:
            raise Http404

    def get(self, request, id):
        folder_favorite = self.get_object(id)
        notes_list = [folder_notes.notes 
                      for folder_notes in FolderNotes.objects.filter(folder=folder_favorite)]
        notes_list = notes_list[::-1]
        return render(request, "folder_detail.html", {"folder": folder_favorite, "notes_list": notes_list})

    def put(self, request, id):
        folder_favorite = self.get_object(id)
        serializer = FolderFavoriteSerializer(folder_favorite, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        folder_favorite = self.get_object(id)
        folder_favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)