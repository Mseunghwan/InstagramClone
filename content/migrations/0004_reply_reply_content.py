# Generated by Django 3.2.15 on 2022-11-11 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_bookmark_like_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='reply_content',
            field=models.TextField(default=''),
        ),
    ]