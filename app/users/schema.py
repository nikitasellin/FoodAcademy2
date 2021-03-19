import graphene
from django.shortcuts import get_object_or_404
from graphene_django.types import DjangoObjectType

from .models import Teacher, Student, CommonUser


class UserType(DjangoObjectType):
    class Meta:
        model = CommonUser

    full_name = graphene.String(source='full_name')


class TeacherType(UserType):
    class Meta:
        model = Teacher


class StudentType(UserType):
    class Meta:
        model = Student


class Query:
    all_teachers = graphene.List(TeacherType, limit=graphene.Int())
    teacher_by_id = graphene.Field(TeacherType, id=graphene.Int())
    all_students = graphene.List(StudentType, limit=graphene.Int())
    student_by_id = graphene.Field(StudentType, id=graphene.Int())

    def resolve_all_teachers(self, info, **kwargs):
        if 'limit' in kwargs:
            return Teacher.objects.all()[:kwargs['limit']]
        return Teacher.objects.all()

    def resolve_teacher_by_id(self, info, **kwargs):
        return get_object_or_404(Teacher, pk=kwargs['id'])

    def resolve_all_students(self, info, **kwargs):
        if 'limit' in kwargs:
            return Student.objects.all()[:kwargs['limit']]
        return Student.objects.all()

    def resolve_student_by_id(self, info, **kwargs):
        return get_object_or_404(Student, pk=kwargs['id'])
