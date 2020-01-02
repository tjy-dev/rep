from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import User
from .models import Follow
from .models import Like
from .models import Comment
from django.db.models import Q
from .forms import PostForm
from .forms import CommentForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http.response import JsonResponse

import os

def user_post_list(request,username):
    person = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=person,published_date__lte=timezone.now()).order_by('-published_date')
    is_follow = Follow.objects.filter(follower=request.user).filter(following=person).count()
    if person == request.user:
        return render(request, 'blog/user_detail_with_list.html',{'posts': posts,})
    else:
        return render(request, 'blog/user_post_list.html', {'posts': posts,'person':person,'is_follow':is_follow})

def post_list(request):
    #following = Follow.objects.filter(follower=request.user)
    #a = []
    #for f in following:
    #    a.append(f.following)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')#.filter(Q(author__in=a) | Q(author=request.user))
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    abc = post.author.id
    abcd = request.user.id
    is_like = Like.objects.filter(user=request.user).filter(post=post).count()
    comment = Comment.objects.filter(post=post)
    return render(request, 'blog/post_detail.html', {'post': post,'abc': abc,'abcd':abcd,'is_like':is_like,'comment':comment})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        if request.method == "POST":
            form = PostForm(request.POST,request.FILES, instance=post,)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return redirect('post_detail', pk=post.pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect('post_list')
    else:
        return redirect('post_detail', pk=post.pk)

###########################################################################

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    is_like = Like.objects.filter(user=request.user).filter(post=post).count()
    if is_like == 0:
        like = Like()
        like.user = request.user
        like.post = post
        like.published_date = timezone.now()
        like.save()
        is_like = 1
    else:
        like = Like.objects.filter(user=request.user).filter(post=post)
        like.delete()
        is_like = 0
    hoge = {
        'like': is_like,
        'text': "",
    }
    return JsonResponse(hoge)

@login_required
def user_follow(request,username):
    person = get_object_or_404(User, username=username)
    is_follow = Follow.objects.filter(follower=request.user).filter(following=person).count()
    if person == request.user:
        return reverse_lazy('post_list')#error
    else:
        if is_follow == 0:
            follow = Follow()
            follow.follower = request.user
            follow.following = person
            follow.created_date = timezone.now()
            follow.save()
            is_follow = 1
        else:
            follow = Follow.objects.filter(follower=request.user).filter(following=person)
            follow.delete()
            is_follow = 0
        hoge = {
            'like': is_follow,
            'text': "",
        }
        return JsonResponse(hoge)

@login_required
def comment_create(request, pk):
    """記事へのコメント作成"""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST,)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.comment_author = request.user
            comment.created_date = timezone.now()
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm(instance=post)
    return render(request, 'blog/comment_create.html', {'form':form,'post':post})

###########################################################################


# sign u_p
from .forms import SignUpForm
from django.views.generic.edit import CreateView

#Not using this view
class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html" 

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        login(self.request, user) # 認証
        self.object = user
        return redirect('post_list')

from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            domain = current_site.domain
            context = {
                'protocol': request.scheme,
                'domain': domain,
                'token': dumps(user.pk),
                'user': user,
            }
            
            subject = render_to_string('registration/subject.txt', context)
            message = render_to_string('registration/message.txt', context)
            
            user.email_user(subject, message)
            #return redirect('user_create_done')
            return render(request,'registration/user_create_done.html')
    else:
        form = SignUpForm()
    return render(request,'registration/signup.html', {'form': form})

from django.views import generic
class user_create_temp(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'registration/user_create_done.html'

from django.conf import settings
from django.http import Http404, HttpResponseBadRequest
class user_create_complete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'registration/user_create_done.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 15*60)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                    return super().get(request, **kwargs)

        return redirect('post_list')


#########################################################################


from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_authenticated

class user_edit(OnlyYouMixin,UpdateView):
    model = User
    template_name = 'registration/edituser.html'
    fields = ['username','email','bio','profile_pic']
    success_url = reverse_lazy('post_list')

    def get_object(self):
        # ログイン中のユーザーで検索することを明示する
        return self.request.user


from django.contrib.auth.views import PasswordChangeView
from .forms import MyPasswordChangeForm

class password_change(OnlyYouMixin,PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('post_list')
    template_name = 'registration/edit_password.html'