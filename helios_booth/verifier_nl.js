// helper functions for verifying a ballot
// assumes all of Helios machinery is loaded

function verify_ballot(election_raw_json, encrypted_vote_json, status_cb) {
    var overall_result = true;
    try {
	election = HELIOS.Election.fromJSONString(election_raw_json);
	var ranking = false;
	if (election.election_type=='ranked election')
		ranking = true;
	var election_hash = election.get_hash();
	status_cb("De vingerafdruk van de verkiezing is " + election_hash);
	
	// display ballot fingerprint
	encrypted_vote = HELIOS.EncryptedVote.fromJSONObject(encrypted_vote_json, election);
	status_cb("Jouw verificatie-code was " + encrypted_vote.get_hash());
	
      // check the hash
      if (election_hash == encrypted_vote.election_hash) {
          status_cb("Vingerafdruk van de verkiezing matched met die van de stem.");
      } else {
          overall_result = false;
          status_cb("PROBLEEM = Vingerafdruk van de verkiezing matched niet.");          
      }
      
      // display the ballot as it is claimed to be
      if(election.election_type != 'ranked election'){
      status_cb("Inhoud van de stem:");
      _(election.questions).each(function(q, qnum) {
	      if (q.tally_type != "homomorphic") {
		  status_cb("WAARSCHUWING: Het resultaat voor dit type vraag is niet homomorf. Verificatie zou kunnen falen omdat deze enkel gemaakt is voor homomorfe vragen.");
	      }
        
	      var answer_pretty_list = _(encrypted_vote.encrypted_answers[qnum].answer).map(function(aindex, anum) {
		      return q.answers[aindex];
		  });
	      status_cb("Vraag #" + (qnum+1) + " - " + q.short_name + " : " + answer_pretty_list.join(", "));
      });
      }
      
      // verify the encryption
      if (encrypted_vote.verifyEncryption(election.questions, election.public_key, ranking)) {
          status_cb("Encryptie Geverifieerd. (Nog niet sluiten, verificatie is nog bezig.)");
      } else {
          overall_result = false;
          status_cb("PROBLEM = Encryption doesn't match. (Nog niet sluiten, verificatie is nog bezig.)");
      }
      
      // verify the proofs
      if (encrypted_vote.verifyProofs(election.public_key, function(ea_num, choice_num, result) {
      },ranking)) {
          status_cb("Bewijs is OK.");
      } else {
          overall_result = false;
          status_cb("PROBLEEM = Bewijs is niet OK");
      }
    } catch (e) {
      status_cb('probleem bij het lezen van de data, foute inputs: ' + e.toString());
      overall_result=false;
    }

    return overall_result;
}
