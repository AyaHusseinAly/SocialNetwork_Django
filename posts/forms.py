from django import forms
from .models import Post
from .models import Comment
from .models import BadWord
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content",)

# def clean_content(self):
#         content = self.cleaned_data.get('content')
#         bad_words = BadWord.objects.all()
#         results = list(map(lambda x: x.word, bad_words))
        
#         bad_words_list = []
#         for word in results:
#             if word in content:
#                 bad_words_list.append(word)
#         bad_words_string = ', '.join(bad_words_list)
        
#         if len(bad_words_list) > 0:
#             raise ValidationError("The content of a post contain bad words " + bad_words_string)
#         return content

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

# def clean_content(self):
#         content = self.cleaned_data.get('content')
#         bad_words = BadWord.objects.all()
#         results = list(map(lambda x: x.word, bad_words))
        
#         bad_words_list = []
#         for word in results:
#             if word in content:
#                 bad_words_list.append(word)
#         bad_words_string = ', '.join(bad_words_list)
        
#         if len(bad_words_list) > 0:
#             raise ValidationError("The content of a comment contain bad words " + bad_words_string)
#         return content        