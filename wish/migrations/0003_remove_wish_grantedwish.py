# Generated by Django 2.2 on 2020-08-26 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wish', '0002_auto_20200826_1003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish',
            name='grantedwish',
        ),
    ]
