from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostCreateForm
from .models import Comment, Follow, Group, Post
from django.views.decorators.cache import cache_page

User = get_user_model()

# def index(request):
#     #posts = Post.objects.order_by('-pub_date')[:10]
#     #posts = [Post.objects.get(id=5)]
#     posts = Post.objects.filter(author_id=2)
#     users  = User.objects.all()
#     for user in users:
#         print(user.id)
#         print(user.username)
#     for post in posts:
#         print(post.text[:10])
        
#     context = {
#         'posts':posts,
#         }
#     return render(request, 'posts/index1.html', context)

@cache_page(60 * 15)
def index(request):
    # Get search keyword from GET parameters
    keyword = request.GET.get('q', None)
    
    # Start with all posts ordered by date
    #post_list = Post.objects.all().order_by('-pub_date')
    
    # Start with all posts ordered by date
    post_list = Post.objects.select_related('author', 'group').order_by('-pub_date')    
    
    # Apply search filter if keyword exists
    if keyword:
        # Use icontains for case-insensitive search (more user-friendly)
        post_list = post_list.filter(text__icontains=keyword)    
    
    # Pagination: 10 posts per page   
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'keyword': keyword,  # Pass keyword to template for display        
    }
    return render (request, 'posts/index.html', context)
    

def group_posts(request, slug):
    # Получаем объект группы по slug или возвращаем 404 ошибку
    group = get_object_or_404(Group, slug=slug)
    
    # Получаем все посты, принадлежащие этой группе
    # Сортируем по дате публикации от новых к старым
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    
    # Можно добавить ограничение на количество постов
    # posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]

    # Add pagination for group posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Signs of socity {group.slug}'
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def post_create(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        form = PostCreateForm(
            request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save()
            return redirect('posts:profile', request.user.username)
            # return redirect('posts:post_detail', post.post_id)
    form = PostCreateForm()
    return render(request, 'posts/create_post.html',
                  {'form': form, 'groups': groups})
 
# class PostCreateView(LoginRequiredMixin, CreateView):
#     template_name = 'posts/create_post.html'
#     model = Post
#     form_class = PostCreateForm
#     success_url = reverse_lazy('posts:my_profile')

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)   

def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return HttpResponse('Редактировать пост может только его автор')

    form = PostCreateForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }

    return render(request, 'posts/create_post.html', context)

def profile(request, username=None):
    if username is None:
        username = request.user.username

    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(
        author__username=username).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    sum_of_posts = len(posts)

    context = {
        'username': username,
        'posts': posts,
        'sum': sum_of_posts,
        'page_obj': page_obj,
    }

    if not request.user.is_anonymous:
        following = Follow.objects.filter(user=request.user,
                                          author=author).exists()
        context['following'] = following

    return render(request, 'posts/profile.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()
    comments = Comment.objects.filter(post_id=post_id)
    author = post.author
    all_posts = Post.objects.filter(author=author)
    sum_of_posts = len(all_posts)
    context = {
        'post': post,
        'sum': sum_of_posts,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)

def author_posts(request, author_id):
    posts = Post.objects.filter(author_id=author_id)

    context = {
        'posts': posts,
    }
    return render(request, 'posts/author_posts.html', context)

def groups(request):
    title = 'Список групп'
    groups = Group.objects.all()
    context = {
        'title': title,
        'groups': groups,
    }
    return render(request, 'posts/all_groups.html', context)

@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)

@login_required
def profile_follow(request, username):
    follow_author = get_object_or_404(User, username=username)
    if request.user != follow_author:
        Follow.objects.get_or_create(user=request.user, author=follow_author)
    return redirect('posts:profile', username=username)

@login_required
def profile_unfollow(request, username):
    unfollow_from_author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user).filter(
        author=unfollow_from_author).delete()
    return redirect('posts:profile', username=username)

def follow_index(request):
    from django.db import reset_queries
    reset_queries()
    title = 'Избранные авторы'
    # post_list = Post.objects.all().order_by('-pub_date')
    # follows = Follow.objects.filter(user=request.user).values_list('author')
    # print(follows)
    # post_list = Post.objects.filter(author__in=follows).order_by('-pub_date')
    post_list = Post.objects.prefetch_related('author').filter(
        author__following__user=request.user).order_by('-pub_date')
    print(f' Количество запросов {len(connection.queries)}')
    pagi = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = pagi.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': title
    }
    return render(request, 'posts/index.html', context)

