from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

from .models import Member

import datetime


def atd_ranking(request):
    member_lists = Member.objects.order_by('-atd_checked')
    member_lists = member_lists[:5]
    return render(request, 'main/atd_ranking.html', {'member_lists': member_lists})

def full_ranking(request):
    member_lists = Member.objects.order_by('-atd_checked')
    return render(request, 'main/full_ranking.html', {'member_lists': member_lists})

@ensure_csrf_cookie
# @csrf_exempt
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
            last_date = personnel.last_checked
            KST = datetime.timedelta(hours=9)
            act_last_date = last_date + KST
            
            # Duplicated Attendace Checker
            now = datetime.datetime.now().strftime('%Y-%m-%d').split('-')
            year_now = now[0]
            month_now = now[1]
            day_now = now[2]

            converted_date = act_last_date.strftime('%Y-%m-%d').split('-')
            year_checked = converted_date[0]
            month_checked = converted_date[1]
            day_checked = converted_date[2]

            # Already Checked
            if day_checked == day_now and \
                month_checked == month_now and year_checked == year_now:

                print(str(personnel) + '님은 오늘 이미 출석하셨습니다.// ' +
                str(year_checked) + '년 ' + 
                str(month_checked) + '월 ' + str(day_checked) + '일에 마지막으로 출석함')

            # Not Checked Today    
            else:
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