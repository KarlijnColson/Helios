"""
Glue some events together
"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import translation
from django.conf import settings
import helios.views
import helios.signals

import views

# TODO This doesn't work for voters that are not also users
# TODO url is nog logic. Puts 'en-us' instead of 'en' or 'nl'

def vote_cast_send_message(user, voter, election, cast_vote, **kwargs):
    # Prepare the message
    if(translation.get_language() == 'nl'):
    	subject = "%s - Je hebt gestemd!" % election.name
	translation.active('nl')
    	body = """
	Je hebt succesvol een stem ingediend voor %s.

	Jouw stem is opgeslagen op:

 	   %s

	De verkiezings-info vind je op: 

	%s

	""" % (election.name, helios.views.get_castvote_url(cast_vote), helios.views.get_election_url(election))

    	if election.use_voter_aliases:
        	body += """
	Deze verkiezing gebruikt aliases om je stem geheim te houden.
	Youw kiezers alias is: %s
	""" % voter.alias

    	body += """
	--
	Helios
	"""
    else:
    	subject = "%s - Cast Vote" % election.name
	translation.active('en')
    	body = """
	You have successfully cast a vote in %s.

	Your ballot is archived at:

 	   %s

	The election URL is: 

	%s 

	""" % (election.name, helios.views.get_castvote_url(cast_vote), helios.views.get_election_url(election))

    	if election.use_voter_aliases:
        	body += """
	This election uses voter aliases to protect your privacy.
	Your voter alias is: %s
	""" % voter.alias

    	body += """
	--
	Helios
	"""

    # send it via the notification system associated with the auth system
    user.send_message(subject, body)

helios.signals.vote_cast.connect(vote_cast_send_message)


def election_tallied(election, **kwargs):
    pass

helios.signals.election_tallied.connect(election_tallied)
