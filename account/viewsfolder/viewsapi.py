
from django.utils import timezone
from ..models import Post,User,Follow,Like,Comment
from django.db.models import Q
from ..forms import PostForm,CommentForm
from django.shortcuts import get_object_or_404

import django_filters
from rest_framework import viewsets, filters
from ..serializer import UserSerializer, PostSerializer,CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import BasePermission 
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == 1

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('username',)
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated,IsAdmin,)   

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.order_by('-published_date')
    serializer_class = PostSerializer
    filter_fields = ('author', 'text',)
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        #if user.is_superuser:
           #return Post.objects.order_by('-published_date')
        if user.is_authenticated:
            following = Follow.objects.filter(follower=self.request.user)
            a = []
            for f in following:
                a.append(f.following)
            snippets = Post.objects.filter(Q(author__in=a) | Q(author=self.request.user)).order_by('-published_date')
            return snippets

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(PostViewSet, self).dispatch(*args, **kwargs)

class SearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.order_by('-published_date')
    serializer_class = PostSerializer
    filter_fields = ('author', 'text',)
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            q = self.request.GET.get(key="q", default="")
            snippets = Post.objects.text__in(q).order_by('-published_date')
            return snippets

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(PostViewSet, self).dispatch(*args, **kwargs)

class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.order_by('-created_date')
    serializer_class = CommentSerializer
    filter_fields = ('comment_author', 'parent','post',)
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Comment.objects.order_by('-created_date')


from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers


class PostDelete(APIView):
    def get(self, request, format=None):
        #usernames = [post.text for post in Post.objects.all()[0:3]]#1-3個め表示
        following = Follow.objects.filter(follower=request.user)
        a = []
        for f in following:
            a.append(f.following)
        snippets = Post.objects.filter(Q(author__in=a) | Q(author=request.user))
        #serializer = PostSerializer(snippets, many=True)
        return Response({"detail":"No permission"})#serializer.data)

    def post(self, request):
        data = request.data
        delete = data["delete"]
        pk = data["id"]
        usern = data["username"]
        post = get_object_or_404(Post, pk=pk)

        if usern == request.user.username:
            if delete == "true":
                if request.user == post.author:
                    post.delete()
                    return Response({'delete': 'True'})
                else:
                    return Response({'detail': 'No permisson'})
        else:
            return Response({'detail': 'No permisson'})

class PostLike(APIView):
    def get(self, request, format=None):
        return Response({"detail":"No permission"})

    def post(self, request):
        data = request.data
        pk = data["id"]
        usern = data["username"]
        wlike = data["like"]
        post = get_object_or_404(Post, pk=pk)

        if usern == request.user.username:
            if wlike == "true":
                is_like = Like.objects.filter(user=request.user).filter(post=post).count()
                if is_like == 0:
                    like = Like()
                    like.user = request.user
                    like.post = post
                    like.published_date = timezone.now()
                    like.save()
                    return Response({'like': 'True'})
                else:
                    like = Like.objects.filter(user=request.user).filter(post=post)
                    like.delete()
                    return Response({'like': 'False'})
        else:
            return Response({'detail': 'No permisson'})

class UserFollow(APIView):
    def get(self, request, format=None):
        return Response({"detail":"No permission"})

    def post(self, request):
        data = request.data
        pk = data["id"]
        usern = data["username"]
        wlike = data["follow"]
        user = get_object_or_404(User, pk=pk)

        if usern == request.user.username:
            if wlike == "true":
                is_follow = Follow.objects.filter(follower=request.user).filter(following=user).count()
                if is_follow == 0:
                    follow = Follow()
                    follow.follower = request.user
                    follow.following = user
                    follow.published_date = timezone.now()
                    follow.save()
                    return Response({'Follow': 'True'})
                else:
                    follow = Follow.objects.filter(follower=request.user).filter(following=user)
                    follow.delete()
                    return Response({'Follow': 'False'})
            else:
                is_follow = Follow.objects.filter(follower=request.user).filter(following=user).count()
                if is_follow == 0:
                    return Response({'Following': 'False'})
                else:
                    return Response({'Following': 'True'})
        else:
            return Response({'detail': 'No permisson'})

class PostCreate(APIView):
    def post(self, request):
        data = request.data
        text = data["text"]
        pic = data["picture"]
        aut = data["author"]
        if aut == request.user.username:
            request.user.password
            post = Post()
            post.text = text
            post.author = request.user
            post.created_date = timezone.now()
            post.picture = pic
            post.save()
            return Response({'detail': 'Success'})
        return Response({'detail': 'No permisson'})

class Post_like_api(APIView):
    def get(self, request, format=None):
        #wd = request.GET.get(key="delete", default="false")
        return Response({'sucsess':'True'})
    def post(self, request):
        return Response({'sucsess':'True'})

