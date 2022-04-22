# Generated by Django 3.2.11 on 2022-03-19 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_auto_20220319_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='drwas',
            field=models.SmallIntegerField(default=0, verbose_name='平场数'),
        ),
        migrations.AddField(
            model_name='participant',
            name='goals',
            field=models.SmallIntegerField(default=0, verbose_name='进球数'),
        ),
        migrations.AddField(
            model_name='participant',
            name='goals_conceded',
            field=models.SmallIntegerField(default=0, verbose_name='失球数'),
        ),
        migrations.AddField(
            model_name='participant',
            name='losts',
            field=models.SmallIntegerField(default=0, verbose_name='负场数'),
        ),
        migrations.AddField(
            model_name='participant',
            name='points',
            field=models.SmallIntegerField(default=0, verbose_name='积分'),
        ),
        migrations.AddField(
            model_name='participant',
            name='wins',
            field=models.SmallIntegerField(default=0, verbose_name='胜场数'),
        ),
    ]
