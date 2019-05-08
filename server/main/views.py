from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
#from django.views.decorators.csrf import csrf_exempt

from .models import Member

import json
import datetime
import base64

decoded_id = ''

def page_not_found(request, exception):
    res = render(request, "main/404.html", {})
    res.status_code = 404
    return res

def atd_ranking(request):
    member_lists = Member.objects.order_by('-atd_checked')
    member_lists = member_lists[:5]
    return render(request, 'main/atd_ranking.html', {'member_lists': member_lists})

def full_ranking(request):
    member_lists = Member.objects.order_by('-atd_checked')
    return render(request, 'main/full_ranking.html', {'member_lists': member_lists})

#@csrf_exempt
@ensure_csrf_cookie
def atd_check(request):
    if request.method == "POST":
        act_card_id = request.POST.get('card_id')
        try:
            mem_lookup = Member.objects.get(card_id=act_card_id)
        except Member.DoesNotExist:
            mem_lookup = []
        if mem_lookup: # mem_lookup list not empty.
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

            converted_date_for_json = act_last_date.strftime('%Y-%m-%d %H:%M:%S')
            converted_date = act_last_date.strftime('%Y-%m-%d').split('-')
            year_checked = converted_date[0]
            month_checked = converted_date[1]
            day_checked = converted_date[2]

            ''' The json that we're trying to return to RBP consists four values.
                The four values are 'status', 'name', 'card_id', 'last_checked'.
                'status' is for to know which json is in certain case. For example, if we do not have the status value,
                RBP's code will be difficult to recognize whether the owner of the card checked attendance today or not.
                There are three status codes : 0, 1, 2
                0 : Already checked today
                1 : First time checking today
                2 : Unregistered
                We need card_id for the new members that are not on the Member DB for Registration Page.
            '''

            # Already Checked
            if day_checked == day_now and \
                month_checked == month_now and year_checked == year_now:

                output_str = str(personnel) + '님은 오늘 이미 출석하셨습니다.// ' + \
                str(year_checked) + '년 ' + \
                str(month_checked) + '월 ' + str(day_checked) + '일에 마지막으로 출석함'
                print(output_str)
                mem_info = {'status': 0, 'name': str(personnel), 'card_id': personnel.card_id, 'last_checked': str(converted_date_for_json)}
                mem_info_json = json.dumps(mem_info, ensure_ascii=False)

            # Not Checked Today    
            else:
                personnel.atd_check()
                output_str = str(personnel) + '님이 출석에 성공하였습니다.'
                print(output_str)
                mem_info = {'status': 1, 'name': str(personnel), 'card_id': personnel.card_id, 'last_checked': str(converted_date_for_json)}
                mem_info_json = json.dumps(mem_info, ensure_ascii=False)


            return HttpResponse(mem_info_json, content_type='application/json')
        else:
            # Not Registered
            # We do not count any of the members as checked.
            print('Card ID : ' + act_card_id +' Not Registered!!')
            mem_info = {'status': 2, 'name': '', 'card_id': act_card_id, 'last_checked': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
            mem_info_json = json.dumps(mem_info, ensure_ascii=False)

            return HttpResponse(mem_info_json, content_type='application/json')

    else:
        return render(request, 'main/atd_check.html')

@ensure_csrf_cookie
def register(request):
    global decoded_id
    if request.method == "POST":
        name = request.POST.get('name', 'NaN')
        try:
            mem_lookup = Member.objects.get(card_id=decoded_id)
        except Member.DoesNotExist:
            # ID Not Registered. Proceed Registration.
            new_member = Member(card_id=decoded_id, name=name, atd_checked=1, 
                                last_checked=timezone.now())
            new_member.save()
            decoded_id = ''
            return render(request, 'main/reg_complete.html', {})

        # ID is already registered.
        return render(request, 'main/reg_incomplete.html', {})
    else:
        # Initialize Global Variable
        decoded_id = ''
        #Get Encoded Card ID
        encoded_id = request.GET.get('id', 'N')
        if encoded_id == 'N':
            print("Can't find Card ID.")
            return render(request, 'main/404.html')
        # Decode base64
        decoded_id = base64.b64decode(encoded_id).decode('utf-8')
        
        return render(request, 'main/registration.html', {'register_id': decoded_id})
