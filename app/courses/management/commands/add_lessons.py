from datetime import timedelta, datetime
from random import randint, randrange

from django.core.management import BaseCommand

from courses.models import Schedule, CourseGroup

START_TIME = datetime.strptime('20:00', '%H:%M').time()
FINISH_TIME = datetime.strptime('22:00', '%H:%M').time()


def random_date(start, end):
    delta = end - start
    int_delta = delta.days
    random_day = randrange(int_delta)
    return start + timedelta(days=random_day)


def add_lesson(course_groups_list, counter):
    idx = randint(0, len(course_groups_list) - 1)
    group = course_groups_list[idx]
    course = group.course
    teachers = course.teachers.all()
    teachers_list = [t for t in teachers]
    idx = randint(0, len(teachers_list) - 1)
    teacher = teachers_list[idx]
    lesson_date = random_date(group.start_date, group.end_date)
    description = f'{course.title}, урок #{counter}'
    lesson = Schedule.objects.create(
        lesson_date=lesson_date,
        start_time=START_TIME,
        finish_time=FINISH_TIME,
        description=description,
        teacher=teacher,
        course_group=group
    )
    print(lesson)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Schedule.objects.all():
            print('Уроки уже добавлены')
            return
        all_course_groups = CourseGroup.objects.all()
        if not all_course_groups:
            print('Сначала добавьте группы')
            return
        groups = [group for group in all_course_groups]
        for c in range(15):
            add_lesson(groups, c)
        print('Уроки успешно добавлены')


