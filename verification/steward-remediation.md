# Steward remediation

The `COMPATIBLE` ballot gate now requires both:

- `same_event == true`
- `backward_compatible == true`

An unrelated before/after event pair can therefore never receive a terminal compatibility certificate merely because it was labeled backward-compatible by the semantic evaluator. Invalid output fails closed to `SOURCE_UNVERIFIED`.

Regression coverage: `test_compatible_requires_same_event` supplies an otherwise well-formed `COMPATIBLE` ballot with `backward_compatible=true` and `same_event=false`; the contract rejects it and stores `SOURCE_UNVERIFIED`. The complete Direct Mode suite passes `20/20`.

The old StudioNet address is explicitly marked historical because deployed-source parity would be false after this patch. Before resubmission, deploy this exact contract source, verify byte-for-byte parity, and run a fresh compatible lifecycle plus an adversarial `same_event=false` case against the replacement address.
