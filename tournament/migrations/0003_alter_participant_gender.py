# Generated by Django 3.2.11 on 2022-03-14 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别'),
        ),
    ]
