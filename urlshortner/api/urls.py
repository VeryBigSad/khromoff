from django.urls import path
from urlshortner.api import views

urlpatterns = [
    path('shorturl.get', views.shorturl_details),
    path('visit.get', views.visit_details),
]
