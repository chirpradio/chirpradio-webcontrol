from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()


handler500 = "pinax.views.server_error"


urlpatterns = patterns("apps.webcontrol.views",
    url(r"^$", "control_panel", name="control-panel"),
    url(r"^do_dump_new_artists_in_dropbox$", "do_dump_new_artists_in_dropbox", name="do-dump"),
    url(r"^diff_whitelist$", "diff_whitelist", name="diff-whitelist"),
    url(r"^do_import$", "do_import", name="do-import"),
    url(r"^do_backup$", "do_backup", name="do-backup"),
    url(r"^generate_collection$", "generate_collection", name="generate-collection"),
    url(r"^push_artists$", "push_artists", name="push-artists"),
)
