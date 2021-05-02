from django import forms
from .models import Message
from django.core.exceptions import ValidationError

class MsgForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("text",)



