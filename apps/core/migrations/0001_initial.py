# Generated by Django 5.0.4 on 2024-05-10 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocTipo',
            fields=[
                ('tipo_doc_id', models.AutoField(primary_key=True, serialize=False)),
                ('sigla', models.CharField(default='DNI', max_length=5)),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
    ]
