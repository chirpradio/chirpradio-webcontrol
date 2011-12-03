from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()


handler500 = "pinax.views.server_error"


urlpatterns = patterns("apps.webcontrol.views",
    url(r"^$", "control_panel", name="control-panel"),
)
