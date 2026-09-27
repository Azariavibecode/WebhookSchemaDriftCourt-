# Architecture

Each case binds one event type, JSON pointer, allegation, and exactly three source slots. Slot insertion is idempotence-protected and membership freezes at `seal_case`. There is no time-based coordination and no party-specific authority.

Before semantic judgment, every validator retrieves and verifies each GitHub commit, non-truncated recursive tree, exact path entry, blob mode and size, recomputed Git blob SHA-1, raw content, and SHA-256 commitment. Any failure produces `SOURCE_UNVERIFIED`.

Comparative consensus returns a closed JSON ballot containing object identity, verdict, reason, confidence, and four boolean findings. Deterministic gates reject internally inconsistent positive verdicts. Only a successful comparative result writes the terminal case and increments `assessed_count`; validator disagreement therefore rolls back atomically.

This differs structurally from challenge/rebuttal systems: the proof obligation is simultaneous compatibility reconciliation across a fixed triplet, not an allegation contested during a deadline.
