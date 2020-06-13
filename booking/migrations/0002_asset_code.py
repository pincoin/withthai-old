# Generated by Django 3.0.7 on 2020-06-13 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='code',
            field=models.IntegerField(choices=[(0, 'GB prime pay'), (1, 'Petty cash'), (2, 'PayPal'), (3, 'Passbook Krungsri')], db_index=True, default=0, verbose_name='Asset code'),
        ),
    ]
