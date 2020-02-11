from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager

from stdimage.models import StdImageField #サイズ指定画像

from django.conf import settings

import uuid 
import os 
from PIL import Image


def get_image_path(instance, filename):
    prefix = 'images/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension
    #カスタマイズした画像パスを取得する
    #:param instance: インスタンス (models.Model)
    #:param filename: 元ファイル名
    #:return: カスタマイズしたファイル名を含む画像パス

def getThumbnail(str):
    proImage = str
    ext = ""
    if proImage != "":
        while True:
            if proImage[-1] == ".":
                break
            else:
                ext = proImage[-1] + ext
                proImage = proImage[:-1]
        proImage = proImage + "thumbnail."
        proImage = proImage + ext
    return proImage

def delete_previous_profile_picture(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        # 保存前のファイル名を取得
        result = User.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None
        super(User, self).save()
        
        # 関数実行
        result = function(*args, **kwargs)

        result2 = User.objects.filter(pk=self.pk)
        newpic = result2[0] if len(result2) else None
        # 保存前のファイルがあったら削除
        if previous:
            if previous.profile_pic.name:
                if newpic:
                    if newpic.profile_pic.name:
                        if previous.profile_pic.name != newpic.profile_pic.name:
                            os.remove(settings.MEDIA_ROOT + '/' + previous.profile_pic.name)
                            os.remove(settings.MEDIA_ROOT + '/' + getThumbnail(previous.profile_pic.name))
                            return result
                else:
                    os.remove(settings.MEDIA_ROOT + '/' + previous.profile_pic.name)
                    os.remove(settings.MEDIA_ROOT + '/' + getThumbnail(previous.profile_pic.name))
                    return result
    return wrapper

def delete_previous_file(function):
    #不要となる古いファイルを削除する為のデコレータ実装.
    #:param function: メイン関数
    #:return: wrapper
    def wrapper(*args, **kwargs):
        #Wrapper 関数.
        #param args: 任意の引数
        #param kwargs: 任意のキーワード引数
        #return: メイン関数実行結果
        self = args[0]

        # 保存前のファイル名を取得
        result = Post.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None
        super(Post, self).save()
        
        # 関数実行
        result = function(*args, **kwargs)

        result2 = Post.objects.filter(pk=self.pk)
        newpic = result2[0] if len(result2) else None

        # 画像のリサイズを行う
        if newpic:
            if newpic.picture.name:
                path = settings.MEDIA_ROOT + '/' + newpic.picture.name
                
                img = Image.open(path)

                h, w = img.size
                length = h + w
                quality = 1400 / length
                img_resize = img.resize((int(img.width * quality), int(img.height * quality)))
                title, ext = os.path.splitext(path)
                img_resize.save(title + '.thumbnail' + ext)

                length = h + w
                quality = 3500 / length
                img_resize = img.resize((int(img.width * quality), int(img.height * quality)))
                img_resize.save(path)

        # 保存前のファイルがあったら削除
        if previous:
            if previous.picture.name:
                if newpic:
                    if newpic.picture.name:
                        if previous.picture.name != newpic.picture.name:
                            os.remove(settings.MEDIA_ROOT + '/' + previous.picture.name)
                            os.remove(settings.MEDIA_ROOT + '/' + getThumbnail(previous.picture.name))
                            return result
                else:
                    os.remove(settings.MEDIA_ROOT + '/' + previous.picture.name)
                    os.remove(settings.MEDIA_ROOT + '/' + getThumbnail(previous.picture.name))
                    return result
    return wrapper

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(unique=False)
    published_date = models.DateTimeField(blank=True, null=True,unique=False)
    #picture = models.ImageField(upload_to=get_image_path, null=True,blank=True,unique=False)
    picture = StdImageField(upload_to=get_image_path,null=True,blank=True,variations={
        'thumbnail':(350,300,True),
    })
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    @delete_previous_file
    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        super(Post, self).save(*args, **kwargs)
        
    @delete_previous_file
    def delete(self, *args, **kwargs):
        super(Post, self).delete(*args, **kwargs)
        
    #def __str__(self):
    #    return self.title

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    created_date = models.DateTimeField(blank=True,null=True)

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='follower',null=True)
    following = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='following',null=True)
    created_date = models.DateTimeField(blank=True,null=True)

class Comment(models.Model):
    comment_text = models.TextField('コメント内容',max_length=250)
    post = models.ForeignKey(Post, verbose_name='対象記事', on_delete=models.CASCADE,null=True)
    parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    created_date = models.DateTimeField(blank=True,null=True)

from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _  
  
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, profile_pic, bio, date_of_birth, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username,profile_pic=profile_pic,bio=bio, date_of_birth=date_of_birth, email=email,password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, profile_pic=None,bio=None,date_of_birth=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, profile_pic,bio, date_of_birth, email, password, **extra_fields)

    def create_superuser(self, username, profile_pic, bio, date_of_birth, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username=username, profile_pic=profile_pic, bio=bio, date_of_birth=date_of_birth, email=email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()
    
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    #ここに追加する
    profile_pic = StdImageField(_('profile picture'),upload_to=get_image_path,null=True,blank=True,variations={
        'thumbnail':(40,40,True),
    })

    bio = models.TextField(_('bio'),max_length=250,null=True,blank=True)
    date_of_birth = models.DateField(_('date of birth'),null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=False,unique=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','profile_pic','bio','date_of_birth',]#####追加する(コンソールよう)

    @delete_previous_profile_picture
    def save(self, *args, **kwargs):
        print("hello")
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        #abstract = True # ここを削除しないといけないことを忘れない！！！！！！！！！！
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
