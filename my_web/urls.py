from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_page'),
    path('load_more', views.load_more, name='load_more'),
]
