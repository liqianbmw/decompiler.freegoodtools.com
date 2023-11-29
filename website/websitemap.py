from django.contrib.sitemaps import Sitemap

# from core import models


# class WebSiteSitemap(Sitemap):
#     name = 'web'
#     changefreq = 'daily'
#     limit = 50000
#
#     def items(self):
#         return models.ArticleContext.objects.order_by('title')


from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
# from core.models import ArticleContext
from django.utils import timezone

class MainViewSitemap(Sitemap):
    protocol="https"
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['home']
        # return ['home', 'contact', 'disclosure', 'terms', 'privacy', 'deals:deals', 'blog:blog']
    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()

class JavaDecompilerViewSitemap(Sitemap):
    protocol="https"
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['javaDecompilersIndex','javaDecompilers','javaDecompilerAnalyze']
    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()

class ApkDecompilerViewSitemap(Sitemap):
    protocol="https"
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['apkDecompilersIndex','apkDecompilers','apkDecompilerAnalyze']
    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()


class AboutViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 0.5
    def items(self):
        return ['about']
    def location(self, item):
        return reverse(item)
    def lastmod(self, item):
        return timezone.now()

class NewsViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 0.5
    def items(self):
        return ['newsMain']
        # return ['newsMain']
    def location(self, item):
        return reverse(item)
    def lastmod(self, item):
        return timezone.now()

class NewsDetailViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 0.5
    def items(self):
        return None;
        # return  ArticleContext.objects.all()
#         # return ['newsMain']
#     def location(self, item):
#         return reverse(item)
#     def lastmod(self, item):
#         return timezone.now()

class SchoolViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 0.5
    def items(self):
        return ['aiChooseSchool','aiAreaSchool','aiIndustySchool','aiQualitySchool','aiDetailSchool']
    def location(self, item):
        return reverse(item)
    def lastmod(self, item):
        return timezone.now()

# class ProfessionalViewSitemap(Sitemap):
#     changefreq = "never"
#     priority = 0.5
#     def items(self):
#         return ['aiChooseSchool','aiAreaSchool','aiIndustySchool','aiQualitySchool','aiDetailSchool']
#     def location(self, item):
#         return reverse(item)
#     def lastmod(self, item):
#         return timezone.now()
