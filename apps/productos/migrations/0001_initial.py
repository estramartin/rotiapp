# Generated by Django 5.0.4 on 2024-05-10 01:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agendas', '0001_initial'),
        ('insumos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('categoria_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('precio_standar', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=18, null=True)),
                ('is_precio_standar', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('producto_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('fecha_upd', models.DateField(auto_now=True)),
                ('margen', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('promocion_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('fecha_inicio', models.DateField(auto_now=True)),
                ('fecha_fin', models.DateField(auto_now=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Promoción',
                'verbose_name_plural': 'Promociones',
            },
        ),
        migrations.CreateModel(
            name='ProductoInsumo',
            fields=[
                ('producto_insumo_id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=18)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('fecha_upd', models.DateField(auto_now=True)),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='insumos.insumo')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insumos', to='productos.producto')),
            ],
        ),
        migrations.CreateModel(
            name='PromocionProducto',
            fields=[
                ('prom_prod_id', models.AutoField(primary_key=True, serialize=False)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promociones', to='productos.producto')),
                ('promocion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='productos.promocion')),
            ],
        ),
        migrations.CreateModel(
            name='Vianda',
            fields=[
                ('vianda_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('fecha_upd', models.DateField(auto_now=True)),
                ('activo', models.BooleanField(default=True)),
                ('precio_standar', models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ('agenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viandas', to='agendas.agenda')),
            ],
            options={
                'verbose_name': 'Vianda',
                'verbose_name_plural': 'Viandas',
                'unique_together': {('nombre', 'agenda')},
            },
        ),
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('cat_prod_id', models.AutoField(primary_key=True, serialize=False)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='productos.categoria')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='productos.producto')),
            ],
            options={
                'unique_together': {('categoria', 'producto')},
            },
        ),
        migrations.CreateModel(
            name='ViandaProducto',
            fields=[
                ('vianda_prod_id', models.AutoField(primary_key=True, serialize=False)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viandas', to='productos.producto')),
                ('vianda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='productos.vianda')),
            ],
            options={
                'unique_together': {('vianda', 'producto')},
            },
        ),
    ]
