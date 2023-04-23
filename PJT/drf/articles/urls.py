from django.contrib import admin
from django.urls import path
from articles import views

app_name = 'articles'
urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('create/', views.create_article,),
    path('comments/', views.comment_list,)
    path('comments/<pk:comment_pk>/', views.comment_detail,),
    path('articles/<int:article_pk>/comments/', views.comme_create,),
]