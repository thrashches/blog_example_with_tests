from django.urls import path
from .views import *


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('posts/', PostCreateView.as_view(), name='create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='update'),
]
