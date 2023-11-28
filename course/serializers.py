from rest_framework import serializers

from course.models import Course

class PrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')
        
class CourseSerializer(serializers.ModelSerializer):
    prerequisites = PrerequisiteSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = '__all__'