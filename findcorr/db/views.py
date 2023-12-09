import json

from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404
from django.http import HttpRequest, HttpResponse

from .models import CorrelationFull
from .dirt_correlation import get_df_to_plot


def round_corr(correlations: CorrelationFull) -> CorrelationFull:
        for group in correlations:
            if isinstance(group.correlation, float):
                group.correlation = round(group.correlation * 100)
        return correlations


def filter_industry(correlations: CorrelationFull, industry: str) -> CorrelationFull:
    correlations_filtered = []
    for group in correlations:
        group.sector_a, group.sector_b = group.sector_a.strip(), group.sector_b.strip()
        if (group.sector_a == industry) or (group.sector_b == industry):
            correlations_filtered.append(group)
    return correlations_filtered


def search_by_ticker(correlations: CorrelationFull, ticker: str) -> CorrelationFull:
    correlations_filtered = []
    for group in correlations:
        if (ticker in group.ticker_a.lower()) or (ticker in group.ticker_b.lower()):
            correlations_filtered.append(group)
    return correlations_filtered


def corr_lst(request: HttpRequest) -> HttpResponse:
    corr_list = round_corr(CorrelationFull.objects.all())

    industry = request.GET.get('industry', '').strip()
    if industry:
        corr_list = filter_industry(corr_list, industry)
    
    ticker = request.GET.get('q', '').strip()
    if ticker:
        corr_list = search_by_ticker(corr_list, ticker)

    sort = request.GET.get('sort', '')
    direction = request.GET.get('direction', 'asc')
    if sort:
        if direction == 'none':
            sort = 'id'
        if direction == 'desc':
            sort = '-' + sort
        corr_list = corr_list.order_by(sort)

    industries = CorrelationFull.objects.values_list('sector_a', flat=True).distinct()
    industries = sorted([ind.strip() for ind in set(industries) if ind.strip() != industry])
    
    paginator = Paginator(corr_list, 20)  # Show 20 correlations per page

    page_number = request.GET.get('page', '')
    correlations = paginator.get_page(page_number)

    return render(
        request, 
        'db/group/list.html', 
        {'industries': industries, 
         'correlations': correlations,
         'selected_industry': industry,}
    )


def corr(request: HttpRequest, ticker_a: str, ticker_b: str) -> HttpResponse:
    ticker_a, ticker_b = ticker_a.strip(), ticker_b.strip()
    corr_list = get_list_or_404(CorrelationFull, ticker_a=ticker_a, ticker_b=ticker_b)
    corr_list = round_corr(corr_list)

    df_plot = get_df_to_plot(ticker_a, ticker_b, '2021-12-01 00:00:00', '2023-12-01 00:00:00')
    lst_index = df_plot.index.tolist()
    ohlc_a = df_plot['OHLC_A_scaled'].tolist()
    ohlc_b = df_plot['OHLC_B_scaled'].tolist()
    spread_scaled = df_plot['spread_scaled'].tolist()
    # spread_medium = df_plot['spread_medium'].tolist()
    spread_medium = df_plot['spread_medium_line'].tolist()

    title = f"Масштабированная OHLC цена {ticker_a}  (тикер А) и {ticker_b} (тикер B), спред и лин. регрессия"

    return render(
        request, 
        'db/group/detail.html', 
        {'correlation': corr_list[0],
         'lst_index': json.dumps(lst_index),
         'ohlc_a': json.dumps(ohlc_a),
         'ohlc_b': json.dumps(ohlc_b),
         'spread_scaled': json.dumps(spread_scaled),
         'spread_medium': json.dumps(spread_medium),
         'title': title,
         'ticker_a': ticker_a,
         'ticker_b': ticker_b,}
    )
