from django.contrib import admin
from django.urls import path
from movies import views

app_name = 'movies'
urlpatterns = [
    path('actor_list/', views.actor_list, name="actor_list"),
    path('actor_list/<int:actor_pk>/', views.actor_detail, name="actor_detail"),
    path('movie_list/', views.movie_list, name="movie_list"),
    path('movie_list/<int:movie_pk>/', views.movie_detail, name="movie_detail"),
    path('review_list/', views.review_list, name="review_list"),
    path('review_list/<int:review_pk>/', views.review_detail, name="review_detail"),
    path('<int:movie_pk>/create_review/', views.create_review, name="create_review"),
]