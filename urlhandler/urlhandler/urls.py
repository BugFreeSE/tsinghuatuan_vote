from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'userpage.views.home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^webhost_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^u/', include('userpage.urls')),
    url(r'^', include('adminpage.urls')),
) + staticfiles_urlpatterns()
