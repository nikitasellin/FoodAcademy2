# Generated by Django 3.1.5 on 2021-01-31 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursegroup',
            name='students',
            field=models.ManyToManyField(related_name='course_groups', to='users.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(related_name='courses', to='users.Teacher'),
        ),
    ]
