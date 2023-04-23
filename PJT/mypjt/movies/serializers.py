from rest_framework import serializers
from .models import Actor, Movie, Review

class ActorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ('id', 'title',)

class ActorDetail