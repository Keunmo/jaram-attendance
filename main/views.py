from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

from .models import Member
from .forms import AtdForm


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
        form = AtdForm(request.POST)
        if form.is_valid():
            form.save()
            form_copy = request.POST.copy()
            act_card_id = form_copy.get('card_id')
            atdchk_member = Member.objects.get(card_id=act_card_id)
            atdchk_member.atd_check()
            print(atdchk_member)
            print(form)
            return "Attendance Checked!"
        else:
            print("ㅅㅂ")
            return form

    else:
        return render(request, 'main/atd_check.html')