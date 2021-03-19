import datetime

from django.core.management import BaseCommand
from factory import django, Faker, PostGenerationMethodCall

from users.models import CommonUser, Teacher, Student


class CommonUserFactory(django.DjangoModelFactory):
    class Meta:
        model = CommonUser

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', 'password')
    phone_number = Faker('msisdn')


class TeacherFactory(CommonUserFactory):
    class Meta:
        model = Teacher

    bio = Faker('text', max_nb_chars=500, ext_word_list=None)


class StudentFactory(CommonUserFactory):
    class Meta:
        model = Student

    birth_date = Faker(
        'date_between_dates',
        date_start=datetime.date(1970, 1, 1),
        date_end=datetime.date(1993, 1, 1)
    )


def create_teachers(count):
    if Teacher.objects.all():
        print('Преподаватели уже добавлены')
        return
    with Faker.override_default_locale('ru_RU'):
        for i in range(count):
            factory = TeacherFactory
            factory.create()
    print('Преподаватели успешно добавлены')


def create_students(count):
    if Student.objects.all():
        print('Студенты уже добавлены')
        return
    with Faker.override_default_locale('ru_RU'):
        for i in range(count):
            factory = StudentFactory
            factory.create()
    print('Студенты успешно добавлены')


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_teachers(5)
        create_students(10)
