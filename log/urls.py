
from django.conf.urls import url
from . import views
from .views import create


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create/$', views.create, name='create'),

]
