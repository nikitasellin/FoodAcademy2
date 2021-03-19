from django.contrib import admin

from .models import Course, CourseGroup, Schedule

admin.site.register(Course)
admin.site.register(Schedule)


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0
    ordering = 'lesson_date',


@admin.register(CourseGroup)
class CourseGroupAdmin(admin.ModelAdmin):
    list_display = 'title', 'start_date', 'end_date'
    ordering = '-start_date',
    inlines = ScheduleInline,
