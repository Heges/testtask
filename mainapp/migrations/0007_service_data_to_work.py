# Generated by Django 3.0.7 on 2020-09-03 07:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20200831_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='data_to_work',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Число работы'),
            preserve_default=False,
        ),
    ]
