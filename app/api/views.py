from django.urls import reverse_lazy
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from contactus.models import Message
from courses.models import Course, CourseGroup
from users.models import Teacher

from api.serializers import CustomTokenRefreshSerializer, CustomTokenObtainPairSerializer, \
    MessageAdminSerializer, TeacherAdminSerializer, CourseAdminSerializer, TeacherSerializer, CourseSerializer, \
    CourseGroupBaseSerializer
from api.paginators import StandardResultsSetPagination
from api.permissions import IsStudent, IsRealSubscriber


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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


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


class SubscriptionToCourseViewSet(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  GenericViewSet):
    queryset = CourseGroup.objects.all()
    serializer_class = CourseGroupBaseSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = IsStudent, IsRealSubscriber

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        if not partial:
            return super().update(request, *args, **kwargs)
        instance = self.get_object()
        students_list = [student.pk for student in instance.students.all()]
        new_student = request.data['newStudent']
        students_list.append(new_student)
        serializer = self.get_serializer(
            instance,
            data={'students': set(students_list)},
            partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
