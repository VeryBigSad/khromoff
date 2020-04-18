from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_new_link),
    path('links', views.links),
    path('a/p/<str:short_id>', views.redirect, {'preview': True, 'anonymous': True}),  # anonymous redirect with preview
    path('a/<str:short_id>', views.redirect, {'anonymous': True}),  # anonymous redirect
    path('p/<str:short_id>', views.redirect, {'preview': True}),  # redirect with preview

    path('<str:short_id>', views.redirect)
]

