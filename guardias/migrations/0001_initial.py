# Generated by Django 5.2.1 on 2025-05-25 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guardia',
            fields=[
                ('id_guardia', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'guardia',
                'managed': False,
            },
        ),
    ]
