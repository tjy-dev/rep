from django import forms
from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text','picture',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)
        
# sign up 用
from .models import User
from django.contrib.auth.forms import UserCreationForm
BIRTH_YEAR_CHOICES = range(1930,2009)
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','profile_pic','date_of_birth','bio')

        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES)
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
        


#password change
from django.contrib.auth.forms import PasswordChangeForm
class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'