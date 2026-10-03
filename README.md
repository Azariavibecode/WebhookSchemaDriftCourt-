# WebhookSchemaDriftCourt

WebhookSchemaDriftCourt is a GenLayer Intelligent Contract that adjudicates one narrowly scoped webhook compatibility claim from three immutable GitHub snapshots: the schema before a change, the schema after it, and the consumer's documented dependency.

## Why GenLayer

JSON syntax can be compared deterministically, but compatibility depends on meaning: whether two representations describe the same event, whether a consumer actually relies on the changed pointer, and whether migration guidance makes an incompatible transition actionable. Comparative consensus decides only that bounded semantic question after the contract authenticates every source.

## Independent architecture

This project uses a three-snapshot compatibility ballot:

`REGISTERED → three fixed slots bound → ASSESSABLE → ASSESSED`

It has no challenge window, rebuttal, parent/child docket, recovery revision, or author allowlist. Once all slots are sealed, their membership is immutable. A terminal assessment cannot be replayed.

Slots:

- `BEFORE_SCHEMA`
- `AFTER_SCHEMA`
- `CONSUMER_CONTRACT`

Verdicts: `COMPATIBLE`, `BREAKING_CHANGE`, `MIGRATION_REQUIRED`, and fail-closed `SOURCE_UNVERIFIED`.

`COMPATIBLE` is accepted only when the before/after snapshots describe the same event and the change is backward-compatible. `BREAKING_CHANGE` is accepted only when the same event is being compared, the consumer depends on the target, and the change is not backward-compatible. `MIGRATION_REQUIRED` additionally requires documented migration guidance.

There is no owner, administrator, deployer privilege, trusted GitHub account, or repository allowlist. Any GitHub source is usable when its immutable commit, canonical tree entry, Git blob SHA-1, raw bytes, size, and SHA-256 commitment verify.

## Test

```bash
python -m pytest -q
```

Target runtime: GenLayer `0.2.16`; deployment target: StudioNet chain ID `61999`.

Replacement StudioNet contract: [`0x3FD9B3E4F28e299e4261B4c2D37D3d6CFAc45D87`](https://explorer-studio.genlayer.com/address/0x3FD9B3E4F28e299e4261B4c2D37D3d6CFAc45D87). Its deployed source is byte-for-byte identical to the patched repository source (`SHA-256 7cdd8d05a7249156cf8929c59038732cc593abf0a68fd2be0ab2ea8f5326454a`). See the [replacement StudioNet evidence](verification/studionet-verification.md).

See [architecture](docs/ARCHITECTURE.md), [threat model](docs/THREAT_MODEL.md), [fixture manifest](verification/fixture-manifest.md), and [local verification](verification/local-verification.md).
