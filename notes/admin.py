from django.contrib import admin

from notes.models import Note

# Register your models here.
class NotesModelAdmin(admin.ModelAdmin):
    list_display=("get_user", "course")
    
    def get_user(self, obj):
        return obj.user.get_full_name()
    get_user.short_description = "Name"
    
admin.site.register(Note, NotesModelAdmin)