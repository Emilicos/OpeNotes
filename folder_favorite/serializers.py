from rest_framework import serializers

from .models import FolderFavorite, FolderNotes


class FolderFavoriteSerializer(serializers.ModelSerializer):
    notes_count = serializers.SerializerMethodField()

    def get_notes_count(self, folder_favorite):
        return folder_favorite.folder_notes.count()

    class Meta:
        model = FolderFavorite
        fields = '__all__'


class FolderNotesCountSerializer(serializers.Serializer):
    object = FolderFavoriteSerializer()
    notes_count = serializers.IntegerField()
