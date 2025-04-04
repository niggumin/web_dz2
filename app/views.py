import copy
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
questions.append({ 
                    'title': 'Question number ' + str(666),
                    'author': "Mr. Beaver",
                    'id': i,
                    'text': 'Ты уже знаешь этот #ТЕКСТ',
                    'tag1' : 'Tag5',
                    'tag2' : 'Tag1',
                    })
answers = []
for i in range(0,30):
    answers.append({ 
                    'author': "AmNyam",
                    'id': i,
                    'text': '#ТЕКСТ I really do not know what answer will be more suitable for the situation which you have described and even can not give you even a simple advice about this complex topic.' + str(i),
                    })


def pagination(collection, request):
    paginator = Paginator(collection, 5)

    try:
        pageNum = int(request.GET.get('page', 1))
        page = paginator.page(pageNum)
    except (PageNotAnInteger, EmptyPage, ValueError):
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def index(request):
    
    page = pagination(questions, request)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def hot(request):

    snoitseuq = questions[::-1]  
    
    page = pagination(snoitseuq, request)

    context = {'questions': page.object_list, 'page_obj': page}
    return render(request, 'hot.html', context=context)


def tag(request, targetTag):
    filteredQuestions = [
        q for q in questions
        if q.get('tag1') == targetTag or q.get('tag2') == targetTag
    ]
    page = pagination(filteredQuestions, request)

    context = {'questions': page.object_list, 'page_obj': page, 'targetTag': targetTag}
    return render(request, 'tag.html', context=context)


def question(request, questionId):
    
    page = pagination(answers, request)
    
    return render(request, 'question.html', context={'question': questions[questionId], 'answers': page.object_list, 'page_obj': page})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
