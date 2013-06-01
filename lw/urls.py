from django.conf.urls import patterns, include, url
from invites.views import *
from django.views.generic import TemplateView

import os.path
media = os.path.join(os.path.dirname(__file__), 'media')

# URL patterns for invite campaign pages

urlpatterns = patterns('',
    (r'^$', landing),
    (r'^emailadded/$', processInviteRequest),
    (r'^twitter/$', beginTwitterAuth),
    (r'^result/$', thanks),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':media}),
)

# URL patterns for the main application

urlpatterns += patterns('',
    (r'^m/', include('main.urls')),
)