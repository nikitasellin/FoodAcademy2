from django import forms

from .models import Course, Teacher


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'image', 'teachers')

    teachers = forms.ModelMultipleChoiceField(
        label='Преподаватели',
        queryset=Teacher.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
