# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from decom import views
from django.conf.urls import url
from django.views.generic.base import TemplateView




urlpatterns = [
    # The home page
    # path('', views.index, name='home'),

    #java主页面
    path('java_Decompilers_index.html', views.javaDecompilersIndex, name='javaDecompilersIndex'),
    #初次登录java反编译主页面
    path('java_Decompilers.html', views.javaDecompilers, name='javaDecompilers'),
    #上传文件后，显示的主页面
    path('java_decompiler_analyze.html', views.javaDecompilerAnalyze, name='javaDecompilerAnalyze'),
    #java反编译显示文件结构页面
    path('java_decompiler_folder.html', views.javaDecompilerFolder, name='javaDecompilerFolder'),
    #文件详细页面，分为java文件和jpg文件两种形式
    path('java_decompile_detail.html', views.javaDecompileFileDetail, name='decompileFileDetail'),

    # apk主页面
    path('apk_Decompilers_index.html', views.apkDecompilersIndex, name='apkDecompilersIndex'),
    # 初次登录apk反编译主页面
    path('apk_Decompilers.html', views.apkDecompilers, name='apkDecompilers'),
    # 上传文件后，显示的主页面
    path('apk_decompiler_analyze.html', views.apkDecompilerAnalyze, name='apkDecompilerAnalyze'),
    # apk反编译显示文件结构页面
    path('apk_decompiler_folder.html', views.apkDecompilerFolder, name='apkDecompilerFolder'),
    # 文件详细页面，分为apk文件和jpg文件两种形式
    path('apk_decompile_detail.html', views.apkDecompileFileDetail, name='decompileFileDetail'),




    # 文件详细页面，分为java文件和jpg文件两种形式
    # path('decompile_down_tools.html', views.decompileDownTools, name='decompileDownTools'),


    path('download_zip.html', views.downloadZip, name='downloadZip'),


    path('download_jad.html', views.downloadJadPage, name='downloadJadPage'),


]
