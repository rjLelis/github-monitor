from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.index, name='index'),
    path('token', views.get_token, name='get-token'),
    path('redirect', views.redirect_access, name='redirect')
]
