from rest_framework import serializers
from .models import Article, Comment


class CommentListSerializer(serializers.ModelField):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article',)


class ArticleListSerializer(serializers.ModelSerializer):
    # comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comment_set = CommentListSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    class Meta:
        model = Article
        fields = '__all__'

    # fields 명만 바꾸기
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = rep.pop('comment_set', [])
        return rep