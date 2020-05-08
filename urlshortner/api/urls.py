from django.urls import path

from urlshortner.api import views

urlpatterns = [
    path('shorturl.get', views.ShorturlDetails.as_view(), name='shorturl-details'),
    path('shorturl.create', views.CreateShorturl.as_view(), name='shorturl-create'),
    # path('visit.list', views.VisitViewSet.as_view({'get': 'list'}), name='visit-list'),
    path('visit.get', views.VisitDetails.as_view(), name='visit-details'),
]
