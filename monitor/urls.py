from django.urls import path
from . import views

app_name = 'monitor'

urlpatterns = [
    path('repositories',views.RepositoryListCreateView.as_view(),
        name='repositories-list-create')
]
