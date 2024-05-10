# Generated by Django 5.0.4 on 2024-05-07 23:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_clientevianda'),
        ('personas', '0006_alter_personadomicilio_direccion_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={},
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cli_id',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='persona_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.persona'),
        ),
    ]
