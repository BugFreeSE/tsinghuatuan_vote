from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import settings
from tastypie.api import Api
from urlhandler.api import VoteActResource, CandidateResource, VoteLogResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(VoteActResource())
v1_api.register(VoteLogResource())
v1_api.register(CandidateResource())

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'userpage.views.home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^webhost_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^u/', include('userpage.urls')),
    url(r'^', include('adminpage.urls')),
    url(r'^api/', include(v1_api.urls)),
) + staticfiles_urlpatterns()
