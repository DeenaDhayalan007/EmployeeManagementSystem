# Generated by Django 3.2.7 on 2021-09-27 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeedetils',
            name='Employee_Name',
            field=models.CharField(default='Employee_Name', max_length=50, verbose_name='Employee_Name'),
        ),
    ]
