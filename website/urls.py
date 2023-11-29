# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, re_path,include  # add this
from authentication.views import ChangeLanguageView
from website.websitemap import JavaDecompilerViewSitemap,ApkDecompilerViewSitemap,AboutViewSitemap,NewsViewSitemap,SchoolViewSitemap,NewsDetailViewSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from blog.sitemaps import PostSitemap
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from django.views.static import serve

sitemaps = {
    'java_decompiler': JavaDecompilerViewSitemap,
    'apk_decompiler': ApkDecompilerViewSitemap,
    "posts": PostSitemap,
}

# urlpatterns = [
#     path('i18n/', include('django.conf.urls.i18n')),
# ]
# urlpatterns += i18n_patterns [
urlpatterns =  [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("decom.urls")),           # UI Kits Html decompiler
    path("", include("blog.urls")),           # UI Kits Html decompiler

    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),
    path('accounts/', include('authentication.urls')),


    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('pv/', TemplateView.as_view(template_name='pv.txt')),
    path('pv.txt', TemplateView.as_view(template_name="pv.txt", content_type="text/plain"), name="pv"),
    re_path('BingSiteAuth.xml',TemplateView.as_view(template_name="BingSiteAuth.xml", content_type="text/plain"), name="BingSiteAuth"),
    re_path('ads.txt',TemplateView.as_view(template_name="ads.txt", content_type="text/plain"), name="ads"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),] + urlpatterns

