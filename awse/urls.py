from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from .sitemaps import AWSE_Pages_Sitemap

sitemaps_awse_pages = {
    'awse_pages': AWSE_Pages_Sitemap,
}

urlpatterns = [
    path('', views.index, name='index_page'),
    path('load', views.load, name='load'),
    path('p/<str:aware_id>/', views.awareview, name="custom_page"),
    path('p/json/<str:aware_id>/', views.awareview_json, name="custom_page_json"),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('footer_load', views.footer_html, name='footer_load'),
    path('credits', views.credits, name='credits'),
    path('terms', views.terms, name='terms'),
    path('privacy', views.privacy, name='privacy'),
    path('opensearch.xml', views.search_config, name='search_config'),
    path('image', views.image_proxy_view, name='imageproxy'),
    path('suggestions', views.search_suggestions_get, name='search_suggestions_get'),
    path('sync_time_server', views.sync_time_server, name='sync_time_server'),
    path('get_ad', views.get_ad, name='get_ad'),
    path('get_banner', views.get_banner, name='get_banner'),
    path('whois', views.whois_data, name='whois_data'),
    path('yt', views.get_video_yt, name='get_video_yt'),
    path('sitemap_awse_pages.xml', cache_page(16000)(sitemap), {'sitemaps': sitemaps_awse_pages},
         name='django.contrib.sitemaps.views.sitemap'),
]
