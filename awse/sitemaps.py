from django.contrib.sitemaps import Sitemap

from .models import AWSE_Page


class AWSE_Pages_Sitemap(Sitemap):
    changefreq = "always"
    priority = 0.9
    limit = 1000

    def items(self):
        return AWSE_Page.objects.order_by('?')

    def lastmod(self, obj):
        return obj.time
