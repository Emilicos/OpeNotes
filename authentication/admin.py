from django.contrib import admin

from authentication.models import Profile

# Register your models here.

class ProfileModelAdmin(admin.ModelAdmin):
    list_display=("get_user_name", "npm", "faculty", "study_program", "educational_program")
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()
    get_user_name.short_description = "Name"

admin.site.register(Profile, ProfileModelAdmin)