# Generated by Django 5.0.4 on 2024-05-04 19:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0006_promocion_promocionproducto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('venta_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('fecha_upd', models.DateField(auto_now=True)),
                ('total', models.FloatField()),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VentaDet',
            fields=[
                ('venta_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('precio', models.FloatField()),
                ('cantidad', models.FloatField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('fecha_upd', models.DateField(auto_now=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='ventas.venta')),
            ],
        ),
    ]
