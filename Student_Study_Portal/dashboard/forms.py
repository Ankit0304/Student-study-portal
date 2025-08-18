from django import forms
from .models import *
from django.contrib.auth.forms import User, UserCreationForm
class NoteForm(forms.ModelForm):
    class Meta :
        model = Note
        fields = ['title', 'description', 'attachment']
        
class DateInput(forms.DateInput):
    input_type = 'date'
            
class HomeworkForm(forms.ModelForm):
    class Meta :
        model = Homework
        widgets = {
            'due' : DateInput(),
        }
        fields = ['subject', 'title', 'description', 'due', 'is_finished']
        
class searchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Search...'}))
    
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']
        
class RegisterationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    