# Generated by Django 3.2.11 on 2022-03-29 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0012_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(max_length=64, verbose_name='密码'),
        ),
    ]
