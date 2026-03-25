from django.shortcuts import render, get_object_or_404
from .models  import Post, Group
from django.contrib.auth import get_user_model


User = get_user_model()

def index(request):
    #posts = Post.objects.order_by('-pub_date')[:10]
    #posts = [Post.objects.get(id=5)]
    posts = Post.objects.filter(author_id=2)
    users  = User.objects.all()
    for user in users:
        print(user.id)
        print(user.username)
    for post in posts:
        print(post.text[:10])
        
    context = {
        'posts':posts,
        }
    return render(request, 'posts/index1.html', context)


def group_posts(request, slug):
    # Получаем объект группы по slug или возвращаем 404 ошибку
    group = get_object_or_404(Group, slug=slug)
    
    # Получаем все посты, принадлежащие этой группе
    # Сортируем по дате публикации от новых к старым
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    
    # Можно добавить ограничение на количество постов
    # posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)
