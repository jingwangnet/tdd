# Generated by Django 3.2.7 on 2022-02-04 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_auto_20220131_0151'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('text', 'list')},
        ),
    ]
