from django.contrib import admin
from django.urls import path
from todos import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'todos'
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:pk>/detail/', views.detail, name="detail"),
    path('create/', views.create, name="create"),
    path('<int:pk>/update/', views.update, name="update"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
