# Generated by Django 3.0.1 on 2020-10-11 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BodegaApp', '0002_auto_20201010_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodega',
            name='productos',
            field=models.ManyToManyField(to='BodegaApp.Producto', verbose_name='Productos'),
        ),
    ]