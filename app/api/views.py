from django.urls import reverse_lazy
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet

from contactus.models import Message
from courses.models import Course
from users.models import Teacher

from .serializers import CourseSerializer, TeacherSerializer, \
    TeacherAdminSerializer, CourseAdminSerializer, MessageAdminSerializer
from .paginators import StandardResultsSetPagination


class RootView(APIView):
    def get(self, request):
        links = {
            'Readonly views': request.build_absolute_uri(
                    reverse_lazy('api:view_models:api-root')),
            'Full access': request.build_absolute_uri(
                reverse_lazy('api:full_access:api-root')),
            'Obtain token': request.build_absolute_uri(
                reverse_lazy('api:token_obtain_pair')),
            'Refresh token': request.build_absolute_uri(
                reverse_lazy('api:token_refresh')),
        }
        return Response(links)


class CoursesViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination


class TeachersViewSet(ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = StandardResultsSetPagination


class CourseAdminViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseAdminSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = IsAdminUser,


class TeacherAdminViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherAdminSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = IsAdminUser,


class MessageAdminViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageAdminSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = IsAdminUser,
