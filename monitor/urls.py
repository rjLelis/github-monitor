from django.urls import path
from . import views

app_name = 'monitor'

urlpatterns = [
    path('repositories', views.RepositoryListCreateView.as_view(),
         name='repositories-list-create'),
    path('repositories/<str:repo_name>/commits',
         views.commits_by_repository, name='commits-by-repository'),
     path('push_event', views.push_event, name='push-event')
]
