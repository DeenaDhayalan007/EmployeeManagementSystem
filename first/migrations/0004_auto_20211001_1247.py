# Generated by Django 3.2.7 on 2021-10-01 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0003_auto_20210927_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='lat',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='address',
            name='lon',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='address',
            name='pincode',
            field=models.CharField(max_length=100, verbose_name='pincode'),
        ),
    ]
