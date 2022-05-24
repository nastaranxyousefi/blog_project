from django.urls import path

from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/<str:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('update/<slug:slug>/<str:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('delete/<slug:slug>/<str:pk>/', views.PostDeleteView.as_view(), name='post_delete'),

]