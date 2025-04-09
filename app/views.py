import bleach
from .models import Question, Answer, Tag
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
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

def get_popular_tags(): 
    
    popular_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:6]
    return popular_tags


# Controllers

def index(request):
    questions = Question.objects.new()
    page = pagination(questions, request)
    popular_tags = get_popular_tags()

    context={'questions': page.object_list, 'page_obj': page, 'popular_tags': popular_tags}
    return render(request, 'index.html', context=context)


def hot(request):
    questions = Question.objects.best()
    page = pagination(questions, request)
    popular_tags = get_popular_tags()


    context = {'questions': page.object_list, 'page_obj': page, 'popular_tags': popular_tags}
    return render(request, 'hot.html', context=context)


def tag(request, targetTag):
    try:
        tag = Tag.objects.get(name=targetTag)
    except Tag.DoesNotExist:
        questions = [] 
    else:
        questions = Question.objects.filter(tags=tag)
    page = pagination(questions, request)
    popular_tags = get_popular_tags()


    context = {'questions': page.object_list, 'page_obj': page, 'targetTag': targetTag, 'popular_tags': popular_tags}
    return render(request, 'tag.html', context=context)


def question(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
        answers = question.answer_set.all()  
        page = pagination(answers, request)
        popular_tags = get_popular_tags()


        context = {'question': question, 'answers': page.object_list, 'page_obj': page, 'popular_tags': popular_tags}
        return render(request, 'question.html', context=context)
    except Http404:
        return HttpResponse("Question not found", status=404)


def login(request):
    popular_tags = get_popular_tags()

    return render(request, 'login.html', context={'popular_tags': popular_tags})


def signup(request):
    popular_tags = get_popular_tags()

    return render(request, 'signup.html', context={'popular_tags': popular_tags})


def ask(request):
    popular_tags = get_popular_tags()

    return render(request, 'ask.html', context={'popular_tags': popular_tags})


def settings(request):
    popular_tags = get_popular_tags()

    return render(request, 'settings.html', context={'popular_tags': popular_tags})
