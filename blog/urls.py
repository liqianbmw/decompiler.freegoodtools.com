# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from blog import views
from django.conf.urls import url
from django.views.generic.base import TemplateView
from .feeds import AtomSiteNewsFeed, LatestPostsFeed
from django.conf.urls import  url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
# from .views import template_test


urlpatterns = [
    # path('', views.domainIndex, name='domainIndex'),
    # path('index.html', views.domainIndex, name='domainIndex'),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("", views.PostList.as_view(), name="home"),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
path('editor/', include('django_summernote.urls')),
]


