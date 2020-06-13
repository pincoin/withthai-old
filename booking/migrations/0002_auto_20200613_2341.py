# Generated by Django 3.0.7 on 2020-06-13 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assettransaction',
            name='category',
            field=models.IntegerField(choices=[(0, 'Payment'), (1, 'Refund'), (2, 'Purchase'), (3, 'Purchase cancel'), (4, 'Transfer payment'), (5, 'Gains'), (6, 'Expense')], db_index=True, default=0, verbose_name='Transaction category'),
        ),
    ]
