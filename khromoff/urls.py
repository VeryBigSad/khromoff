"""khromoff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shorturl/', include('urlshortner.urls')),

    # accounts shit
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('me', views.me, name='me'),
    path('personal', views.personal, name='personal'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),

    # api
    path('api-docs/', include('api.urls')),
    path('api/shorturl/', include('urlshortner.api.urls'))
]

handler404 = 'khromoff.views.error404'
handler500 = 'khromoff.views.error500'
