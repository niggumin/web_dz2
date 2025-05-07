import app.views
from .models import Answer, Profile, Question, Tag
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

   

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your answer...'
            })
        }
    
    # def clean_content(self):
    #     content = self.cleaned_data['content']
    #     if len(content) < 1:
    #         raise forms.ValidationError("Your Answer Is Empty")
    #     return content
    
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ""
        self.fields['content'].help_text = None
    





class QuestionForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your question title'
        }),
        error_messages={
            'required': 'Title is required'
        }
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'btn-check',
            'autocomplete': 'off'
        }),
        required=False,
        label="Tags"
    )

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']  

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        


    # def clean_content(self):
    #     content = self.cleaned_data['content']
    #     if len(content) < 1:
    #         raise forms.ValidationError("Your comment Is Empty")
    #     return content
    
    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) < 1:
    #         raise forms.ValidationError("Your title Is Empty")
    #     return title
    

    def save(self, commit=True):
        question = super().save(commit=False) 

        if self.user and hasattr(self.user, 'profile'):
            question.author = self.user.profile  

        if commit:
            question.save()
            self.save_m2m()  

        return question

    



class ProfileForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']  

   
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already taken")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].label = "Choose your profile picture"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None

    def save(self):
        user = super().save()
        user.email = self.cleaned_data['email']
        
        
        user.save()
        profile, created = Profile.objects.get_or_create(user=user)
        profile.avatar = self.cleaned_data['avatar']
        profile.save()
        
        return user