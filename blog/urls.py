from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns.extend([
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('bloggers/', views.BloggerListView.as_view(), name='blogger_list')
])

urlpatterns.extend([
    path('<pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blogger/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger_detail')
])

urlpatterns.extend([
    path('<pk>/create', views.CommentCreate.as_view(), name='comment_create'),
    path('accounts/register', views.register, name='register')
])