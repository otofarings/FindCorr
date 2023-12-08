from django.contrib import admin
from .models import Correlation, Ticker, CorrelationFull


@admin.register(Correlation)
class CorrelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker_A', 'ticker_B', 'correlation')
    search_fields = ('ticker_A', 'ticker_B')
    ordering = ('id', 'correlation', 'ticker_A', 'ticker_B')
    empty_value_display = '-пусто-'


@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'name', 'sector')
    search_fields = ('ticker', 'name', 'sector')
    ordering = ('id',)
    empty_value_display = '-пусто-'


@admin.register(CorrelationFull)
class CorrelationDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker_a', 'name_a', 'sector_a', 'ticker_b', 'name_b', 'sector_b', 'correlation', 'status')
    search_fields = ('ticker_a', 'ticker_b', 'sector_a', 'sector_b', 'name_a', 'name_b', 'status')
    ordering = ('id', 'correlation', 'ticker_a', 'ticker_b')
    empty_value_display = '-пусто-'
