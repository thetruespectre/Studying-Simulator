# Generated by Django 5.0.1 on 2024-02-10 07:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_classroom_participants'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='participants',
            field=models.ManyToManyField(blank=True, null=True, related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]
