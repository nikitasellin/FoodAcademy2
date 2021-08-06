from django.contrib.auth import get_user_model
from rest_framework import serializers

from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend

from courses.models import Course, CourseGroup, Schedule
from users.models import Teacher
from contactus.models import Message
from users.utils import get_user_role


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


class CourseGroupBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseGroup
        fields = ('id', 'title', 'start_date', 'students')


class CourseSerializer(serializers.ModelSerializer):
    course_group = CourseGroupBaseSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    thumbnail = ThumbnailSerializer(alias='thumbnail', source='image')
    teachers = TeacherSerializer(many=True, read_only=True)


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

    teacher = TeacherSerializer(read_only=True)


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
    teachers = TeacherSerializer(many=True, read_only=True)


class MessageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('first_name', 'last_name', 'email', 'phone_number',
                            'title', 'text', 'received_time')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update(
            {
                'user': dict(
                    pk=self.user.pk,
                    full_name=self.user.full_name,
                    email=self.user.email,
                    role=get_user_role(self.user.pk),
                )
            }
        )
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_pk = decoded_payload['user_id']
        user_model = get_user_model()
        user = user_model.objects.get(id=user_pk)
        data.update(
            {
                'user': dict(
                    pk=user.pk,
                    full_name=user.full_name,
                    email=user.email,
                    role=get_user_role(user.pk),
                )
            }
        )
        return data
