# Generated by Django 2.0.5 on 2018-05-11 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='后端开发', max_length=50, verbose_name='课程类别'),
        ),
    ]
