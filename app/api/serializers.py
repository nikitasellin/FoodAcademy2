from rest_framework import serializers

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from courses.models import Course
from users.models import Teacher
from contactus.models import Message


class ThumbnailSerializer(serializers.ImageField):
    def __init__(self, alias, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_only = True
        self.alias = alias

    def to_representation(self, value):
        if not value:
            return None

        url = thumbnail_url(value, self.alias)
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = 'id', 'first_name', 'last_name'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    thumbnail = ThumbnailSerializer(alias='thumbnail', source='image')
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
