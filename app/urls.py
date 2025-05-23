"""
URL configuration for askme_vavilov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('tag/<str:targetTag>', views.tag, name='tag'),
    path('question/<int:question_id>', views.question, name='question'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
    path('search_tags/', views.search_tags, name='search_tags'),

    path('test', views.profile_list, name='profile_list'),
    
]
