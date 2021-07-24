from django.contrib.sitemaps import Sitemap
from .models import AWARE_Page


class AWARE_Pages_Sitemap(Sitemap):
    changefreq = "always"
    priority = 0.9
    limit = 1000

    def items(self):
        return AWARE_Page.objects.order_by('?')

    def lastmod(self, obj):
        return obj.time
