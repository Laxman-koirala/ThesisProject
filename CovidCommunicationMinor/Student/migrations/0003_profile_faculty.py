# Generated by Django 3.0.7 on 2021-02-01 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0002_profile_joinyear'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Faculty',
            field=models.TextField(default='Game Design and Development'),
        ),
    ]