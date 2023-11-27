from django.contrib import admin

from course.models import Course

# Register your models here.
class CourseModelAdmin(admin.ModelAdmin):
    list_display=("name", "code", "credit", "semester")
    list_filter=["semester"]
    search_fields=("name", "code")
    
admin.site.register(Course, CourseModelAdmin)