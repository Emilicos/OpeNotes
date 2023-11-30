from django.contrib import admin

from notes.models import Notes

# Register your models here.
class NotesModelAdmin(admin.ModelAdmin):
    list_display=("get_user", "course", "body")

    def get_user(self, obj):
        return obj.user.get_full_name()
    get_user.short_description = "Name"
    
admin.site.register(Notes, NotesModelAdmin)