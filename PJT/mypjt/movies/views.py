from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Actor, Movie, Review
from .serializers import
from rest_framework import status


# Create your views here.
def actor_list(request):
    pass

def actpr_detail(request, actor_pk):
    pass

def movie_list(request):
    pass

def movie_detail(request, movie_pk):
    pass

def review_list(request):
    pass

def review_detial(request, review_pk):
    pass

def create_review(request, movie_pk):
    pass