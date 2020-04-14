from django.urls import path

from . import views

urlpatterns = [
    path('about', views.about),
    path('ogin', views.login_page),
    path('ogout', views.logout_page),
    path('personal', views.cabinet),
    path('', views.index)

]
