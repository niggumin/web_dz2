import copy
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

questions = []
for i in range(0,30):
    questions.append({ 
                    'title': 'Question number ' + str(i),
                    'author': "Krasnoglazik",
                    'id': i,
                    'text': '#ТЕКСТ ' + str(i),
                    'tag1' : 'Tag3',
                    'tag2' : 'Tag2',
                    })

answers = []
for i in range(0,30):
    answers.append({ 
                    'author': "AmNyam",
                    'id': i,
                    'text': '#ТЕКСТ I really do not know what answer will be more suitable for the situation which you have described and even can not give you even a simple advice about this complex topic.' + str(i),
                    })

def index(request):
    return render(request, 'index.html', context={'questions': questions})

def hot(request):
    snoitseuq = reversed(copy.deepcopy(questions))
    return render(request, 'hot.html', context={'questions': snoitseuq})

def tag(request, targetTag):
    
    return render(request, 'tag.html', context={'questions': questions, 'targetTag': targetTag})

def question(request, questionId):
   
    if questionId == -1:
        return HttpResponse("WRONG ID")
    
    return render(request, 'question.html', context={'question': questions[questionId], 'answers': answers})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')
