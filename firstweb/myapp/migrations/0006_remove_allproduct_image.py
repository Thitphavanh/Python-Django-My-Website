# Generated by Django 3.2 on 2021-12-21 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20211221_2112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allproduct',
            name='image',
        ),
    ]
