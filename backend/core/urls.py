"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.views.generic import TemplateView

admin.site.site_title = "Beerdegu Admin"
admin.site.site_header = "Beerdegu Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rooms.urls')),
    path('api/', include('beers.urls')),
    path('auth/', include('users.urls')),
    # frontend urls
    re_path(".*", TemplateView.as_view(template_name="index.html")),
]
