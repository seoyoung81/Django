### Admin Site

> Django의 가장 강력한 기능 중 하나인 automatic admin interface
> 
- 관리자 페이지
    - 사용자가 아닌 서버의 관리자가 활용하기 위한 페이지
    - 모델 class를 `admin.py`에 등록하고 관리
    - 레코드 생성 여부 확인에 매우 유용하며 직접 레코드를 삽입할 수도 있음

1. **관리자 계정 생성**
    
    `python [manage.py](http://manage.py) createsuperuser`
    
    - username과 password를 입력해 관리자 계정을 생성
        - email 선택사항
        - 비밀번호 생성 → 보안상 터미널에 입력되지 않음
2. **admin site 로그인**
    
    `[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)` 로 접속 후 로그인
    
    - 계정만 만든 경우 Django 관리자 화면에서 모델 클래스는 보이지 않음
3. **admin에 모델 클래스 등록**
    - 모델의 record를 보기 위해서는 admin.py에 등록 필요
    
    ```python
    # articles/admin.py
    from django.contrib import admin
    from .models import Article
    
    admin.site.register(Article)
    ```
    
4. **등록된 모델 클래스 확인**
5. **데이터 CRUD 테스트**
    - admin 페이지에서 데이터를 조작해보기

### CRUD with View

> QuerySet API를 통해 view 함수에서 직접 CRUD  구현하기
> 

**사전준비**

1. base 템플릿 작성
    - bootstrap CDN 및 템플릿 추가 경로 작성
    
    ```html
    <!-- templates/base.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
    </head>
    <body>
      {% block content %}
    	{% endblock content %}
    </body>
    </html>
    ```
    
    ```python
    # settings.py
    TEMPLATES = [
    	{
    		'DIRS' = [BASE_DIR / 'templates',],
    ]
    ```
    
2. url 분리 및 연결
    
    ```python
    # articles/url.py
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
    
3. index 페이지 작성
    
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
    
4. Article Model 작성
    
    ```python
    from django.db import models
    
    # Create your models here.
    class Article(models.Model):
    	title = models.CharField(max_length=10)
    	content = models.TextFiedl()
    	
    	updated_at = models.DateTimeField(auto_now=True)
    	created_at = models.DateTimeField(auto_now_add=True)
    ```
    
5. 관리자 페이지에서 글 생성해보기
    
    

**READ 1(index page)**

1. 전체 게시글 조회
    - index 페이지에서는 전체 게시글을 조회해서 출력한다
        
        ```python
        # articles/views.py
        from .models import Article
        
        def index(request):
        	articles = Article.objects.all()
        	context = {
        		'articles': articles,
        	}
        	return render(request, 'articles/index.html', context)
        ```
        
        ```html
        <!--templates/articles/index.html-->
        {% extends 'base.html' %}
        {% block content %}
        	<h1>Articles</h1>
        	<hr>
        	{% for article in articles %}
        	<p>글 번호 : {{ article.pk }}</p>
        	<p>글 제목 : {{ article.title }}</p>
        	<p>글 내용 : {{ article.content }}</p>
        	<hr>
        {% endfor %}
        {% endblock content %}
        
        ```
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0aa52f47-2e16-48ad-9fd3-325f5d9ee9b2/Untitled.png)
        
    

**READ 2(detail page)**

- 개별 게시글 상세 페이지 제작
- 모든 게시글 마다 뷰 함수와 템플릿 파일을 만들 수는 없음
    - 글의 번호(pk)를 활용해서 하나의 뷰 함수와 템플릿 파일로 대응
- 무엇을 활용할 수 있을까?
    - Variable Routing
1. **urls**
    - URL로 특정 게시글을 조회할 수 있는 번호를 받음
        
        ```python
        # articles/urls.py
        
        urlpatterns = [
        	...
        	path('<int:pk>/', views.detail, name='detail'),
        ]
        ```
        
2. **views**
    - `Article.objects.get(pk=pk)` 에서 오른쪽 pk는 variable routing을 통해 받은 pk, 왼쪽 pk는 DB에 저장된 레코드의 id 컬럼
        
        ```python
        # articles/views.py
        
        def detail(request, pk):
        	article = Article.objects.get(pk=pk)
        	context = {
        		'article' : article,
        	}
        	return render(request, 'articles/detail.html', context)
        ```
        
3. **templates**
    
    ```html
    <!-- templates/articles/detail.html-->
    {% extends 'base.html' %}
    
    {% block content %}
    	<h2>DETAIL</h2>
    	<h3>{{ article.pk }} 번째 글</h3>
    	<hr>
    	<p>제목: {{ article.title }}</p>
    	<p>내용: {{ article.content }}</p>
    	<p>작성 시각: {{ article.created_at }}</p>
    	<p>수정 시각: {{ article.updated_at }}</p>
    	<hr>
    	<a href="{% url 'articles:index' %}">[back]</a>
    {% endblock content %}
    ```
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/15d93829-468a-49c9-afa0-06099b7ecc99/Untitled.png)
    
    - 제목을 누르면 상세페이지로 이동하게 하기
    
    ```html
    <!-- articles index.html-->
    {% extends 'base.html' %}
    
    {% block content %}
    	<h1>Articles</h1>
    	{% for article in articles %}
    		<p>글 번호: {{ article.pk }}</p>
    		<a href="{% url 'articles:detail' article.pk %}">
    			<p>글 제목: {{ article.title }}</p>
    		</a>
    		<p>글 내용: {{ article.content }}</p>
    		<hr>
    	{% endfor %}
    {% endblock content %}
    ```
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/509e4c76-9d58-471f-8e37-3f215a785a4c/Untitled.png)
    

**CREATE**

- CREATE 로직을 구현하기 위해서는 2개의 view 함수 필요
    - 사용자의 입력을 받을 페이지를 렌더링 하는 함수 1개
        - `"new" view function`
    - 사용자가 입력한 데이터를 전송 받아 DB에 저장하는 함수 1개
        - `"create" view function`
        
1. **url**
    
    ```python
    # articles/urls.py
    
    urlpatterns = [
    	...
    	path('create/', views.create, name='create'),
    ]
    ```
    
2. **View**
    
    ```python
    def freate(request):
    	title = request.GET.get('title')
    	content = request.GET.get('content')
    	
    	article = Article(title=title, content=content)
    	article.save()
    	
    	return redirect('articles:detail', article.pk)
    ```
    
    - `redirect()`
        - 인자에 작성된 곳으로 다시 요청을 보냄
        - 사용 가능한 인자
            1. view name (URL pattern name) `retrun redirect('articles:index')`
            2. absolute or relative URL `return redirect('/articles/')`
3. **New**
    - new 페이지로 이동할 수 있는 하이퍼 링크 작성
    - form 마무리
    
    ```html
    <!-- templates/articles/index.html-->
    {% extends 'base.html'%}
    
    {% block content %}
    	<h1>Articles</h1>
    	<a href="{% url 'articles:new' %}">NEW</a>
    	<hr>
    {% endblock content %}
    ```
    
    ```html
    <!-- templates/articles/new.html-->
    {% extends 'base.html'%}
    
    {% block content %}
    	<h1>NEW</h1>
    	<form action="{% url 'articles:create' %}" method="GET">
    		<label for='title'>Title: </label>
    		<input type="text" name="title"><br>
    		<label for='content'>Content: </label>
    		<textarea name="content"></textarea><br>
    		<input type="submit">
    	</form>
    	<hr>
    	<a href="{% url 'articles:index' %}">[back]</a>
    {% endblock content %}
    ```
    

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0b7c5f41-3a7a-47de-8b67-de7d7f3faca3/Untitled.png)

## HTTP Method

**HTTP**

- 네트워크 상에서 데이터를 주고 받기 위한 약속

**HTTP Method**

- 데이터(리소스)에 어떤 요청(행동)을 원하는지를 나타낸 것

**GET & POST**

- GET
    - 어떠한 데이터(리소스)를 조회하는 요청
    - GET 방식으로 데이터를 전달하면 Query String 형식으로 보내짐
    - 데이터를 조회하는데, 데이터 전달이 필요한 이유?
    
    **현재 코드 재검토**
    
    - GET은 쿼리 스트링 파라미터로 데이터를 보내기 때문에 url을 통해 데이터를 보냄
    - 현재 요청은 데이터를 조회하는 것이 아닌 작성을 워하는 요청
- POST
    - 어떠한 데이터(리소스)를 생성(변경)하는 요청
    - POST 방식으로 데이터를 전달하면 Query String 이 아닌 Body에 담겨서 보내짐

**정리**

- GET
    - 특정 리소스를 가져오도록 요청할 때 사용
    - 반드시 데이터를 가져올 때만 사용해야 함
    - DB에 변화를 주지 않음
    - CRUD에서 R 역할을 담당
- POST
    - 서버로 데이터를 전송할 때 사용
    - 서버에 변경사항을 만듦
    - 리소스를 생성/변경하기 위해 데이터를 HTTP body에 담아 전송
    - GET의 쿼리 스트링 파라미터와 다르게 URL로 데이터를 보내지 않음
    - CRUD에서 C/U/D 역할을 담당

```html
<!-- templates/articles/new.html-->
{% extends 'base.html' %}

{% block content %}
	<h1 class="text-center">NEW</h1>
	<form action="{% url 'articles:create' %}" method="POST">
	</form>
	<a href="{% url ' articles:index' %}">[back]</a>
{% endblock content %}
```

```python
# articles/views.py
def create(request):
	title = request.POST.get('title')
	content = request.POST.get('content')
```

→ 결과`