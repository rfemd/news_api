from django.urls import path

from .views import *

app_name = "news"

urlpatterns = [

    #path("home/",home_view, name="home-view"),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('all_news/', NewsListView.as_view(), name='news-list'),
    path('tagged_news/', TagNewsListView.as_view(), name='tagged-news-list'),
    path('statistics/', HitCountListView.as_view(), name='hitcount-list'),
    path('likes/', like_dislike, name='like-news-view'),
]
