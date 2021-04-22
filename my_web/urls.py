from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from django.urls import path
from .sitemaps import AWARE_Pages_Sitemap, QuoteSitemap, FactSitemap
from . import views

sitemaps_aware_pages = {
    'aware_pages': AWARE_Pages_Sitemap,
}

sitemaps_quotes = {
    'quotes': QuoteSitemap,
}

sitemaps_facts = {
    'facts': FactSitemap,
}

urlpatterns = [
    path('', views.index, name='index_page'),
    path('info/', views.info, name='info_page'),
    path('status', views.status, name='status_page'),
    path('bot', views.botpage, name='bot_page'),
    path('load_more', views.load_more, name='load_more'),
    path('quote/', views.error_404, name='quoteaddr'),
    path('fact/', views.error_404, name='factaddr'),
    path('aware/', views.error_404, name='awareaddr'),
    path('news/', views.news_feed, name='news_page'),
    path('quote/<str:quoteid>/', views.quoteview),
    path('fact/<str:factid>/', views.factview),
    path('aware/<str:awareid>/', views.awareview),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('image/', views.image_proxy_view, name='imageproxy'),
    path('suggestions', views.search_suggestions_get, name='search_suggestions_get'),
    path('image_generate_api/', views.image_generate_api, name='image_generate_api'),
    path('aware_api/', views.aware_api, name='aware_api'),
    path('sitemap_aware_pages.xml', cache_page(7200)(sitemap), {'sitemaps': sitemaps_aware_pages},
         name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap_quotes.xml', cache_page(7200)(sitemap), {'sitemaps': sitemaps_quotes},
         name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap_facts.xml', cache_page(7200)(sitemap), {'sitemaps': sitemaps_facts},
         name='django.contrib.sitemaps.views.sitemap'),
]
