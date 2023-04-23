from rest_framework import serializers
from .models import Article, Comment

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class CommentListSerializer(serializers.ModelField):
    class Meta:
        model = Comment
        fields = '__all__'