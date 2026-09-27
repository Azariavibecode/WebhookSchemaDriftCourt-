# StudioNet verification

Verified on 2026-09-27 on GenLayer StudioNet, chain ID `61999`.

- Contract: [`0xD0811B9873d579fAA18B64a9b47fF2BC6e0aEe31`](https://explorer-studio.genlayer.com/address/0xD0811B9873d579fAA18B64a9b47fF2BC6e0aEe31)
- Deployed and repository source SHA-256: `a037b87b77dc1d865782186c3e2268007a9499513eeb8ee2edc044f3981b8c93`
- Source parity: **exact byte-for-byte match**
- Test role A: `0x67A1A08Fc4cf7D05c859d0d3D8398a3A30B1677e`
- Test role B: `0x7C87B10a3d43F3b3551414401F8b26B9F662bAB5`

Final authoritative counters:

```json
{"assessed_count":4,"case_count":4,"sealed_count":4}
```

| Case | Expected branch | Verdict | Confidence | Reason | Assessment transaction |
|---:|---|---|---|---|---|
| 0 | Removed required field | `BREAKING_CHANGE` | `HIGH` | `FIELD_REMOVED` | [`0x4710…80ba`](https://explorer-studio.genlayer.com/tx/0x47106103b74c62441d6561dfdeb0dec7123efc232c989b110f18dbcd042080ba) |
| 1 | Additive optional field | `COMPATIBLE` | `HIGH` | `CONSUMER_NOT_AFFECTED` | [`0xa124…0e20`](https://explorer-studio.genlayer.com/tx/0xa1242fa416a3a01e58ec6e588bdf025ed9ad1d9c6a108e08001f01fc16ec0e20) |
| 2 | Documented pointer migration | `MIGRATION_REQUIRED` | `HIGH` | `MIGRATION_PATH_REQUIRED` | [`0xb360…68c0`](https://explorer-studio.genlayer.com/tx/0xb360c913118ef9dabccdd7b4ea48c9b6c697762aac1f3fe55daa2065602f68c0) |
| 3 | Incorrect source digest | `SOURCE_UNVERIFIED` | `LOW` | `SOURCE_INTEGRITY_FAILURE` | [`0x98be…54c5`](https://explorer-studio.genlayer.com/tx/0x98beb77e1df99700fab1676599321b468af824dfc7209910988a5b3df01b54c5) |

## Lifecycle anchors

| Action | Transaction | Effect |
|---|---|---|
| Register breaking case | [`0x5d71…f00d`](https://explorer-studio.genlayer.com/tx/0x5d713cd996f81c9c6bbc5c5a12accf49a0a80cc2de035b93b3a3e5f5cf33f00d) | Case 0 registered by role A |
| Bind before schema | [`0x0625…47dd`](https://explorer-studio.genlayer.com/tx/0x062505107012143e7d102753ded49acda9ea992fdc2ac7a478f5141428e747dd) | Immutable slot binding |
| Bind after schema | [`0x5a7e…1f6c`](https://explorer-studio.genlayer.com/tx/0x5a7e5590c9d3ab2285d840e953fae95dd7ca6177a1ce90e3d93d0eeb62a91f6c) | Immutable slot binding |
| Bind consumer contract | [`0x9930…60d1`](https://explorer-studio.genlayer.com/tx/0x993024aece26ea46cf781303d1a903810034fd0b910822102c072c507b3660d1) | Completes fixed triplet |
| Seal case 0 | [`0x1e72…eeb5`](https://explorer-studio.genlayer.com/tx/0x1e722deaebde648eb70be22e50aa849df4a95d9a2746b5268207458c7c33eeb5) | Case becomes `ASSESSABLE` |

## Adversarial guards

All calls finalized with `MAJORITY_AGREE` and left counters unchanged.

| Guard | Transaction |
|---|---|
| Post-seal snapshot mutation | [`0x4321…4782`](https://explorer-studio.genlayer.com/tx/0x43213a420a197a8251b19eb6d97070bb2437f63405eddb96a403089d51c54782) |
| Missing case | [`0xd5d8…5613`](https://explorer-studio.genlayer.com/tx/0xd5d8fa098320ab184fbd23b92149263616d09de829bad9a5c40b90fe01b05613) |
| Invalid case input | [`0x7741…b975`](https://explorer-studio.genlayer.com/tx/0x7741de3d5adf132ab0b213e00092d2a531ef3c35f9446457fda6c78eb2cab975) |
| Terminal assessment replay | [`0x60f2…e334`](https://explorer-studio.genlayer.com/tx/0x60f26eae37d7033e27a80ec2e301b92bda4d21322b18b7d6b1cfccec0ee0e334) |

Runner: [`scripts/run_studionet_e2e.mjs`](../scripts/run_studionet_e2e.mjs). It resumes from authoritative contract state, records `resultName`, accepts wallet credentials only through stdin, and never persists them.
