from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Administrator, Teacher, Student


@admin.register(Administrator)
class AdministratorAdmin(UserAdmin):
    model = Administrator
    list_display = ('first_name', 'last_name', 'email',
                    'phone_number', 'is_active', 'is_staff',
                    'is_superuser')
    list_display_links = ('email',)
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'last_name')
    ordering = ('last_name', 'email')

    fieldsets = (
        ('Основная информация',
         {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Статус',
         {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )
    add_fieldsets = (
        ('Основная информация',
         {'fields':
             ('email', 'first_name', 'last_name', 'password1', 'password2')}),
        ('Статус',
         {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )


@admin.register(Teacher)
class TeacherAdmin(AdministratorAdmin):
    model = Teacher

    fieldsets = (
        ('Основная информация',
         {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Статус',
         {'fields': ('is_active',)}),
        ('Дополнительная информация',
         {'fields': ('bio',)})
    )
    add_fieldsets = (
        ('Основная информация',
         {'fields':
             ('email', 'first_name', 'last_name', 'password1', 'password2')}),
        ('Статус',
         {'fields': ('is_active',)}),
        ('Дополнительная информация',
         {'fields': ('bio',)})
    )


@admin.register(Student)
class StudentAdmin(AdministratorAdmin):
    model = Student

    fieldsets = (
        ('Основная информация',
         {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Статус',
         {'fields': ('is_active',)}),
        ('Дополнительная информация',
         {'fields': ('birth_date',)})
    )
    add_fieldsets = (
        ('Основная информация',
         {'fields':
             ('email', 'first_name', 'last_name', 'password1', 'password2')}),
        ('Статус',
         {'fields': ('is_active',)}),
        ('Дополнительная информация',
         {'fields': ('birth_date',)})
    )
