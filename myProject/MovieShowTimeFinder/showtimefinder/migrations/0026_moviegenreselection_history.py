# Generated by Django 2.1.1 on 2018-11-23 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showtimefinder', '0025_remove_moviegenreselection_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviegenreselection',
            name='History',
            field=models.BooleanField(null=True),
        ),
    ]