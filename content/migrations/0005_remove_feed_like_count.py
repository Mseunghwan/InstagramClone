# Generated by Django 3.2.15 on 2022-11-12 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_reply_reply_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='like_count',
        ),
    ]