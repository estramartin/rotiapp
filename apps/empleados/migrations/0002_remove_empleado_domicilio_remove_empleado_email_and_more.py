# Generated by Django 5.0.4 on 2024-05-04 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='domicilio',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='email',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='telefono',
        ),
    ]