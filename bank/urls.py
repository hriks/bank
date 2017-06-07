
from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth import views
from log.forms import LoginForm
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('log.urls')),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'), # noqa
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_URL
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
