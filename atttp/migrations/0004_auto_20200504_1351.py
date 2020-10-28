# Generated by Django 3.0.5 on 2020-05-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atttp', '0003_auto_20200504_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamedetail',
            name='niz',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
        migrations.AlterField(
            model_name='igrisce',
            name='naziv',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AddConstraint(
            model_name='gamedetail',
            constraint=models.UniqueConstraint(fields=('igra', 'niz'), name='unique_detail'),
        ),
        migrations.AddConstraint(
            model_name='igrisce',
            constraint=models.UniqueConstraint(fields=('naziv',), name='unique_court'),
        ),
    ]