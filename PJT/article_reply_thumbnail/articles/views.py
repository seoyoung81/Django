from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    # comment 작성 폼
    commentForm = CommentForm()
    # 이미 작성된 comment list
    # comment_list = article.comment_set.all()
    comment_list = article.comment_set.filter(parent__isnull=True) # 댓글 Select * form Comment Where parent IS NULL;
    context = {
        'article': article,
        'commentForm': commentForm,
        'comment_list': comment_list,
        }
    return render(request, 'articles/detail.html', context)


def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()

    context = {'form': form}
    return render(request, 'articles/create.html', context)


def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')


def update(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    context = {'form': form, 'article': article}
    return render(request, 'articles/update.html', context)


def create_comment(request, pk):
    # 작성할 article 객체 불러오기
    article = Article.objects.get(pk=pk)
    # modelForm
    commentForm = CommentForm(request.POST) # 사용자 입력 값 받아와서, 폼 인스턴스까지
    parent_pk = request.POST.get('parent_pk')

    
    if commentForm.is_valid():
        comment = commentForm.save(commit=False)  # TCL
        comment.article = article
        # 얘가 댓글인지 답글인지
        if parent_pk:
            parent_comment = Comment.objects.get(pk=parent_pk)
            comment.parent = parent_comment
        comment.save()
    return redirect('articles:detail', article.pk)

