
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import traceback
import urllib
from wsgiref.util import FileWrapper
import commands
from django.template import loader
from urllib import parse
from decom import constant
from decom.models import FileItem,FileUrlPath;
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import time,base64
import os, json
from django.views.decorators.csrf import csrf_exempt
import shutil
import logging # 导入模块
from django.conf import settings
logger = logging.getLogger('django') # 使用在配置文件中定义的名为“django”的日志器


# 主页
def domainIndex(request):

    context = {};
    context['segment'] = 'index';
    # context['static'] = 'index';
    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


from django.shortcuts import get_object_or_404, render
from django.views import generic

from .forms import CommentForm
from .models import Post


class PostList(generic.ListView):

    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog/index.html"
    paginate_by = 3


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'


def post_detail(request, slug):
    template_name = "blog/post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()



    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )

