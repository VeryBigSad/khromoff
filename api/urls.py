from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='api-docs-index'),
    path('test-request', views.make_request, name='api-make-request')
]
