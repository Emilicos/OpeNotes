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
    
    def validate_credit(self, value):
        if value < 0 or value > 24:
            raise serializers.ValidationError("SKS tidak boleh kurang dari 0 atau lebih dari 24")
        return value
    
    def validate_semester(self, value):
        if value < 1 or value > 8:
            raise serializers.ValidationError("Semester tidak boleh kurang dari 1 atau lebih dari 8")
        return value