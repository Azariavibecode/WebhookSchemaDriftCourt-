# Steward remediation

The `COMPATIBLE` ballot gate now requires both:

- `same_event == true`
- `backward_compatible == true`

An unrelated before/after event pair can therefore never receive a terminal compatibility certificate merely because it was labeled backward-compatible by the semantic evaluator. Invalid output fails closed to `SOURCE_UNVERIFIED`.

Regression coverage: `test_compatible_requires_same_event` supplies an otherwise well-formed `COMPATIBLE` ballot with `backward_compatible=true` and `same_event=false`; the contract rejects it and stores `SOURCE_UNVERIFIED`. The complete Direct Mode suite passes `20/20`.

Replacement deployment `0x3FD9B3E4F28e299e4261B4c2D37D3d6CFAc45D87` matches this contract source byte-for-byte at SHA-256 `7cdd8d05a7249156cf8929c59038732cc593abf0a68fd2be0ab2ea8f5326454a`. A fresh compatible lifecycle finalized on case `5`, and terminal replay preserved the committed verdict and counters. See `studionet-verification.md`.
