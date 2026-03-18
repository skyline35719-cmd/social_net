from django.urls import path
from . import views


app_name = 'post'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    #path('group/<slug:name>',views.group_posts), name-'group_posts')
]