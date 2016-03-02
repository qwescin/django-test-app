from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

months = ('January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December')



months_revert = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June',
          '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}
# Create your views here.

conv_date = []
conv_year_month = []

def post_list(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts, 5)

    page = request.GET.get('page')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)

    for post in posts:
        month, year = str(post.published_date.month), str(post.published_date.year)
        if month+year in conv_date: continue
        conv_date.append(month+year)
        conv_year_month.append((month, year))

    return render(request, 'blogpost/post_list.html', {'posts_list': posts_list, 'conv_date': conv_date,
                                                       'months_revert':months_revert, 'conv_year_month': conv_year_month})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blogpost/post_detail.html', {'post': post})

def months_archive(request, year, month):

    posts_all = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    posts = Post.objects.filter(published_date__year=year, published_date__month=month).order_by('-published_date')

    paginator = Paginator(posts, 5)

    page = request.GET.get('page')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)

    for post in posts_all:
        months, year = str(post.published_date.month), str(post.published_date.year)
        if months+year in conv_date: continue
        conv_date.append(months+year)
        conv_year_month.append((months, year))

    return render(request, 'blogpost/post_list.html', {'posts_list': posts_list, 'conv_date': conv_date,
                                                       'months_revert':months_revert, 'conv_year_month': conv_year_month})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blogpost/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blogpost/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blogpost/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

