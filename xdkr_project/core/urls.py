from django.urls import include
from django.urls import path
from . import views
from django.conf import settings
from django.templatetags.static import static
from .views import serve_document
from .models import Document, Tag

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('create/', views.document_create, name='document_create'),
    path('<int:pk>/read', views.document_read, name='document_read'),
    path('<int:pk>/update', views.document_update, name='document_update'),
    path('<int:pk>/delete', views.document_delete, name='document_delete'),
    path('documents/<int:pk>/serve/', serve_document, name='serve_document'),
    ]