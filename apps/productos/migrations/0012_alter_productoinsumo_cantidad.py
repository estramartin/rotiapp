# Generated by Django 5.0.4 on 2024-05-06 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0011_alter_categoria_precio_standar_alter_producto_margen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoinsumo',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=18),
        ),
    ]
