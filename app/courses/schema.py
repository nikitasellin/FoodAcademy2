import graphene
from django.shortcuts import get_object_or_404
from graphene_django.types import DjangoObjectType

from .models import Course, CourseGroup


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class CourseGroupType(DjangoObjectType):
    class Meta:
        model = CourseGroup


class Query:
    all_courses = graphene.List(CourseType, limit=graphene.Int())
    course_by_id = graphene.Field(CourseType, id=graphene.Int())
    all_groups = graphene.List(CourseGroupType, limit=graphene.Int())
    group_by_id = graphene.Field(CourseGroupType, id=graphene.Int())

    def resolve_all_courses(self, *args, **kwargs):
        if 'limit' in kwargs:
            return Course.objects.all()[:kwargs['limit']]
        return Course.objects.all()

    def resolve_course_by_id(self, info, **kwargs):
        return get_object_or_404(Course, pk=kwargs['id'])

    def resolve_all_groups(self, *args, **kwargs):
        if 'limit' in kwargs:
            return CourseGroup.objects.all()[:kwargs['limit']]
        return CourseGroup.objects.all()

    def resolve_group_by_id(self, info, **kwargs):
        return get_object_or_404(CourseGroup, pk=kwargs['id'])
