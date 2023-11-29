from datetime import timedelta

from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class UserCacheMixin:
    user_cache = None


class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if settings.USE_REMEMBER_ME:
        #     self.fields['remember_me'] = forms.BooleanField(label=_('Remember me'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('You entered an invalid password.'))

        return password
#
#
class SignInViaUsernameForm(SignIn):
    username = forms.CharField(label=_('Username'))

    @property
    def field_order(self):
        # if settings.USE_REMEMBER_ME:
        #     return ['username', 'password', 'remember_me']
        return ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError(_('You entered an invalid username.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return username

class SignInViaEmailOrUsernameForm(SignIn):
    email_or_username = forms.CharField(label=_('Email or Username'))

    @property
    def field_order(self):
        # if settings.USE_REMEMBER_ME:
        #     return ['email_or_username', 'password', 'remember_me']
        return ['email_or_username', 'password']

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address or username.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return email_or_username

class ArticleContextForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    _id = forms.CharField(label='文章id',max_length=50);#文章id(id)
    totallevel = forms.CharField(label='total显示',max_length=50);#total显示(totalLevel)
    typeid = forms.CharField(label='所属版块id',max_length=50);#所属版块id(typeid)  typeid=1 资讯内容   typeid=2 政策动态 typeid=3 各地政策汇总
    modelid = forms.CharField(label='所属模型id',max_length=50);#所属模型id(modelid)
    arcrank = forms.CharField(label='排序',max_length=50);#排序(arcrank)
    click = forms.CharField(label='点击',max_length=50);#点击(click)
    title = forms.CharField(label='文章标题',max_length=50);#文章标题(title)
    shortitle = forms.CharField(label='文章短标题',max_length=50);#文章短标题(shortitle)
    writer = forms.CharField(label='作者',max_length=50);#作者(writer)
    resource = forms.CharField(label='来源',max_length=50);#来源(resource)
    updatedate = forms.CharField(label='更新时间',max_length=50);#更新时间(updatedate)
    sendate = forms.CharField(label='发表时间',max_length=50);#发表时间(sendate)
    keywords = forms.CharField(label='关键词',max_length=50);#关键词(keywords)
    content = forms.CharField(label='文章正文',max_length=50);#文章正文(content)
    contentimg1 = forms.CharField(label='正文图片',max_length=50);#正文图片(contentimg1)
    titleimg1 = forms.CharField(label='标题图片',max_length=50);#标题图片(titleimg1)
