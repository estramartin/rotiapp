# Generated by Django 5.0.4 on 2024-05-26 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_alter_productoinsumo_cantidad'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promocion',
            options={'verbose_name': 'Promoción unica', 'verbose_name_plural': 'Promociones varias'},
        ),
    ]
