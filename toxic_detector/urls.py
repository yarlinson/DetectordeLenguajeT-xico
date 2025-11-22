"""
URL configuration for toxic_detector project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path, include

def admin_logout_view(request):
    """Vista personalizada para logout del admin que acepta GET y POST"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('/')

urlpatterns = [
    path('admin/logout/', admin_logout_view, name='admin_logout'),
    path('admin/', admin.site.urls),
    path('', include('detector.urls')),
]
