# Generated by Django 4.2.7 on 2023-12-08 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0008_alter_correlationsfull_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Correlation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ticker_A', models.CharField(max_length=20)),
                ('ticker_B', models.CharField(max_length=20)),
                ('correlation', models.FloatField()),
                ('calc_dt', models.DateTimeField()),
            ],
            options={
                'db_table': 'correlations',
                'ordering': ('correlation',),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CorrelationFull',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ticker_a', models.CharField(max_length=20)),
                ('name_a', models.CharField(max_length=100)),
                ('sector_a', models.CharField(max_length=50)),
                ('ticker_b', models.CharField(max_length=20)),
                ('name_b', models.CharField(max_length=100)),
                ('sector_b', models.CharField(max_length=50)),
                ('correlation', models.FloatField()),
                ('status', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'correlations_full',
                'ordering': ['-correlation'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ticker', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=255)),
                ('sector', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'decoding',
                'ordering': ('id',),
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Correlations',
        ),
        migrations.DeleteModel(
            name='CorrelationsFull',
        ),
        migrations.DeleteModel(
            name='TickerList',
        ),
    ]
