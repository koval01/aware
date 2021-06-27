from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from django.urls import path
from .sitemaps import AWARE_Pages_Sitemap
from . import views

sitemaps_aware_pages = {
    'aware_pages': AWARE_Pages_Sitemap,
}

urlpatterns = [
    path('', views.index, name='index_page'),
    path('status/', views.status, name='status_page'),
    path('load_more/', views.load_more, name='load_more'),
    path('bot_gateway/<str:token>/', views.bot_gateway, name='bot_gateway'),
    path('aware/', views.error_404, name='awareaddr'),
    path('aware/<str:awareid>/', views.awareview),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('footer_load', views.footer_html, name='footer_load'),
    path('opensearch.xml', views.search_config, name='search_config'),
    path('image/', views.image_proxy_view, name='imageproxy'),
    path('video/', views.video_proxy_view, name='videoproxy'),
    path('suggestions/', views.search_suggestions_get, name='search_suggestions_get'),
    path('sync_time_server/', views.sync_time_server, name='sync_time_server'),
    path('image_generate_api/', views.image_generate_api, name='image_generate_api'),
    path('aware_api/', views.aware_api, name='aware_api'),
    path('get_ad/', views.get_ad, name='get_ad'),
    path('get_banner/', views.get_banner, name='get_banner'),
    path('yt/', views.get_video_yt, name='get_video_yt'),
    path('sitemap_aware_pages.xml/', cache_page(7200)(sitemap), {'sitemaps': sitemaps_aware_pages},
         name='django.contrib.sitemaps.views.sitemap'),
]
