from lw.urls import *
from main.views import *

urlpatterns += patterns('',
    (r'^landing/$', nlr(hello)),
    (r'^signup/(\d+)/$', nlr(signup)),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_user),
    (r'^feed/$', lr(feed)),
)