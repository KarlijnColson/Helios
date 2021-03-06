# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf.urls import include, url, patterns
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings

from views import *

urlpatterns = None

urlpatterns = patterns('',
  (r'^autologin$', admin_autologin),
  (r'^testcookie$', test_cookie),
  (r'^testcookie_2$', test_cookie_2),
  (r'^nocookies$', nocookies),
  (r'^socialbuttons$', socialbuttons),
  (r'^stats/', include('helios.stats_urls')),

  # get randomness
  (r'^get-randomness$', get_randomness),

  # election shortcut by short name
  (r'^e/(?P<election_short_name>[^/]+)$', election_shortcut),
  (r'^e/(?P<election_short_name>[^/]+)/vote$', election_vote_shortcut),

  # vote shortcut
  (r'^v/(?P<vote_tinyhash>[^/]+)$', castvote_shortcut),

  # trustee login
  (r'^t/(?P<election_short_name>[^/]+)/(?P<trustee_email>[^/]+)/(?P<trustee_secret>[^/]+)$', trustee_login),

  # election
  (r'^elections/params$', election_params),
  (r'^elections/verifier$', election_verifier),
  (r'^elections/single_ballot_verifier$', election_single_ballot_verifier),
  (r'^elections/new$', election_new),
  (r'^elections/administered$', elections_administered),
  (r'^elections/voted$', elections_voted),

   url(r'^elections/(?P<election_uuid>[^/]+)', include('helios.election_urls')),
)

