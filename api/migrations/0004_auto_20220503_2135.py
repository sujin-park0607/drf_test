# Generated by Django 3.1.3 on 2022-05-03 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20220503_2057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='passward',
            new_name='password',
        ),
    ]
