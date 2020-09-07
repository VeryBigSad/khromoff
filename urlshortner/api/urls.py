from django.urls import path

from urlshortner.api import views

urlpatterns = [
    path('shorturl.get', views.ShorturlDetails.as_view(), name='shorturl-details'),
    path('shorturl.create', views.CreateShorturl.as_view(), name='shorturl-create'),
    path('shorturl.deactivate', views.ShorturlDeactivate.as_view(), name='shorturl-deactivate'),
    path('visit.get', views.VisitDetails.as_view(), name='visit-details'),
]
