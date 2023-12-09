# Generated by Django 5.0 on 2023-12-09 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0011_candles'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandlesDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'candles',
                'managed': False,
            },
        ),
    ]