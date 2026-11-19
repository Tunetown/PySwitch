# Observed Axe-Fx III firmware labels

This small follow-up to #294 names three complete identity responses captured
on the contributor's Mark II: 33.00 beta 5 (26 October 2026), official 33.00
(30 October) and official 33.01 (31 October). The status UI uses the label from
the complete response fingerprint, including the build date, instead of
mistaking the beta's raw version fields for a generic 97.00 release.

An unknown valid response keeps the previous raw major/minor display. A bad
checksum, unrelated function or malformed response is not a firmware label.
The fixtures contain identity bytes only, not firmware binaries or preset data.

## Deliberately not a write release

Recognition does not detect Mark I versus Mark II, alias a beta to a release,
select editor metadata, copy a parameter catalog or enable a writer. Both
existing explicit Amp writers retain their original full-response fingerprints.
The read-only output boundary and generic device capabilities are unchanged.
Official 33.00/33.01 replies still fail both existing write experiments.

This port has offline tests, including one-byte mutations with repaired
checksums, read-only connection tests, and rejection by both existing writers.
The identity fixtures come from earlier independent Mark II captures. No new
hardware session was performed for this extraction; a native run of this exact
upstream port and physical Mark I acceptance remain separate work.

Next slices can propose explicit, independently verified official-release
writers and scene-aware existing-preset editing without treating a display
label as permission. #270 remains the overall implementation reference.
