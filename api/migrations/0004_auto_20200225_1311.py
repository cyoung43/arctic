# Generated by Django 3.0.3 on 2020-02-25 20:11

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200225_1251'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
