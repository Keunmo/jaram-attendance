from django import forms
from .models import Member

class AtdForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('card_id',)