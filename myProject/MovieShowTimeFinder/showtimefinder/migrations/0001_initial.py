# Generated by Django 2.1.1 on 2018-09-19 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(max_length=100)),
                ('last_name', models.TextField(blank=True, max_length=500)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
