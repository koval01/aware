from django.contrib.sitemaps import Sitemap
from .models import Post, Quote, Facts, Info, AWARE_Page


class PostSitemap(Sitemap):
    changefreq = "always"
    priority = 0.9
    limit = 1000

    def items(self):
        return Post.objects.order_by('?')

    def lastmod(self, obj):
        return obj.time_field


class QuoteSitemap(Sitemap):
    changefreq = "always"
    priority = 0.9
    limit = 1000

    def items(self):
        return Quote.objects.order_by('?')

    def lastmod(self, obj):
        return obj.time


class FactSitemap(Sitemap):
    changefreq = "always"
    priority = 0.9
    limit = 1000

    def items(self):
        return Facts.objects.order_by('?')

    def lastmod(self, obj):
        return obj.f_time


class AWARE_Pages_Sitemap(Sitemap):
    changefreq = "always"
    priority = 0.9
    limit = 1000

    def items(self):
        return AWARE_Page.objects.order_by('?')

    def lastmod(self, obj):
        return obj.time


class InfoSitemap(Sitemap):
    changefreq = "always"
    priority = 0.9
    limit = 1000

    def items(self):
        return Info.objects.order_by('?')

    def lastmod(self, obj):
        return obj.i_time
