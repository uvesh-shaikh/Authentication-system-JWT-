"""
Main URL routing for auth_project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve

urlpatterns = [
    path('api/', include('auth_app.urls')),
]

# Serve static files explicitly (both DEBUG and production)
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

# SPA catchall - serve index.html for all other routes
urlpatterns += [
    path('', TemplateView.as_view(template_name='index.html')),
    re_path(r'^(?!static/).*$', TemplateView.as_view(template_name='index.html')),
]
