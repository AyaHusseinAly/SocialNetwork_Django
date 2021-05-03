from django import forms
from .models import Post
from .models import Comment
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content",)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = "__all__"
        fields = ("content",)
        # fields = ("owner","content",)
        # fields = "__all__"
        # widgets={
        #     'owner':forms.TextInput(attrs={'value':'','id':'eldr'})
        # }