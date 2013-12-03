from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
                       url(r'^$', 'userpage.views.home'),
                       url(r'^validate/$', 'userpage.views.validate_view'),
                       url(r'^validate/try/$', 'userpage.views.validate_post'),
                       url(r'^activity/$','userpage.views.details_view'),
                       url(r'^qrcode/$','userpage.views.qrcode_view'),
                       )