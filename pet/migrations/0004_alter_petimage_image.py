# Generated by Django 5.2 on 2025-04-22 15:24

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0003_petimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petimage',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
