from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
#from django.views.decorators.csrf import csrf_exempt

from .models import Member

import json
import datetime

cracked_id = ''

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

            ''' The json that we're trying to return to RBP consists three values.
                The three values are 'status', 'name', 'card_id', 'last_checked'.
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
        a = request.GET.get('id', 'N')
        return render(request, 'main/atd_check.html')

@ensure_csrf_cookie
def register(request):
    global cracked_id
    if request.method == "POST":
        name = request.POST.get('name', 'NaN')
        try:
            mem_lookup = Member.objects.get(card_id=cracked_id)
        except Member.DoesNotExist:
            # ID Not Registered. Proceed Registration.
            new_member = Member(card_id=cracked_id, name=name, atd_checked=1, 
                                last_checked=timezone.now())
            new_member.save()
            cracked_id = ''
            return render(request, 'main/reg_complete.html', {})
        
        print('Already Registered')
        # ID is already registered.
        return render(request, 'main/reg_incomplete.html', {})
    else:
        # Initialize Global Variable
        cracked_id = ''
        #Get Encrypted Card ID
        card_id = request.GET.get('id', 'N')
        if card_id == 'N':
            print("Can't find Card ID.")
            return render(request, 'main/404.html')

        # Decode ascii
        splited = card_id.split('58')
        seperate = [[i[:len(i)//2], i[len(i)//2:]] for i in splited]
        list_a = []

        for a in range(len(seperate)):
            for b in range(len(seperate[a])):
                list_a.append(seperate[a][b])
        cracked_id_list = list(map(chr, list(map(int, list_a))))
        i = 1

        for c in cracked_id_list:
            if i % 2 == 1:
                cracked_id += c
                i += 1
            else:
                if i is not len(cracked_id_list):
                    cracked_id += c
                    cracked_id += ':'
                    i += 1
                else:
                    cracked_id += c
        '''
        The code above is to make the str of ascii codes into just strs as they were before.
        It will be hard to crack just the ascii codes, but we do know how long the str is, and
        there is always a ':' between every two letters.
        So, we crack the ascii strings with those two points above.
            ###Example###
            seperate(list) : [['50', '53'], ['68', '66'], ['67', '48'], ['65', '52']]
            list_a(list) : ['50', '53', '68', '66', '67', '48', '65', '52']
            cracked_id_list(list) : ['2', '5', 'D', 'B', 'C', '0', 'A', '4']
            cracked_id(string) : 25:DB:C0:A4
        '''
        return render(request, 'main/registration.html', {'register_id': cracked_id})
