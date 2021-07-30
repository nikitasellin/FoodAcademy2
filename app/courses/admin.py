from django.contrib import admin

from .models import Course, CourseGroup, Schedule


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = 'title', 'teachers_list',

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('teachers')

    def teachers_list(self, obj: Course):
        teachers = obj.teachers.all()
        return ', '.join((t.full_name for t in teachers))


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = 'lesson_period', 'course_group', 'teacher',

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('course_group')


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0
    ordering = 'lesson_date',


@admin.register(CourseGroup)
class CourseGroupAdmin(admin.ModelAdmin):
    list_display = 'title', 'start_date', 'end_date', 'students_list',
    ordering = '-start_date',
    inlines = ScheduleInline,

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('students')

    def students_list(self, obj: Course):
        students = obj.students.all()
        return ', '.join((s.full_name for s in students))
