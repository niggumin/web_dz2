from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.

questions = []
for i in range(1,30):
    questions.append({ 
                    'title': 'title' + str(i),
                    'author': "Krasnoglazik",
                    'id': i,
                    'text': 'text' + str(i),
                    'tag1' : 'Tag №3',
                    'tag2' : 'Tag №2',
                    })

def index(request):
    return render(request, 'index.html', context={'questions': questions})

def hot(request):
    return render(request, 'hot.html', context={'questions': questions})

def tag(request):
    return render(request, 'tag.html', context={'questions': questions})

def question(request):
    return render(request, 'question.html', context={'questions': questions})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')
