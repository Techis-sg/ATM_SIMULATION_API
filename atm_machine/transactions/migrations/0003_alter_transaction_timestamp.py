# Generated by Django 4.2.2 on 2023-06-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transaction_actiontype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default='2023-06-14 23:53:42'),
        ),
    ]
