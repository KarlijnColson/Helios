from workflows import homomorphic
from models import *
import uuid

NUM_VOTERS = 1000
ELECTION_UUID = '90386511-cd2b-11e3-bf34-040cced8b6a0'

election = Election.objects.filter(uuid=ELECTION_UUID)

for i in range(0, NUM_VOTERS):
    voter_uuid = str(uuid.uuid4())
    voter = Voter(uuid=voter_uuid, voter_name='Test Voter ' + i, voter_login_id='test-' + i, election=election)
    voter.generate_password()
    voter.save()

    ev = homomorphic.EncryptedVote.fromElectionAndAnswers(election, [[1]])
    encrypted_vote = ev.ld_object.includeRandomness().toJSONDict()

    vote_fingerprint = cryptoutils.hash_b64(encrypted_vote)

    vote = datatypes.LDObject.fromDict(utils.from_json(encrypted_vote), type_hint='legacy/EncryptedVote').wrapped_obj

    # prepare the vote to cast
    cast_vote_params = {
        'vote': vote,
        'voter': voter,
        'vote_hash': vote_fingerprint,
        'cast_at': datetime.datetime.utcnow()
    }

    cast_vote = CastVote(**cast_vote_params)
    cast_vote.save()
