from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from .models import CorrelationFull


def round_corr(correlations):
        for group in correlations:
            group.correlation = round(group.correlation * 100)
        return correlations


def corr_lst(request):
    corr_list = CorrelationFull.objects.all()
    corr_list = round_corr(corr_list)
    paginator = Paginator(corr_list, 20)  # Show 20 correlations per page

    page_number = request.GET.get('page')
    correlations = paginator.get_page(page_number)

    industries = CorrelationFull.objects.values_list('sector_a', flat=True).distinct()
    industries = sorted(list(set(industries)))

    return render(request, 'db/group/list.html', {'industries': industries, 'correlations': correlations})


def corr(request, ticker):
    corr_list = get_list_or_404(CorrelationFull, ticker_a=ticker)
    corr_list = round_corr(corr_list)
    paginator = Paginator(corr_list, 20)

    page_number = request.GET.get('page')
    correlations = paginator.get_page(page_number)

    return render(request, f'db/group/detail.html', {'correlations': correlations})
