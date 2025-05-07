
from django.urls import reverse, reverse_lazy

from app.forms import AnswerForm, LoginForm, ProfileForm, QuestionForm
from .models import Profile, Question, Answer, Tag
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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




def search_tags(request):
    query = request.GET.get('query', '')
    if query:
        tags = Tag.objects.filter(name__icontains=query)[:5]
        results = [{'name': tag.name, 'id': tag.id} for tag in tags]
    else:
        results = []
    return JsonResponse({'results': results})




def question(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
        answers = question.answer_set.all()  
        page = pagination(answers, request)
        popular_tags = get_popular_tags()

        form = AnswerForm()
        if request.method == "POST":
            form = AnswerForm(request.POST)
            if form.is_valid():
                if request.user.is_authenticated:  
                    answer = form.save(commit=False)
                    answer.question = question
                    answer.author = request.user.profile
                    answer.save()
                    return redirect('question', question_id=question.id)
                else:
                    return redirect(reverse('login'))

        context = {'question': question, 'answers': page.object_list, 'page_obj': page, 'popular_tags': popular_tags, 'form': form}
        return render(request, 'question.html', context=context)
    except Http404:
        return HttpResponse("Question not found", status=404)



def login(request):
    popular_tags = get_popular_tags()

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            print(user)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                form.add_error(field=None ,error="Wrong user name or password")

    
    return render(request, 'login.html', context={'popular_tags': popular_tags, 'form': form})



def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))



def signup(request):
    popular_tags = get_popular_tags()
    
    form = ProfileForm()
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()        
            auth.login(request, user)
            return redirect(reverse('index'))
        

    return render(request, 'signup.html', context={'popular_tags': popular_tags, 'form': form})




@login_required(login_url=reverse_lazy("login"))
def ask(request):
    popular_tags = get_popular_tags()
    all_tags = Tag.objects.all()  
    tag_page = pagination(all_tags, request)

    if request.method == 'POST':
        form = QuestionForm(request.POST, user=request.user) 
        if form.is_valid():
            question = form.save()  
            return redirect('question', question_id=question.id)

    else:
        form = QuestionForm(user=request.user)
    return render(request, 'ask.html', context={'popular_tags': popular_tags, 'form': form, 'tag_page': tag_page})




@login_required(login_url=reverse_lazy("login"))
def settings(request):
    popular_tags = get_popular_tags()

    return render(request, 'settings.html', context={'popular_tags': popular_tags})




def profile_list(request):
    profiles = Profile.objects.select_related('user').order_by('-created_at')
    return render(request, 'testProf.html', {'profiles': profiles})