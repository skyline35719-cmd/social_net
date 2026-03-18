from django.contrib import admin

# Register your models here.
from django.contrib import admin
# Из модуля models импортируем модель Post
from .models import Post

admin.site.register(Post)