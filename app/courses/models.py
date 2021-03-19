from django.db import models
from django.urls import reverse_lazy

from easy_thumbnails.fields import ThumbnailerImageField

from users.models import Teacher, Student, unique_file_name


class Course(models.Model):
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    title = models.CharField(
        'Название', max_length=100, unique=True, blank=False, null=False)
    description = models.TextField('Описание', blank=False, null=False)
    teachers = models.ManyToManyField(
        Teacher, related_name='courses')
    image = ThumbnailerImageField(
        'Изображение', default='course/image.png', upload_to=unique_file_name)

    @property
    def get_absolute_url(self):
        return reverse_lazy(
            'courses:course_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class CourseGroup(models.Model):
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    title = models.CharField(
        'Название', max_length=100, unique=True, blank=False, null=False)
    course = models.ForeignKey(
            Course, related_name='course_group', on_delete=models.PROTECT)
    students = models.ManyToManyField(
        Student, related_name='course_groups')
    start_date = models.DateField(
        'Дата начала обучения', blank=False, null=False)
    end_date = models.DateField(
        'Дата окончания обучения', blank=False, null=False)
    certificate_issue_date = models.DateField(
        'Дата выдачи сертификата', blank=False, null=False)

    def __str__(self):
        return self.title


class Schedule(models.Model):
    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    lesson_date = models.DateField(
        'Дата проведения урока', blank=False, null=False)
    start_time = models.TimeField(
        'Время начала', blank=False, null=False)
    finish_time = models.TimeField(
        'Время окончания', blank=False, null=False)
    description = models.TextField('Описание', blank=False, null=False)
    teacher = models.ForeignKey(
        Teacher, related_name='schedules', on_delete=models.PROTECT)
    course_group = models.ForeignKey(
        CourseGroup, related_name='schedules', on_delete=models.PROTECT)

    @property
    def lesson_period(self):
        return f'{self.lesson_date}, {self.start_time} - {self.finish_time}'

    def __str__(self):
        return f'{self.lesson_period}. {self.course_group}'
