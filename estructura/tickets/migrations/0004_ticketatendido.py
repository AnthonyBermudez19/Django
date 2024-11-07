# Generated by Django 5.1.2 on 2024-10-29 03:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_alter_ticket_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketAtendido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atendido_en', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tickets.ticket')),
            ],
        ),
    ]
