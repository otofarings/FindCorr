# Generated by Django 4.2.7 on 2023-12-07 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlgoPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker_a', models.CharField(max_length=20)),
                ('ticker_b', models.CharField(max_length=20)),
                ('corr', models.FloatField()),
            ],
            options={
                'db_table': 'correlations',
                'managed': False,
            },
        ),
    ]
