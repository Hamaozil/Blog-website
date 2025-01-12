#this is for connecting models with forms for better action taken
from django import forms
from .models import LogInUsers , UserBlogs


class LogInForm(forms.ModelForm): # create a from that inherits from ModelForm
    class Meta:
        model = LogInUsers
        fields = ['email', 'password'] # Only email and password fields are needed
        widgets = {
            'password': forms.PasswordInput(),
            #'username': forms.TextInput(),
            'email': forms.EmailInput(),
        } # validate password and email



class BlogsForm(forms.ModelForm): # create a from that inherits from ModelForm
    class Meta:
        model = UserBlogs
        fields = ['title', 'description','img']
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
        }

