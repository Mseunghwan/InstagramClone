# Generated by Django 3.2.15 on 2022-11-11 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='user_id',
        ),
        migrations.AddField(
            model_name='feed',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
