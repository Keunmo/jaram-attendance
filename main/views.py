from django.shortcuts import render
from .models import Member


def atd_ranking(request):
    member_lists = Member.objects.order_by('-atd_checked')
    return render(request, 'main/atd_ranking.html', {'member_lists': member_lists})