from django.contrib.sitemaps.views import sitemap
from django.urls import path
from .sitemaps import PostSitemap, QuoteSitemap, FactSitemap, InfoSitemap
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

urlpatterns = [
    path('', views.index, name='index_page'),
    path('info/', views.info, name='info_page'),
    path('status', views.status, name='status_page'),
    path('stats', views.stats, name='stats_page'),
    path('bot', views.botpage, name='bot_page'),
    path('load_more', views.load_more, name='load_more'),
    path('post/', views.postview_, name='postaddr'),
    path('quote/', views.postview_, name='quoteaddr'),
    path('fact/', views.postview_, name='factaddr'),
    path('story/', views.storyview_, name='storyaddr'),
    path('quote/<int:quoteid>/', views.quoteview),
    path('post/<int:postid>/', views.postview),
    path('fact/<int:factid>/', views.factview),
    path('info/<int:infoid>/', views.infoview),
    path('story/<str:storyid>/', views.storyview),
    path('sitemap_posts.xml', sitemap, {'sitemaps': sitemaps_posts},
         name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap_quotes.xml', sitemap, {'sitemaps': sitemaps_quotes},
         name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap_facts.xml', sitemap, {'sitemaps': sitemaps_facts},
         name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap_info.xml', sitemap, {'sitemaps': sitemaps_info},
         name='django.contrib.sitemaps.views.sitemap'),
]
