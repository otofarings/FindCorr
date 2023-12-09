from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404
from django.http import HttpRequest, HttpResponse

from .models import CorrelationFull


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


def corr_lst(request: HttpRequest) -> HttpResponse:
    corr_list = round_corr(CorrelationFull.objects.all())

    industry = request.GET.get('industry', '').strip()
    if industry:
        corr_list = filter_industry(corr_list, industry)

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
         'selected_industry': industry}
    )


def corr(request, ticker):
    corr_list = get_list_or_404(CorrelationFull, ticker_a=ticker)
    corr_list = round_corr(corr_list)
    paginator = Paginator(corr_list, 20)

    page_number = request.GET.get('page')
    correlations = paginator.get_page(page_number)

    return render(request, f'db/group/detail.html', {'correlations': correlations})
