# Generated by Django 4.2.2 on 2023-06-14 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('card_number', models.IntegerField(primary_key=True, serialize=False)),
                ('pin', models.CharField(max_length=128)),
                ('blocked', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
            options={
                'db_table': 'card',
                'managed': True,
            },
        ),
    ]