# Local verification

Run from the repository root:

```bash
python -m pytest -q
```

Verified on 2026-09-27: `19 passed`.

Coverage includes removed-field breaking change, optional additive compatibility, enum narrowing, documented migration, bad digest, truncated tree, missing source, malformed output, wrong object identity, every positive-verdict gate, slot completeness, duplicate slot, post-seal mutation, terminal replay, invalid case/source/slot, and hostile snapshot content.

StudioNet deployment and live lifecycle evidence remain pending a deployed contract address.
