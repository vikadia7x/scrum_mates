# Generated by Django 2.1.2 on 2018-10-28 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showtimefinder', '0020_auto_20181028_1742'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MovieGenre',
        ),
        migrations.DeleteModel(
            name='MovieMetaData',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]