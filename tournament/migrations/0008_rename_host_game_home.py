# Generated by Django 3.2.11 on 2022-03-19 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0007_auto_20220319_1021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='host',
            new_name='home',
        ),
    ]