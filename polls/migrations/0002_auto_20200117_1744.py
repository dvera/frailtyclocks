# Generated by Django 2.2.5 on 2020-01-17 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agelife',
            old_name='frighresult',
            new_name='frightresult',
        ),
    ]
