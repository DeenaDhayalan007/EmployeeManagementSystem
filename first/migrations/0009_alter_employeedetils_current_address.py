# Generated by Django 3.2.8 on 2021-10-09 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0008_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedetils',
            name='Current_Address',
            field=models.CharField(max_length=300),
        ),
    ]
