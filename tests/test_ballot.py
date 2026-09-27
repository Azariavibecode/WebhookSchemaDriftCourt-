import hashlib, json
from pathlib import Path
import pytest

ROOT = Path(__file__).parents[1]
OWNER, REPO, COMMIT, TREE = "Azaria723", "WebhookSchemaDriftCourt", "a" * 40, "b" * 40
SLOTS = ["BEFORE_SCHEMA", "AFTER_SCHEMA", "CONSUMER_CONTRACT"]
BODIES = {"/" + str(p.relative_to(ROOT)).replace("\\", "/"): p.read_bytes() for p in (ROOT / "fixtures").rglob("*") if p.is_file()}
sha = lambda body: hashlib.sha256(body).hexdigest()
blob = lambda body: hashlib.sha1((f"blob {len(body)}\0").encode() + body).hexdigest()

def source(path, digest=None):
    return json.dumps({"owner": OWNER, "repo": REPO, "commit": COMMIT, "path": path, "digest": digest or sha(BODIES[path])})

def deploy(vm, direct_deploy, actor):
    vm.strict_mocks = True; vm.check_pickling = True
    with vm.prank(actor): return direct_deploy("contracts/WebhookSchemaDriftCourt.py")

@pytest.fixture
def setup(direct_vm, direct_deploy, direct_alice):
    return direct_vm, deploy(direct_vm, direct_deploy, direct_alice), direct_alice

def paths(name):
    base = f"/fixtures/{name}"
    return [base + "/before.json", base + "/after.json", base + "/consumer.md"]

def register(contract, event="payment.completed", pointer="/data/customer/id"):
    return contract.register_case(event, pointer, "The provider schema revision may break the documented consumer dependency at the exact registered pointer.")

def bind(contract, case_id, scenario, override=None):
    for slot, path in zip(SLOTS, paths(scenario)):
        assert contract.bind_snapshot(case_id, slot, source(path, override if slot == "BEFORE_SCHEMA" else None)) == "SNAPSHOT_BOUND"

def mock_sources(vm, scenario, truncated=False, missing=None):
    selected = paths(scenario)
    api = f"https://api.github.com/repos/{OWNER}/{REPO}"
    tree = [{"path": p[1:], "type": "blob", "mode": "100644", "size": len(BODIES[p]), "sha": blob(BODIES[p])} for p in selected]
    vm.mock_web((api + "/git/commits/" + COMMIT).replace(".", r"\.") + "$", {"status": 200, "body": json.dumps({"sha": COMMIT, "tree": {"sha": TREE}}).encode()})
    vm.mock_web((api + "/git/trees/" + TREE + r"\?recursive=1$").replace(".", r"\."), {"status": 200, "body": json.dumps({"truncated": truncated, "tree": tree}).encode()})
    for path in selected:
        vm.mock_web((f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{COMMIT}{path}").replace(".", r"\.") + "$", {"status": 404 if path == missing else 200, "body": BODIES[path]})

def result(verdict, reason, compatible, depends, migration, same=True, case_id=0, confidence="HIGH"):
    return json.dumps({"backward_compatible": compatible, "case_id": case_id, "confidence": confidence,
                       "consumer_depends_on_target": depends, "migration_documented": migration,
                       "reason_code": reason, "same_event": same, "verdict": verdict})

def prepared(vm, contract, scenario, event="payment.completed", pointer="/data/customer/id", digest=None):
    case_id = register(contract, event, pointer)
    bind(contract, case_id, scenario, digest)
    assert contract.seal_case(case_id) == "ASSESSABLE"
    mock_sources(vm, scenario)
    return case_id

def test_breaking_removed_field(setup):
    vm, contract, _ = setup; prepared(vm, contract, "removed-field")
    vm.mock_llm(r"Judge one webhook compatibility.*", result("BREAKING_CHANGE", "FIELD_REMOVED", False, True, False))
    assert contract.assess_case(0) == "BREAKING_CHANGE"
    assert json.loads(contract.get_case(0))["state"] == "ASSESSED"

def test_compatible_additive_field(setup):
    vm, contract, _ = setup; prepared(vm, contract, "additive-optional", pointer="/data/customer_id")
    vm.mock_llm(r"Judge one webhook compatibility.*", result("COMPATIBLE", "SEMANTICALLY_EQUIVALENT", True, True, False))
    assert contract.assess_case(0) == "COMPATIBLE"

def test_type_narrowing_breaks_consumer(setup):
    vm, contract, _ = setup; prepared(vm, contract, "type-narrowing", "shipment.updated", "/data/status")
    vm.mock_llm(r"Judge one webhook compatibility.*", result("BREAKING_CHANGE", "ENUM_CONTRACT_BROKEN", False, True, False))
    assert contract.assess_case(0) == "BREAKING_CHANGE"

def test_documented_migration(setup):
    vm, contract, _ = setup; prepared(vm, contract, "ambiguous-migration", "account.changed", "/data/owner_id")
    vm.mock_llm(r"Judge one webhook compatibility.*", result("MIGRATION_REQUIRED", "MIGRATION_PATH_REQUIRED", False, True, True, confidence="MEDIUM"))
    assert contract.assess_case(0) == "MIGRATION_REQUIRED"

@pytest.mark.parametrize("failure", ["bad_digest", "truncated", "missing"])
def test_source_failures_fail_closed(setup, failure):
    vm, contract, _ = setup
    bad = "0" * 64 if failure == "bad_digest" else None
    register(contract); bind(contract, 0, "removed-field", bad); contract.seal_case(0)
    mock_sources(vm, "removed-field", truncated=failure == "truncated", missing=paths("removed-field")[0] if failure == "missing" else None)
    assert contract.assess_case(0) == "SOURCE_UNVERIFIED"

@pytest.mark.parametrize("payload", [
    result("BREAKING_CHANGE", "FIELD_REMOVED", True, True, False),
    result("BREAKING_CHANGE", "FIELD_REMOVED", False, False, False),
    result("COMPATIBLE", "SEMANTICALLY_EQUIVALENT", False, True, False),
    result("MIGRATION_REQUIRED", "MIGRATION_PATH_REQUIRED", False, True, False),
    result("BREAKING_CHANGE", "FIELD_REMOVED", False, True, False, case_id=99),
    '{"verdict":"BREAKING_CHANGE"}'
])
def test_malformed_or_unsafe_consensus_output_fails_closed(setup, payload):
    vm, contract, _ = setup; prepared(vm, contract, "removed-field")
    vm.mock_llm(r"Judge one webhook compatibility.*", payload)
    assert contract.assess_case(0) == "SOURCE_UNVERIFIED"

def test_slot_completeness_locking_and_replay(setup):
    vm, contract, _ = setup; register(contract)
    assert contract.seal_case(0) == "SNAPSHOTS_INCOMPLETE"
    bind(contract, 0, "removed-field")
    assert contract.bind_snapshot(0, "BEFORE_SCHEMA", source(paths("removed-field")[0])) == "SLOT_ALREADY_BOUND"
    assert contract.seal_case(0) == "ASSESSABLE"
    assert contract.bind_snapshot(0, "AFTER_SCHEMA", source(paths("removed-field")[1])) == "CASE_LOCKED"
    mock_sources(vm, "removed-field")
    vm.mock_llm(r"Judge one webhook compatibility.*", result("BREAKING_CHANGE", "FIELD_REMOVED", False, True, False))
    assert contract.assess_case(0) == "BREAKING_CHANGE"
    before = contract.get_counts(); assert contract.assess_case(0) == "CASE_NOT_ASSESSABLE"; assert contract.get_counts() == before

def test_invalid_inputs_and_object_identity(setup):
    _, contract, _ = setup
    assert contract.register_case("x", "/data/id", "A sufficiently long allegation that should still fail the invalid event token.") == "INVALID_CASE"
    assert contract.register_case("payment.completed", "bad", "A sufficiently long allegation that should still fail the invalid pointer.") == "INVALID_CASE"
    assert contract.bind_snapshot(99, "BEFORE_SCHEMA", "{}") == "CASE_NOT_FOUND"
    register(contract)
    assert contract.bind_snapshot(0, "UNKNOWN", source(paths("removed-field")[0])) == "INVALID_SLOT"
    assert contract.bind_snapshot(0, "BEFORE_SCHEMA", "{}") == "INVALID_SOURCE"

def test_prompt_injection_is_data(setup):
    vm, contract, _ = setup; prepared(vm, contract, "removed-field")
    vm.mock_llm(r"Judge one webhook compatibility.*", result("BREAKING_CHANGE", "FIELD_REMOVED", False, True, False))
    assert contract.assess_case(0) == "BREAKING_CHANGE"
