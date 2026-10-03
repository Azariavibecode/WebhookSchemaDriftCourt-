# Threat model

- Mutable branch names are prohibited; sources require a 40-hex commit.
- Path traversal, encoded separators, ambiguous paths, truncated trees, wrong blobs, wrong byte sizes, and digest mismatches fail closed.
- Snapshot text is hostile data and is quoted inside the prompt; prompt injection cannot expand the output vocabulary.
- A slot cannot be replaced or duplicated, and no snapshot can be added after sealing.
- Missing slots prevent sealing; an unsealed or terminal case cannot be assessed.
- Returned case identity and every consequential boolean are consensus-bound.
- `COMPATIBLE` requires both `same_event=true` and `backward_compatible=true`; unrelated snapshots cannot receive a compatibility certificate.
- `BREAKING_CHANGE` and `MIGRATION_REQUIRED` have their own deterministic semantic gates.
- Malformed, contradictory, or unexpected AI output becomes `SOURCE_UNVERIFIED`.
- No deployer, creator, source author, GitHub owner, or repository receives privileged authority.

The contract does not claim runtime delivery behavior, production traffic impact, or business damages. It concludes only compatibility at the registered event and pointer from the three authenticated snapshots.
