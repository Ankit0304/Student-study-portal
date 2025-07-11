from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method == 'POST':
        
        form = NoteForm(request.POST)
        if form.is_valid():
            notes = Note(user = request.user, title = request.POST['title'], description = request.POST['description'])
            notes.save()
        messages.success(request, 'Note created successfully!')
        return redirect('notes')
    else:
        form = NoteForm()
    notes = Note.objects.filter(user=request.user)
    context = {
            'notes': notes,
            'form': form
    }
    return render(request, 'dashboard/notes.html', context)
# @login_required
def delete_note(request, pk=None):
    Note.objects.get(id=pk).delete()
    return redirect("notes")
# @login_required 
class notes_detail(generic.DetailView):
    model = Note

@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            
            homework = Homework(user=request.user, subject=request.POST['subject'], title=request.POST['title'], description=request.POST['description'], due=request.POST['due'], is_finished=finished)
            homework.save()
            messages.success(request, 'Homework created successfully!')
            return redirect('homework')
        
    else:
        form = HomeworkForm()
        
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True 
    else:
        homework_done = False
        
    context = {
        'homeworks': homework,
        'homework_done': homework_done,
        'form': form
    }
    return render(request, 'dashboard/homework.html', context)

# @login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("homework")

# @login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

# def videoSearch(query, limit=10):
#     return []

def youtube(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        text = request.POST['search']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'tumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            desc = ' '
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'result_list': result_list,
                'input': text
            }
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = searchForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/youtube.html', context)

@login_required
def ToDo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request, 'Todo created successfully!')
            return redirect('todo')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True 
    else:
        todo_done = False
    context = {
        'todos' : todo,
        'form': form,
        'todo_done': todo_done
    } 
    return render(request, 'dashboard/todo.html', context)

# @login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect("todo")

# @login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

@login_required
def books(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        text = request.POST.get('search')
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text + "&maxResults=10&key=AIzaSyA1LRGhaysfgM8brvoOpGDKfmXSVAP0eGo"
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle', ''),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count' : answer['items'][i]['volumeInfo'].get('pageCount', 'N/A'),
                'category': answer['items'][i]['volumeInfo'].get('categories', ['N/A'])[0],
                'rating': answer['items'][i]['volumeInfo'].get('averageRating', 'N/A'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                'preview' : answer['items'][i]['volumeInfo'].get('previewLink', ''),
                
            }
            result_list.append(result_dict)
            context = {
                'form': form,
                'result_list': result_list,
                
            }
        return render(request, 'dashboard/books.html', context)
    else:
        form = searchForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/books.html', context)

@login_required
def dictionary(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        text = request.POST.get('search')
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + text
        r = requests.get(url)
        
        try:
            answer = r.json()
            phonetics = answer[0].get('phonetics', [{}])[0].get('text', 'N/A')
            audio = answer[0].get('phonetics', [{}])[0].get('audio', '')
            definition = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('definition', 'N/A')
            example = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('example', 'No example available')
            synonyms = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('synonyms', [])

            context = {
                'form' : form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio, 
                'definition': definition,
                'example': example,
                'synonyms': synonyms,
            }
        except:
            context = {
                'form': form,
                'input': '',
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = searchForm()
        context = {
            'form': form,
        }
    
    return render(request, 'dashboard/dictionary.html', context)

@login_required
def wiki(request):
    if request.method == 'POST':
        text = request.POST['search']
        form = searchForm(request.POST)
        search = wikipedia.page(text,auto_suggest=False)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary,
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = searchForm()
        context = {
            'form': form,
        }
    return render(request, 'dashboard/wiki.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:     
        form = RegisterationForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/register.html', context)

@login_required
def profile(request):
    homework = Homework.objects.filter(is_finished=False, user=request.user)
    todo = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'homework': homework,
        'todo': todo,
        'homework_done': homework_done,
        'todo_done': todo_done, 
    }
    
    return render(request, 'dashboard/profile.html', context)
