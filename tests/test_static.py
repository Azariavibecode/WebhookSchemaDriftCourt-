from pathlib import Path

SOURCE = (Path(__file__).parents[1] / "contracts" / "WebhookSchemaDriftCourt.py").read_text(encoding="utf-8")

def test_runtime_storage_and_consensus_shape():
    assert SOURCE.startswith("# v0.2.16")
    assert "class Contract(gl.Contract):" in SOURCE
    assert "TreeMap[str, str]" in SOURCE
    assert "gl.eq_principle.prompt_comparative" in SOURCE
    assert "self.cases =" not in SOURCE and "self.snapshots =" not in SOURCE

def test_three_snapshot_ballot_is_not_prior_architecture():
    for term in ["BEFORE_SCHEMA", "AFTER_SCHEMA", "CONSUMER_CONTRACT", "SNAPSHOTS_INCOMPLETE", "ASSESSABLE"]:
        assert term in SOURCE
    for term in ["challenge_deadline", "submit_rebuttal", "revise_context", "SUPERSEDED", "parent_id"]:
        assert term not in SOURCE

def test_source_and_positive_gate_enforcement():
    for term in ["_blob_sha1(raw.body)", "hashlib.sha256(raw.body).hexdigest()", 'tree.get("truncated", True)', "breaking_gate", "migration_gate"]:
        assert term in SOURCE
