from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_new_link, name='index'),

    path('about', views.about, name='about'),  # about the service
    path('view_data/<str:view_data_code>', views.view_data, name='data'),  # spy data

    # path('p', views.redirect),

    # redirect paths
    path('preview/<str:short_id>', views.preview, name='preview'),  # preview of redirect
    path('<str:short_id>', views.redirect_to_long_url, name='redirect'),  # redirect

]
