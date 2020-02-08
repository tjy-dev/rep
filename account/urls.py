from django.urls import path
from . import views
from .viewsfolder import viewsapi
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<pk>/like/', views.post_like, name='post_like'),
    path('post/<pk>/comment/', views.comment_create, name='comment_create'),
    path('user/settings/edit/', views.user_edit.as_view(), name='edit_user'),
    path('user/settings/password/', views.password_change.as_view(), name='edit_password'),
    path('comment/<pk>/reply/', views.reply_comment, name='reply_comment'),

    path('search',views.search,name='search'),

    path('accounts/signup/', views.sign_up, name='signup'),
    path('accounts/done', views.user_create_temp.as_view(), name='user_create_done'),
    path('accounts/complete/<token>/', views.user_create_complete.as_view(), name='user_create_complete'),

    path('<username>',views.user_post_list,name='user_post_list'),
    path('<username>/follow',views.user_follow,name='user_follow'),

    path('api/obtain_token/', auth_views.obtain_auth_token),
    path('api/posts/delete/',viewsapi.PostDelete.as_view(),name='PostDelete'),
    path('api/posts/like/',viewsapi.PostLike.as_view(),name='PostLike'),
    path('api/user/follow/',viewsapi.UserFollow.as_view(),name='UserFollow'),
    path('api/post/new/',viewsapi.PostCreate.as_view(),name='post_create'),
]


# 画像用
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#API
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', viewsapi.UserViewSet)
router.register(r'entries', viewsapi.PostViewSet)
router.register(r'comments', viewsapi.CommentViewSet)


