from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<pk>/like/', views.post_like, name='post_like'),

    
    path('user/settings/edit/', views.user_edit.as_view(), name='edit_user'),
    path('user/settings/password/', views.password_change.as_view(), name='edit_password'),

    path('accounts/signup/', views.sign_up, name='signup'),
    path('accounts/done', views.user_create_temp.as_view(), name='user_create_done'),
    path('accounts/complete/<token>/', views.user_create_complete.as_view(), name='user_create_complete'),

    path('<username>',views.user_post_list,name='user_post_list'),
    path('<username>/follow',views.user_follow,name='user_follow'),
    #path('accounts/signup/', views.SignUp.as_view(), name='signup')
]


# 画像用
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)