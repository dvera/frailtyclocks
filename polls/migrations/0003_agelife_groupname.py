# Generated by Django 2.2.5 on 2020-01-17 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200117_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='agelife',
            name='groupname',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
