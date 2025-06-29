# Generated by Django 5.2 on 2025-06-26 15:26

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=cloudinary.models.CloudinaryField(blank=True, default='profile_pics/default', max_length=255, null=True, verbose_name='image'),
        ),
    ]
