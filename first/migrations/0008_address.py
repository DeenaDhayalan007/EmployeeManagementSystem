# Generated by Django 3.2.7 on 2021-10-01 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('first', '0007_delete_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(decimal_places=10, default=0.0, max_digits=100)),
                ('lon', models.DecimalField(decimal_places=10, default=0.0, max_digits=100)),
                ('city', models.CharField(max_length=100, verbose_name='city')),
                ('district', models.CharField(max_length=100, verbose_name='district')),
                ('state', models.CharField(max_length=100, verbose_name='State')),
                ('pincode', models.CharField(max_length=100, verbose_name='pincode')),
                ('country', models.CharField(max_length=255, verbose_name='Country')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
