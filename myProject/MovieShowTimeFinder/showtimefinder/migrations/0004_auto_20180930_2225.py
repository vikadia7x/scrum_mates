# Generated by Django 2.1.1 on 2018-09-30 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showtimefinder', '0003_auto_20180930_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='username1',
        ),
    ]
