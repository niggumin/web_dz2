from .models import Question, Answer, Tag
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.



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
    questions = Question.objects.all()
    page = pagination(questions, request)

    context={'questions': page.object_list, 'page_obj': page}
    return render(request, 'index.html', context=context)


def hot(request):
    questions = Question.objects.best()
    page = pagination(questions, request)

    context = {'questions': page.object_list, 'page_obj': page}
    return render(request, 'hot.html', context=context)


def tag(request, targetTag):
    try:
        tag = Tag.objects.get(name=targetTag)
    except Tag.DoesNotExist:
        questions = [] 
    else:
        questions = Question.objects.filter(tags=tag)
    page = pagination(questions, request)

    context = {'questions': page.object_list, 'page_obj': page, 'targetTag': targetTag}
    return render(request, 'tag.html', context=context)


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.under_question(question)
    page = pagination(answers, request)
    
    context={'question': question, 'answers': page.object_list, 'page_obj': page}
    return render(request, 'question.html', context=context)


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
