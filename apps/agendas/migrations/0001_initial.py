# Generated by Django 5.0.4 on 2024-05-05 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('agenda_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('fecha_upd', models.DateField(auto_now=True)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
    ]
