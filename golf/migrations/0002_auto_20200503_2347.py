# Generated by Django 3.0.5 on 2020-05-03 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='position',
            field=models.IntegerField(db_index=True, default=0, verbose_name='Position'),
        ),
        migrations.AddField(
            model_name='district',
            name='position',
            field=models.IntegerField(db_index=True, default=0, verbose_name='Position'),
        ),
        migrations.AddField(
            model_name='province',
            name='position',
            field=models.IntegerField(db_index=True, default=0, verbose_name='Position'),
        ),
    ]
