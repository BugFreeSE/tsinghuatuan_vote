from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
                       url(r'^$', 'userpage.views.home'),
                       url(r'^validate/time/$', 'userpage.views.get_timestamp'),
                       url(r'^validate/try/$', 'userpage.views.validate_post'),
                       url(r'^validate/(?P<openid>\S+)/$', 'userpage.views.validate_view'),
                       url(r'^activity/(?P<activityid>\d+)/$','userpage.views.details_view'),
                       url(r'^ticket/(?P<uid>\S+)/$','userpage.views.ticket_view'),
                       url(r'^help/$','userpage.views.help_view'),
                       url(r'^helpact/$','userpage.views.helpact_view'),
                       url(r'^helpclub/$','userpage.views.helpclub_view'),
                       url(r'^helplecture/$','userpage.views.helplecture_view'),
                       url(r'^activity/(?P<actid>\d+)/menu/$', 'userpage.views.activity_menu_view'),
                       url(r'^setting/try/$','userpage.views.setting_view_post'),
                       url(r'^setting/(?P<openid>\S+)/$','userpage.views.setting_view'),
                       url(r'^cancelticket/(?P<ticket_uid>\S+)/$','userpage.views.cancel_ticket'),
                       url(r'^viewseats/(?P<openid>\S+)/(?P<districtid>\d+)/$','userpage.views.view_seats'),
                       )