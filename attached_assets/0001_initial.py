# Generated by Django 5.2 on 2025-04-03 13:18

import colorfield.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('start_date', models.DateTimeField(verbose_name='Start Date')),
                ('end_date', models.DateTimeField(verbose_name='End Date')),
                ('location', models.CharField(max_length=200, verbose_name='Location')),
                ('mode', models.CharField(choices=[('remote', 'Remote'), ('in_person', 'In Person')], default='in_person', max_length=10, verbose_name='Mode')),
                ('organizer', models.CharField(max_length=200, verbose_name='Organizer')),
                ('color', colorfield.fields.ColorField(default='#003d7c', image_field=None, max_length=25, samples=None, verbose_name='Calendar Color')),
                ('capacity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Capacity')),
                ('registered', models.PositiveIntegerField(default=0, verbose_name='Registered Participants')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('registered_at', models.DateTimeField(auto_now_add=True, verbose_name='Registered At')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='events.event')),
            ],
            options={
                'verbose_name': 'Registration',
                'verbose_name_plural': 'Registrations',
                'unique_together': {('event', 'email')},
            },
        ),
    ]
