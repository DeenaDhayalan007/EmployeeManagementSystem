# Generated by Django 3.2.7 on 2021-10-01 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0004_auto_20211001_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='lat',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='lon',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=100),
        ),
    ]
