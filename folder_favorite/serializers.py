from rest_framework import serializers

from .models import FolderFavorite, FolderNotes


class FolderFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderFavorite
        fields = '__all__'


class FolderNotesCountSerializer(serializers.Serializer):
    object = FolderFavoriteSerializer()
    notes_count = serializers.IntegerField()
