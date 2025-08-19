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
    
class AddToBookshelfForm(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput)
    author = forms.CharField(required=False, widget=forms.HiddenInput)
    cover_image = forms.URLField(required=False, widget=forms.HiddenInput)
    total_pages = forms.IntegerField(required=False, min_value=0, widget=forms.HiddenInput)


# Used to update reading progress for a saved book
class ReadingProgressForm(forms.ModelForm):
    # We’ll treat time_spent as “minutes to add” when updating
    time_spent = forms.IntegerField(min_value=0, required=False, initial=0, help_text="Minutes to add")

    class Meta:
        model = ReadingProgress
        fields = ["current_page", "time_spent", "finished"]
    