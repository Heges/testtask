# Generated by Django 3.0.7 on 2020-09-03 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_service_data_to_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='data_to_work',
            field=models.DateField(verbose_name='День записи'),
        ),
    ]
