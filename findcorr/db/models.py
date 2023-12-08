from django.db import models


class Correlation(models.Model):
    id = models.AutoField(primary_key=True)
    ticker_A = models.CharField(max_length=20)
    ticker_B = models.CharField(max_length=20)
    correlation = models.FloatField()
    calc_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'correlations'
        ordering = ('id',)
    
    def __str__(self):
        return f'{self.ticker_A}_{self.ticker_B}'


class Ticker(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'decoding'
        ordering = ('id',)
    
    def __str__(self):
        return self.ticker


class CorrelationFull(models.Model):
    id = models.AutoField(primary_key=True)
    ticker_a = models.CharField(max_length=20)
    name_a = models.CharField(max_length=100)
    sector_a = models.CharField(max_length=50)
    ticker_b = models.CharField(max_length=20)
    name_b = models.CharField(max_length=100)
    sector_b = models.CharField(max_length=50)
    correlation = models.FloatField()
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'correlations_full'
        ordering = ('id',)
        indexes = [
            models.Index(fields=['ticker_a', 'ticker_b']),
        ]
    
    def __str__(self):
        return f'{self.ticker_a}_{self.ticker_b}'


class CorrelationsDB(models.Model):
    description = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False
        db_table = 'correlations'


class DecodingDB(models.Model):
    description = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False
        db_table = 'decoding'


class CorrelationsFullDB(models.Model):
    description = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False
        db_table = 'correlations_full'


class AlgoPackDBRouter(object):
    def db_for_read(self, model, **hints):
        if model in [Correlation, Ticker, CorrelationFull]:
            return 'algo_pack'
        return None

    def db_for_write(self, model, **hints):
        if model in [Correlation, Ticker, CorrelationFull]:
            return 'algo_pack'
        return None

