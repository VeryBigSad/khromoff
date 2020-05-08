from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    # accounts shit
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('me', views.me, name='me'),
    path('personal', views.personal, name='personal'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),

    # api
    # path('api-docs/', include('api.urls')),
    # path('api/', include('urlshortner.api.urls'))
]

handler404 = 'khromoff.views.error404'
handler500 = 'khromoff.views.error500'
