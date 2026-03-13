from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index),
    #path('group/<slug:name>',views.group_posts)
]