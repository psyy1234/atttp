# Generated by Django 3.0.5 on 2020-04-29 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Igrisce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=50)),
                ('telefon', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='GameHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateTimeField()),
                ('igrisce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atttp.Igrisce')),
                ('oseba_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oseba_1', to=settings.AUTH_USER_MODEL)),
                ('oseba_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oseba_2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('niz', models.IntegerField()),
                ('rezultat_1', models.IntegerField()),
                ('rezultat_2', models.IntegerField()),
                ('max_break_point', models.IntegerField(blank=True)),
                ('igra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atttp.GameHead')),
            ],
        ),
    ]