from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

from .models import Member

def atd_ranking(request):
    member_lists = Member.objects.order_by('-atd_checked')
    member_lists = member_lists[:5]
    return render(request, 'main/atd_ranking.html', {'member_lists': member_lists})

def full_ranking(request):
    member_lists = Member.objects.order_by('-atd_checked')
    return render(request, 'main/full_ranking.html', {'member_lists': member_lists})

# @ensure_csrf_cookie
@csrf_exempt
def atd_check(request):
    if request.method == "POST":
        act_card_id = request.POST.get('card_id')
        try:
            mem_lookup = Member.objects.get(card_id=act_card_id)
        except Member.DoesNotExist:
            mem_lookup = []
        if mem_lookup:
            # Registered
            personnel = mem_lookup
            personnel.atd_check()
            print(str(personnel) + '님이 출석에 성공하였습니다.')
            return render(request, 'main/atd_check.html')
        else:
            # Not Registered
            # 일단 얘는 출석 처리 안하는걸로...
            print('Card ID : ' + act_card_id +' Not Registered!!')
            return render(request, 'main/atd_check.html')

    else:
        return render(request, 'main/atd_check.html')