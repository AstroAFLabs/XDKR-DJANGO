# Generated by Django 5.0.2 on 2024-03-13 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='uploaded_content',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]