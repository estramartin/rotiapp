# Generated by Django 5.0.4 on 2024-05-11 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventadet',
            name='cantidad',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
    ]
