# Generated by Django 2.0.5 on 2018-05-07 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('easy', '初级'), ('medium', '中级'), ('hard', '高级')], max_length=10),
        ),
    ]
