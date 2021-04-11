from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from django.urls import path
from .sitemaps import PostSitemap, QuoteSitemap, FactSitemap, InfoSitemap, AWARE_Pages_Sitemap
from . import views

sitemaps_posts = {
    'posts': PostSitemap,
}

sitemaps_quotes = {
    'quotes': QuoteSitemap,
}

sitemaps_facts = {
    'facts': FactSitemap,
}

sitemaps_info = {
    'facts': InfoSitemap,
}

sitemaps_aware_pages = {
    'aware_pages': AWARE_Pages_Sitemap,
}

urlpatterns = [
    path('', views.index, name='index_page'),
    path('info/', views.info, name='info_page'),
    path('status', views.status, name='status_page'),
    path('stats', views.stats, name='stats_page'),
    path('bot', views.botpage, name='bot_page'),
    path('load_more', views.load_more, name='load_more'),
    path('post/', views.error_404, name='postaddr'),
    path('quote/', views.error_404, name='quoteaddr'),
    path('fact/', views.error_404, name='factaddr'),
    path('aware/', views.error_404, name='awareaddr'),
    path('story/', views.error_404, name='storyaddr'),
    path('news/', views.news_feed, name='news_page'),
    path('quote/<str:quoteid>/', views.quoteview),
    path('post/<str:postid>/', views.postview),
    path('fact/<str:factid>/', views.factview),
    path('aware/<str:awareid>/', views.awareview),
    path('story/<str:storyid>/', views.storyview),
    path('image/', views.image_proxy_view, name='imageproxy'),
    path('aware_api/', views.aware_api, name='aware_api'),
    path('sitemap_posts.xml', cache_page(7200)(sitemap), {'sitemaps': sitemaps_posts},
         name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap_quotes.xml', cache_page(7200)(sitemap), {'sitemaps': sitemaps_quotes},
         name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap_facts.xml', cache_page(7200)(sitemap), {'sitemaps': sitemaps_facts},
         name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap_aware_pages.xml', cache_page(7200)(sitemap), {'sitemaps': sitemaps_aware_pages},
         name='django.contrib.sitemaps.views.sitemap'),
]
