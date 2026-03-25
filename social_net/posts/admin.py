# Register your models here.
from django.contrib import admin
# Из модуля models импортируем модель Post
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields =  ('text',)
    list_filter = ('pub_date',)
    empty_value_display = 'empty'
    
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = 'empty'

admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)

