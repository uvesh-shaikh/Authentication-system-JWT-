"""
Main URL routing for auth_project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.views.generic import TemplateView

urlpatterns = [
    path('api/', include('auth_app.urls')),
    # Serve HTML files
    path('', serve, {'path': 'index.html', 'document_root': settings.STATICFILES_DIRS[0]}),
    re_path(r'^(?P<path>.*\.html)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
]

# Serve static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
