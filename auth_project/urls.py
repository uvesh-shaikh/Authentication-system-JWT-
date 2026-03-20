"""
Main URL routing for auth_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('api/', include('auth_app.urls')),
]

# Serve static files - BOTH in DEBUG and PRODUCTION
# WhiteNoise will handle these efficiently in production
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Template routes - MUST BE BEFORE CATCH-ALL
# These handle both /page and /page.html formats
urlpatterns += [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html')),
    path('login', TemplateView.as_view(template_name='login.html'), name='login'),
    path('login.html', TemplateView.as_view(template_name='login.html')),
    path('register', TemplateView.as_view(template_name='register.html'), name='register'),
    path('register.html', TemplateView.as_view(template_name='register.html')),
    path('profile', TemplateView.as_view(template_name='profile.html'), name='profile_page'),
    path('profile.html', TemplateView.as_view(template_name='profile.html')),
]

# Catch-all for undefined routes - THIS MUST BE LAST
urlpatterns += [
    path('<path:path>', TemplateView.as_view(template_name='index.html')),
]

# Custom error handlers
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
