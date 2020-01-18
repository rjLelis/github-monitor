from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_access.urls', namespace='auth')),
    path('api/', include('monitor.urls', namespace='monitor')),
    path('', include('frontend.urls', namespace='frontend'))
]
