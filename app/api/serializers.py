from rest_framework import serializers

from courses.models import Course
from users.models import Teacher
from contactus.models import Message


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = 'id', 'first_name', 'last_name'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = 'id', 'title', 'description', 'teachers'
    teachers = TeacherSerializer(many=True, read_only=True)


class TeacherAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'email',
                  'phone_number', 'bio', 'avatar', 'password')

    def create(self, validated_data):
        teacher = super().create(validated_data)
        teacher.set_password(validated_data['password'])
        teacher.save()
        return teacher


class CourseAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = 'id', 'title', 'description', 'teachers'
    teachers = TeacherSerializer(many=True)


class MessageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('first_name', 'last_name', 'email', 'phone_number',
                            'title', 'text', 'received_time')
