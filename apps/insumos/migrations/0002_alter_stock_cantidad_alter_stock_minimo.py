# Generated by Django 5.0.4 on 2024-05-11 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insumos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='cantidad',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
        migrations.AlterField(
            model_name='stock',
            name='minimo',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5),
        ),
    ]
