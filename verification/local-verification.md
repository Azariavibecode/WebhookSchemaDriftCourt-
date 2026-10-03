# Local verification

Run from the repository root:

```bash
python -m pytest -q
```

Verified after the steward-requested ballot hardening: `20 passed`.

Coverage includes removed-field breaking change, optional additive compatibility, the regression proving `same_event=false` cannot produce `COMPATIBLE`, enum narrowing, documented migration, bad digest, truncated tree, missing source, malformed output, wrong object identity, every positive-verdict gate, slot completeness, duplicate slot, post-seal mutation, terminal replay, invalid case/source/slot, and hostile snapshot content.

The matching deployment and live lifecycle are recorded in [StudioNet verification](studionet-verification.md).
