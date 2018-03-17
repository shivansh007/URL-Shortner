from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [

  # FETCH short_url
  path('short-url/', views.short_url, name = 'short_url'),

  # FETCH long_url
  path('long-url/', views.long_url, name = 'long_url'),

  # FETCH short_urls
  path('short-urls/', views.short_urls, name = 'short_urls'),

  # FETCH long_urls
  path('long-urls/', views.long_urls, name = 'long_urls'),

  # FETCH count
  path('count/', views.count, name = 'count'),
]