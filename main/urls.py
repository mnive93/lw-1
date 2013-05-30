from lw.urls import *
from main.views import *

urlpatterns += patterns('',
    (r'^landing/$', nlr(hello)),
    (r'^signup/(\d+)/$', nlr(signup)),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_user),
)

urlpatterns += patterns('',
    (r'^feed/$', lr(feed)),
    (r'^posting/$', lr(posting)),
    (r'^u/([\w._-]+)$', profilepage),
)