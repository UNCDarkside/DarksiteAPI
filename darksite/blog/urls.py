from django.urls import path

from blog import views


app_name = 'blog'

urlpatterns = [
    path(
        'posts/',
        views.PostListView.as_view(),
        name='post-list',
    ),
    path(
        'posts/<slug:post_slug>/',
        views.PostDetailView.as_view(),
        name='post-detail',
    ),
]
