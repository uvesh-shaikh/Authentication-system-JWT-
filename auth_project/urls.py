"""
Main URL routing for auth_project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse, FileResponse
from django.views.decorators.http import condition
import os

urlpatterns = [
    path('api/', include('auth_app.urls')),
]

# Serve static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # In production, use WhiteNoise via middleware, but add explicit static URL handling
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Catch all other routes and serve index.html (SPA)
# But exclude /static/ and /api/ paths
urlpatterns += [
    re_path(r'^(?!static/|api/).*', TemplateView.as_view(template_name='index.html')),
]
