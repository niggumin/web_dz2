from .models import Answer, Profile, Question, Tag
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



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
    
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 1:
            raise forms.ValidationError("Your Answer Is Empty")
        return content

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ""
        self.fields['content'].help_text = None
    




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        tags = kwargs.pop('tags', None)
        super().__init__(*args, **kwargs)
        
        if tags:
            self.fields['tags'] = forms.ModelMultipleChoiceField(
                queryset=tags,
                widget=forms.CheckboxSelectMultiple,
                required=False,
                label="Select Tags"
            )

    def save(self, commit=True):
        question = super().save(commit=False)
        question.author = self.user.profile
        
        if commit:
            question.save()
            if 'tags' in self.cleaned_data:
                question.tags.set(self.cleaned_data['tags'])
        
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