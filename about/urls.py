from django.urls import path
from django.conf.urls.static import static

from khromoff import settings
from . import views

urlpatterns = [
    path('about', views.about),
    path('ogin', views.login_page),
    path('ogout', views.logout_page),
    path('personal', views.cabinet),
    path('', views.index)

]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
