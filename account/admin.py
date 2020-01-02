from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Post
from .models import Like
from .models import Comment
from .models import Follow

from django.contrib.auth.models import Group

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password','username','profile_pic','bio','date_of_birth')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','bio','profile_pic','date_of_birth', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('username','email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username','email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User,MyUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.unregister(Group)