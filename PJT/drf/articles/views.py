from django.shortcuts import render
from .models import Article, Comment
from .serializers import ArticleListSerializer, CommentListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def article_list(request):
    articles = Article.objects.all()
    serializer = ArticleListSerializer(articles, many = True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleListSerializer(article)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ArticleListSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['POST'])
def create_article(request):
    serializer = ArticleListSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentListSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'GET':
        serializer = CommentListSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentListSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def comment_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    serializer = CommentListSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    