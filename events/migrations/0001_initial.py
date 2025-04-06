# Generated by Django 5.2 on 2025-04-06 19:24

import colorfield.fields
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nazwa')),
                ('description', models.TextField(verbose_name='Opis')),
                ('start_date', models.DateTimeField(verbose_name='Data rozpoczęcia')),
                ('end_date', models.DateTimeField(verbose_name='Data zakończenia')),
                ('location', models.CharField(max_length=200, verbose_name='Lokalizacja')),
                ('mode', models.CharField(choices=[('remote', 'Zdalnie'), ('in_person', 'Stacjonarnie')], default='in_person', max_length=10, verbose_name='Tryb')),
                ('organizer', models.CharField(max_length=200, verbose_name='Organizator')),
                ('color', colorfield.fields.ColorField(default='#003d7c', image_field=None, max_length=25, samples=None, verbose_name='Kolor w kalendarzu')),
                ('capacity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Pojemność')),
                ('registered', models.PositiveIntegerField(default=0, verbose_name='Zarejestrowani uczestnicy')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Zaktualizowano')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_events', to=settings.AUTH_USER_MODEL, verbose_name='Twórca')),
            ],
            options={
                'verbose_name': 'Wydarzenie',
                'verbose_name_plural': 'Wydarzenia',
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True, verbose_name='Data rejestracji')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to='events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Rejestracja na wydarzenie',
                'verbose_name_plural': 'Rejestracje na wydarzenia',
                'unique_together': {('user', 'event')},
            },
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='events', through='events.EventRegistration', to=settings.AUTH_USER_MODEL),
        ),
    ]
