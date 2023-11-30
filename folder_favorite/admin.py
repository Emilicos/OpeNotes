from django.contrib import admin

from .models import FolderFavorite, FolderNotes

# Register your models here.
class FolderFavoriteModelAdmin(admin.ModelAdmin):
    list_display=("user", "nama")
    list_filter=["user"]
    search_fields=("user", "nama")
    
class FolderNotesModelAdmin(admin.ModelAdmin):
    list_display=("folder", "notes")
    list_filter=["folder", "notes"]
    search_fields=("folder", "notes")
    
admin.site.register(FolderFavorite, FolderFavoriteModelAdmin)
admin.site.register(FolderNotes, FolderNotesModelAdmin)