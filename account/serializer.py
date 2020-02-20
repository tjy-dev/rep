# coding: utf-8

from rest_framework import serializers

from .models import User, Post,Comment

from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','profile_pic','bio')

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    published_date = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model = Post
        fields = ('id','text','picture','author','published_date',)

class CommentSerializer(serializers.ModelSerializer):
    comment_author = UserSerializer()
    created_date = serializers.DateTimeField(default=timezone.now)
    
    class Meta:
        model = Comment
        fields = ('id','comment_text','post','parent','comment_author','created_date',)