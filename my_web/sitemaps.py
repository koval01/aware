from django.contrib.sitemaps import Sitemap
from .models import Post, Quote, Facts, Info

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    limit = 1000

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.time_field

class QuoteSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    limit = 50000

    def items(self):
        return Quote.objects.all()

    def lastmod(self, obj):
        return obj.time

class FactSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    limit = 50000

    def items(self):
        return Facts.objects.all()

    def lastmod(self, obj):
        return obj.f_time

class InfoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    limit = 50000

    def items(self):
        return Info.objects.all()

    def lastmod(self, obj):
        return obj.i_time
