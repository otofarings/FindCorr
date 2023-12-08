# Generated by Django 4.2.7 on 2023-12-08 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_decodingdb_tickerlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrelationDetails',
            fields=[
                ('correlation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='db.correlations')),
                ('ticker_A_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ticker_A_details', to='db.tickerlist')),
                ('ticker_B_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ticker_B_details', to='db.tickerlist')),
            ],
        ),
    ]
