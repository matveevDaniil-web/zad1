# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import News, Comment
from .forms import RegisterForm, CommentForm, NewsForm


def home(request):
    latest_news = News.objects.all()[:3]
    return render(request, 'main/home.html', {'latest_news': latest_news})


def contacts(request):
    return render(request, 'main/contacts.html')


def news_list(request):
    news = News.objects.all()
    sort = request.GET.get('sort', 'desc')

    if sort == 'asc':
        news = news.order_by('pub_date')
    else:
        news = news.order_by('-pub_date')

    search_query = request.GET.get('search', '')
    if search_query:
        news = news.filter(Q(title__icontains=search_query))

    return render(request, 'main/news_list.html', {
        'news': news,
        'current_sort': sort,
        'search_query': search_query,
    })


def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    comments = news_item.comments.all()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news_item
            comment.user = request.user
            comment.save()
            return redirect('news_detail', news_id=news_item.id)
    else:
        form = CommentForm()

    return render(request, 'main/news_detail.html', {
        'news': news_item,
        'comments': comments,
        'form': form,
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


def user_login(request, django=None):
    from django.contrib.auth import authenticate
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'main/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    user_comments = Comment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/profile.html', {'user_comments': user_comments})


@login_required
def change_password(request):
    from django.contrib.auth import update_session_auth_hash
    from django.contrib.auth.forms import PasswordChangeForm
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/change_password.html', {'form': form})


@staff_member_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm()
    return render(request, 'main/news_form.html', {'form': form, 'title': 'Создать новость'})


@staff_member_required
def news_edit(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm(instance=news)
    return render(request, 'main/news_form.html', {'form': form, 'title': 'Редактировать новость'})


@staff_member_required
def news_delete(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        news.delete()
        return redirect('news_list')
    return render(request, 'main/news_confirm_delete.html', {'news': news})
