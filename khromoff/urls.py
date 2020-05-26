from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    # accounts
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('me', views.me, name='me'),
    path('personal', views.personal, name='personal'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),

    # bugs
    path('bugs/', include('bughunter.urls')),
    # error 500
    path('500', views.error500, name='error500'),

]

handler404 = 'khromoff.views.error404'
handler500 = 'khromoff.views.error500'
