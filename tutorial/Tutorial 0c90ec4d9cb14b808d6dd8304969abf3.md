# Tutorial

Created: March 22, 2023 4:10 PM
Tags: Django

## Admin site

> 관리자 페이지
> 
- 사용자가 아닌 서버의 관리자가 활용하기 위한 페이지
- 모델 class를 `admin.py`에 등록하고 관리

- admin 계정 생성
    
    `python [manage.py](http://manage.py) createsuperuser`
    
    ![Untitled](Tutorial%200c90ec4d9cb14b808d6dd8304969abf3/Untitled.png)
    
- admin site 로그인
    
    `http://127.0.01:8000/admin/`
    
    ![Untitled](Tutorial%200c90ec4d9cb14b808d6dd8304969abf3/Untitled%201.png)
    
    ![Untitled](Tutorial%200c90ec4d9cb14b808d6dd8304969abf3/Untitled%202.png)
    
- admin에 모델 클래스 등록
- 모델의 record를 보기 위해 `admin.py`
    
    ```python
    # articles/admin.py
    
    from django.contrib import admin
    from .models import Article
    
    admin.site.register(Article)
    ```
    
    ![Untitled](Tutorial%200c90ec4d9cb14b808d6dd8304969abf3/Untitled%203.png)
    
    - 데이터 조작
        
        ![Untitled](Tutorial%200c90ec4d9cb14b808d6dd8304969abf3/Untitled%204.png)
        
    - `db.sqlite3` database open
        
        ![Untitled](Tutorial%200c90ec4d9cb14b808d6dd8304969abf3/Untitled%205.png)
        

**ERROR**

`createsuperuser` 가 안 되는 경우

- `pip install django==3.2.18`
- `pip install pillow`
- `migrate`

CRUD 구현하기

**사전 준비**

- bootstrap CDN 및 템플릿 추가 경로 작성
    
    ```html
    <!-- templates/base.html-->
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Document</title>
      </head>
      <body>
        {% block content %}{% endblock content %}
      </body>
    </html>
    ```
    
    ```python
    # settings.py
    
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates', ],
    ```
    
- url 분리 및 연결
    
    ```python
    # articles/urls.py
    
    from django.urls import path
    
    app_name = 'articles'
    urlpatterns = [
        
    ]
    ```
    
    ```python
    # crud/urls.py
    
    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('articles/', include('articles.urls')),
    ]
    ```
    
- index 페이지 작성
    
    ```python
    # articles/urls.py
    
    from django.urls import path
    from . import views
    
    app_name = 'articles'
    urlpatterns = [
        path('', views.index, name='index'),
    ]
    ```
    
    ```python
    # articles/views.py
    
    from django.shortcuts import render
    
    # Create your views here.
    
    def index(request):
        return render(request, 'articles/index.html')
    ```
    
    ```html
    <!-- templates/articles/index.html-->
    
    {% extends 'base.html' %}
    {% block content %}
    <h1>Articles</h1>
    {% endblock content %}
    ```
    
- Article Model 작성
    
    ```python
    # articles/models.py
    
    from django.db import models
    
    # Create your models here.
    
    class Article(models.Model):
        title = models.CharField(max_length=10)
        content = models.TextField()
        
        updated_at = models.DateTimeField(auto_now=True)
        created_at = models.DateTimeField(auto_now_add=True)
    ```
    
- 관리자 페이지에서 글 생성하기

### READ1(index page)

**전체 게시글 조회**

- index 페이지에서는 전체 게시글을 조회해서 출력

```python
# articles/views.py

from . models import Article

def index(request):
	articles = Article.objects.all() # 전체 불러오기
	context = {
		'articles': articles,
	}
	return render(request, 'articles/index.html', context)
```

```html
{% extends 'base.html' %}
{% block content %}
	<h1>Articles</h1>
	{% for article in articles %}
	<p>글 번호: {{ article.pk }}</p>
	<p>글 제목: {{ article.title }}</p>
	{% endfor %}
{% endblock content %}
```

### READ2(detail page)

- 특정 게시글을 조회할 수 있는 번호받기

```python
urlpatterns = [
	path('<int:pk>/', views.detail, name='detail'),
]
```

```python
def detail(request, pk):
	article = Article.objects.get(pk=pk)
	context = {
		'article' : article,
	}
	return render(request, 'articles/detail.html, context)
```

```html
{% extends 'base.html' %}
{% block content %}
	<h2>DETAIL</h2>
	<p>{{ article.pk}} 번째 글</p>
	<a href="{% url 'articles:index' %}">BACK</a>
{% endblock content %}
```

- index에서 누르면 detail 로 넘어가기

```html
{% extends 'base.html' %}
{% block content %}
	<h1>Articles</h1>
	{% for article in articles %}
	<p>글 번호: {{ article.pk }}</p>
	<a href="{% url 'articles:detail' article.pk %}>
		<p>글 제목: {{ article.title }}</p>
	</a>
	{% endfor %}
{% endblock content %}
```

### CREATE

- 2 개의 `view` 함수 필요
    - `new function`
    - `create function`
- NEW

```python
urlpatterns = [
	path('new/', views.new, name='new'),
]
```

```python
def new(request):
	return render(request, 'articles/new.html')
```

```html
<form action="#" method="GET">
	<label for="title">TITLE: </label>
	<input type="text" name="title">
	<input type="submit">
</form>

<a href="{% url 'articles:index' %}">BACK</a>
```

- `index.html` 에 new 로 갈 수 있는 하이퍼 링크 작성

```html
<a href="<% url 'articles:new' %}">NEW</a>
```

- CREATE

```python
urlpatterns = [
	path('create/', views.create, name="create"),
]
```

- `view` 작성 3가지 방법(1번과 2번을 주로 선택)
    
    ```python
    
    def create(request):
    	title = request.GET.get('title')
    	content = request.GET.get('content')
    	return redirect('articles:detail', article.pk)
    ```
    
    ```python
    def create(request):
    	article = Article()
    	article.title = title
    	article.content = content
    	article.save()
    	return redirect('articles:detail', article.pk)
    ```
    
    ```python
    def create(request):
    	Article.objects.create(title=title, content=content)
    	redirect('articles:detail', article.pk)
    ```
    
    **render VS redirect**
    
    이미 만들어져 있는 url 로 보내고 싶은 경우 `redirect` 사용
    
    ```html
    <form action="{% url 'articles:create' %}" method="GET">
    ...
    </form>
    ```
    

### redirect()

> 인자에 작성된 곳으로 다시 요청을 보냄
> 
- 사용 가능한 인자
    - view name (URL pattern name) `return redirect(articles`
    - absolute or relative URL `return redirect('/articles/)`

### GET VS POST

**GET**

> 어떠한 데이터를 조회하는 요청 → Query String 형식
> 
- 특정 리소스를 가져오도록 요청할 때 사용
- 반드시 데이터를 가져올 때만 사용
- DB에 변화 X
- CRUD 에서 R

**POST**

> 어떠한 데이터를 생성하는 요청 → Body에 담겨서 보내짐
> 
- 서버로 데이터를 전송할 때 사용
- 서버에 변경사항을 만듦
- 리소스를 생성/변경하기 위해 데이터를 HTTP body에 담아 전송
- GET의 쿼리 스트링 파라미터와 다르게 URL로 데이터를 보내지 않음
- CRUD 에서 CUD

→ POST method 적용해보기

💥 Forbidden ERROR

**csrf_token**

> 템플릿에서 내부 URL로 향하는 Post form을 사용하는ㄱ ㅕㅇ우에 사용
> 

`{% csrf_token %}`

### DELETE

- 삭제하고자 하는 특정 글을 조회 후 삭제해야함

```python
urlpatterns = [
	path('<int:pk>/delete/', views.delete, name='delete'),
]
```

```python
def delete(request, pk):
	article = Article.objects.get(pk=pk)
	article.delete()
	return redirect('articles:index')
```

```html
<form action="{% url 'articles:delete' article.pk %}" method="POST">
	{% csrf_token %}
	<input type="submit" value="DELETE">
</form>
<a href="{% url 'articles:index' %}BACL</a>
```

### UPDATE

```python
urlpatterns = [
	path('<int:pk>/update/', views.update, name="update"),
]
```

```python
def update(request, pk):
	article = Article.objects.get(pk=pk)
	article.title = request.POST.get('title')
	article.content = request.POST.get('content')
	return redirect('articles:detail', article.pk)
```

```html
<input type="text" name="title" value="{{article.title}}"><br>
<textarea name="content">{{ article.content }}</textarea>

<form action="{% url 'articles:update' article.pk %}' method="POST">
{% scrf_token %}
```

- 기존 데이터 출력
- `detail.html` 에서 update 페이지로 이동하기 위한 하이퍼링크 작성

```html
<a href="{% url 'articles:update' article.pk %}>EDIT</a>
```

### create

> new + create view
> 

```python
def create(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		content = request.POST.get('content')
		article = Article(title=title, content=content)
		article.save()
		return redirect('articles:detail', pk=article.pk)
	else:
		return render(request, 'articles/create.html')
```

### upate

> edit + update view
> 

```python
def update(request, pk):
	article = ARticle.objects.get(pk=pk)
	if request.method == 'POST':
		article.title = request.POST.get('title)
		content = request.POST.get('content')
		article = Article(title=title, content=content)
		article.save()
		return redirect('articles:detail', pk=article.pk)
	else:
		context = {'article' : article}
		return render(request, 'articles/create.html', context)
```

### delete

> POST 요청에 대해서만 삭제 가능하게 하기
> 

```python
def delete(request, pk):
	article = Article.objects.get(pk=pk)
	if request.method == 'POST':
		article.delete()
		return redirect('articles:index')
	else:
		redirect('articles:detail, article.pk)
```

### Django Form

> Form Class를 선언하여 Django Form 시스템 관리하기
> 

- 앱 폴더에 `[forms.py](http://forms.py)` 생성 후 `ArticleForm Class` 선언

```python
# articles/forms.py
from django import forms

class ArticleForm(forms.Form):
	title = forms.CharField(max_length=10)
	content = forms.CharField()
```

- form 에는 TextField가 존재하지 않는다
    - Form fields
        
        `forms.CharField()`
        
        - 입력에 대한 유효성 검사 로직 처리
        - 템플릿에서 직접 사용
    - Widgets
        
        `forms.Charfield(widget=forms.Textarea)`
        
        - 웹 페이지의 HTML input 요소 렌더링
            - 단순히 input 요소의 보여지는 부분을 변경
- `view` 업데이트

```python
def create(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		content = request.POST.get('content')
		article = Article(title=title, content=content)
		article.save()
		return redirect('articles:detail', pk=article.pk)
	else:
		form = ArticleForm()
		context = {'form':form}
		return render(request, 'articles/create.html', context)
```

- `template` 업데이트

```html
{% extends 'base.html' %}
{% block content %}
	<h1>CREATE</h1>
	<form action="{% url 'articles:create' %}" method="POST">
	{% csrf_token %}
	{{ form.as_p }}
	<input type="submit">
	</form>
	<a href="{% url 'articles:index' %}">BACK</a>
{% endblock content %}
```

![Untitled](Tutorial%200c90ec4d9cb14b808d6dd8304969abf3/Untitled%206.png)

### STATIC

**Static files 구성하기(settings)**

- `STATIC_ROOT`에 정적 파일 수집하기
    
    `STATIC_ROOT = BASE_DIR /  'staticfiles'`
    
- `STATICFILES_DIRS`
    
    ```python
    STATICFILES_DIRS = [
    	BASE_DIR / 'static',
    ]
    ```
    
- `STATIC_URL`
    
    `STATIC_URL = '/static/'`
    

**static file 가져오기**

1. 기본 경로
    - `articles/static/articles` 에 이미지 파일 배치하기
    - static tag 사용해 이미지 파일 출력하기
    
    ```python
    {% load static %}
    {% block content %}
    	<img src="{% static 'articles/sample_img_1.png' %}" alt="sample-img-1">
    
    ```
    
2. 추가 경로
    - 추가 경로 작성
    
    ```python
    # settings.py
    STATICFILES_DIRS = [
    BASE_DIR / 'static',
    ]
    ```
    
    - 추가 경로에서 파일 가져오기
        - static/ 경로에 이미지 파일 배치하기
        - static tag 사용해 이미지 파일 출력하기
        
        ```python
        <img src="{% static 'sample_img_2.png%}" alt="sample-img-2">
        
        ```
        

### MEDAI

**ImageField()**

> 이미지 업로드
> 
- 경로 지정
    
    ```python
    # settings.py
    MEDIA_ROOT = BASE_DIR / 'media'
    ```
    
- url 경로 지정
    
    ```python
    # settings.py
    MEDIA_URL = '/media/'
    ```
    
- 개발단계에서 사용자가 업로드한 미디어 파일 제공하기
    
    ```python
    # crud/urls.py
    from django.conf import settings
    from django.conf.urls.static import static
    
    urlpatterns = [
    	...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```
    

- 사용하기
    - `ImageField` 작성
    
    ```python
    class Article(models.Model):
    	image = models.ImageField(blank=True)
    ```
    
    - `migrations`
        
        `Pillow` 라이브러리 필요
        
- form 태그의 `enctype` 속성 변경
    
    ```html
    <form action="{% url 'articles:create' %}" method="POST" enctype="multipart/form-date">
    ```
    
- request.FILES 추가하기
    
    ```python
    # articles/views.py
    
    def create(request):
    	if request.method == 'POST':
    			form = ArticleForm(request.POST, request.FILES)
    ```
    
- 이미지 출력하기
    
    ```html
    <img src="{{ article.image.url }}">
    ```