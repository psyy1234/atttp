# Generated by Django 3.0.5 on 2020-05-04 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atttp', '0002_auto_20200429_1100'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='gamehead',
            constraint=models.UniqueConstraint(fields=('datum', 'igrisce', 'oseba_1', 'oseba_2'), name='unique_head'),
        ),
    ]
