from django.urls import path
from . import views
urlpatterns = [
    path('', views.create_new_link, name='urlshortner-index'),

    # auth only
    path('view_data/<str:view_data_code>', views.view_data, name='urlshortner-data'),  # data about
    # particular shorturl obj

    # my social media redirects (why here? idk)
    path('my-github-redirect', views.redirect, name='my-github-redirect'),
    path('my-telegram-redirect', views.redirect, name='my-telegram-redirect'),
    path('my-vk-redirect', views.redirect, name='my-vk-redirect'),

    # redirect paths
    path('a/p/<str:short_id>', views.redirect, {'preview': True, 'anonymous': True}, name='shorturl-a-p-redirect'),
    path('a/<str:short_id>', views.redirect, {'anonymous': True}, name='shorturl-a-redirect'),
    path('p/<str:short_id>', views.redirect, {'preview': True}, name='shorturl-p-redirect'),
    path('<str:short_id>', views.redirect, name='shorturl-redirect'),

]


