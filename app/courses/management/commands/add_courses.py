import datetime
from random import choice, randint

from django.core.management import BaseCommand
from factory import django, Faker, LazyAttribute, SubFactory
from factory.fuzzy import FuzzyDate

from courses.models import Course, CourseGroup
from users.models import Teacher, Student


TODAY = datetime.date.today()


class CourseFactory(django.DjangoModelFactory):
    class Meta:
        model = Course

    title = Faker('job')
    description = Faker('text', max_nb_chars=1000, ext_word_list=None)


class CourseGroupFactory(django.DjangoModelFactory):
    class Meta:
        model = CourseGroup

    course = SubFactory(CourseFactory)
    start_date = FuzzyDate(
        TODAY,
        TODAY + datetime.timedelta(days=30))
    end_date = LazyAttribute(lambda o: o.start_date + o.duration)
    certificate_issue_date = LazyAttribute(lambda o: o.end_date + o.cert_delay)

    class Params:
        cert_delay = datetime.timedelta(days=30)
        duration = datetime.timedelta(days=150)


def add_course(factory, teachers):
    course = factory.create()
    for teacher_id in range(randint(1, teachers.count())):
        teacher = choice(teachers)
        course.teachers.add(teacher)
    return course


def add_course_group(factory, course, students):
    course_group = factory.build()
    course_group.course = course
    group_title = f'{course.title}-{course_group.start_date.year}-{course_group.start_date.month}'
    course_group.title = group_title
    course_group.save()
    for student_id in range(randint(1, students.count())):
        student = choice(students)
        course_group.students.add(student)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if CourseGroup.objects.all():
            print('Курсы и группы уже добавлены')
            return
        all_teachers = Teacher.objects.all()
        all_students = Student.objects.all()
        if not (all_teachers and all_students):
            print('Сначала добавьте пользователей')
            return
        with Faker.override_default_locale('ru_RU'):
            course_factory = CourseFactory
            group_factory = CourseGroupFactory
            for c in range(5):
                course = add_course(course_factory, all_teachers)
                add_course_group(group_factory, course, all_students)
        print('Курсы и группы успешно добавлены')
