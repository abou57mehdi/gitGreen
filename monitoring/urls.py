# monitoring/urls.py
from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('article/<int:article_id>/', views.article_detail, name='article_details'),
    path('upload/', views.upload_file, name='upload_file'),

]


