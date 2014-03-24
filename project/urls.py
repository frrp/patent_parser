from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from api import v1_api

# Admin
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^large_data_admin/', include('large_data_admin.urls')),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
