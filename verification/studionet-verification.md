# Replacement StudioNet verification — 2026-10-03

Network: StudioNet (`61999`)

Contract: [`0x3FD9B3E4F28e299e4261B4c2D37D3d6CFAc45D87`](https://explorer-studio.genlayer.com/address/0x3FD9B3E4F28e299e4261B4c2D37D3d6CFAc45D87)

## Submitted/deployed source parity

- Deployed source SHA-256: `7cdd8d05a7249156cf8929c59038732cc593abf0a68fd2be0ab2ea8f5326454a`
- Local patched source SHA-256: `7cdd8d05a7249156cf8929c59038732cc593abf0a68fd2be0ab2ea8f5326454a`
- Exact comparison: `true`
- Initial state: `{"assessed_count":0,"case_count":0,"sealed_count":0}`

This replacement contains the steward-requested gate: a `COMPATIBLE` ballot is accepted only when both `same_event` and `backward_compatible` are true.

## Fresh valid COMPATIBLE lifecycle

The active evidence revision is [`Azariavibecode/WebhookSchemaDriftCourt-@fac73b8`](https://github.com/Azariavibecode/WebhookSchemaDriftCourt-/tree/fac73b836c0d2239ac7001159afc0c227f816c03/fixtures/additive-optional). Every transaction below finalized with `MAJORITY_AGREE`.

| Step | Actor | Transaction |
|---|---|---|
| Register case `5` | wallet B | [`0x95c44f9614d99af37cf181d13abf1653da4e21b5a5da86f280e7d44f8d227dc2`](https://explorer-studio.genlayer.com/transactions/0x95c44f9614d99af37cf181d13abf1653da4e21b5a5da86f280e7d44f8d227dc2) |
| Bind before schema | wallet B | [`0x12f02c5f07cfd9217f3f1f820107d55b15356683e67f4c124282b2cd982308d1`](https://explorer-studio.genlayer.com/transactions/0x12f02c5f07cfd9217f3f1f820107d55b15356683e67f4c124282b2cd982308d1) |
| Bind after schema | wallet A | [`0x0c44940ea2fc60739b84c2c4ac656614e9291d08a499e9a4f7190f77e13a53bb`](https://explorer-studio.genlayer.com/transactions/0x0c44940ea2fc60739b84c2c4ac656614e9291d08a499e9a4f7190f77e13a53bb) |
| Bind consumer contract | wallet B | [`0xe7e88d9e06b7dbcf6228f5e02ca475ceec49e9ad28508eacb60f818274622baf`](https://explorer-studio.genlayer.com/transactions/0xe7e88d9e06b7dbcf6228f5e02ca475ceec49e9ad28508eacb60f818274622baf) |
| Seal immutable ballot | wallet A | [`0xca7c5ae08e67ce2aa7733096efda73b7f2a03ae004aa0bab6ae4de2dfa4ecdf3`](https://explorer-studio.genlayer.com/transactions/0xca7c5ae08e67ce2aa7733096efda73b7f2a03ae004aa0bab6ae4de2dfa4ecdf3) |
| Assess compatibility | wallet A | [`0x96af0c61bea7d2b0044c83f386c878e76bfc6be903a5c499ed5e952d54bb2edf`](https://explorer-studio.genlayer.com/transactions/0x96af0c61bea7d2b0044c83f386c878e76bfc6be903a5c499ed5e952d54bb2edf) |

Canonical `get_case(5)` readback is `ASSESSED / COMPATIBLE / HIGH / CONSUMER_NOT_AFFECTED`. Because the deterministic gate rejects `COMPATIBLE` unless `same_event=true && backward_compatible=true`, this verdict cannot arise from the prohibited `same_event=false` ballot. Direct Mode separately injects exactly that hostile ballot and proves it becomes `SOURCE_UNVERIFIED`.

## Adversarial and failure evidence

- Terminal replay by wallet B: [`0xc226a6116f961ef3eb28562b58de5548803bc2c91bc16e80f70a7db72106a5c7`](https://explorer-studio.genlayer.com/transactions/0xc226a6116f961ef3eb28562b58de5548803bc2c91bc16e80f70a7db72106a5c7), finalized `MAJORITY_AGREE`. Counts remained `8/8/8` and case `5` remained unchanged.
- Intentionally wrong source digest, case `7`: [`0x44fc8e09fbc2f6ccbc46912b7b2306e417349536af2ddeae769d629104f34f4b`](https://explorer-studio.genlayer.com/transactions/0x44fc8e09fbc2f6ccbc46912b7b2306e417349536af2ddeae769d629104f34f4b), committed `SOURCE_UNVERIFIED / SOURCE_INTEGRITY_FAILURE`.
- Post-seal mutation guard: [`0xe76dcdc8e0f916232254a4d9164676bb65ec7a7d326cafdc1ac62bb811347b5c`](https://explorer-studio.genlayer.com/transactions/0xe76dcdc8e0f916232254a4d9164676bb65ec7a7d326cafdc1ac62bb811347b5c), no counter mutation.
- Missing-case guard: [`0xb799ebd72a6e70af590efbbedf4c8e9dc264edb31f669fa0b3f2f55c4cbf6675`](https://explorer-studio.genlayer.com/transactions/0xb799ebd72a6e70af590efbbedf4c8e9dc264edb31f669fa0b3f2f55c4cbf6675), no counter mutation.
- Invalid-case guard: [`0x570ae829e1641467e93e6e84c097c498fec5a037bc89fecb88c8960ba6e3e55d`](https://explorer-studio.genlayer.com/transactions/0x570ae829e1641467e93e6e84c097c498fec5a037bc89fecb88c8960ba6e3e55d), no counter mutation.

The original fixture repository became unavailable and produced four fail-closed `SOURCE_UNVERIFIED` records (`0–3`). With the active revision, cases `4` and `6` encountered temporary source retrieval failure and remained `SOURCE_UNVERIFIED`; they are not represented as positive verdicts. Case `5` is the successful compatible control and case `7` is the intentional integrity-failure control.
