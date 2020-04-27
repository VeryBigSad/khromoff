from django.urls import path
from . import views

app_name = 'urlshortner'
urlpatterns = [
    path('', views.create_new_link, name='index'),

    path('view_data/<str:view_data_code>', views.view_data, name='data'),  # spy data

    # redirect paths
    path('p/<str:short_id>', views.preview, name='preview'),
    path('<str:short_id>', views.redirect_to_long_url, name='redirect'),

]


