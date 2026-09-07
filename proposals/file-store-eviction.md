# Proposal: file-store eviction under quota (extends §12.11)

Status: DRAFT for review. Prepared from a 50-node stress simulation of the
archiver constellation (app `test/xprs_scale_50_test.dart`,
`test/xprs_archiver_eviction_test.dart`), which surfaced what §12.11 does and
does not cover.

## What the simulation confirmed against the current spec

§12.11 governs the PACKET spool and it now holds in the reference station: a
large archiver over its byte quota evicts by class first, age second — the
spool before custody mail before declared mail, and declared mail (a `d:` for a
callsign whose `t:mailbox hold:` names this station) survives even when it is
the oldest thing in the store. (The reference implementation was age-only until
this pass; it now reads the class off `d:` + the `hold:` table, per §12.11.)

## The gap: hosted FILES are a second store, unmentioned by §12.11

§12.11 speaks only of packets. An archiver that also hosts content-addressed
files (§12.9.2, `serve:files`, `cmd:put`) keeps a SECOND store — the bytes
behind `file:` references — with its own capacity and its own eviction, and the
spec says nothing about how that store sheds load. In the field the file store
is where the bytes actually are (a picture is kilobytes to megabytes; a packet
is at most 250 bytes), so a quota policy that never mentions it is the one that
matters most.

Proposed as a new subsection.

### 12.11.1 When the FILE store is full

A file host's byte budget is the operator's (§30.3), and when it is full a
file must go. The order mirrors §12.11's classes, read off how the bytes came
to be held rather than off a packet:

1. **Cached bytes** a station fetched for its own reading and re-seeds as a
   convenience: the cheapest to lose, because the reference that names them is
   still resolvable from any other holder (§8.1, §12.9.2).
2. **Deposited bytes** a stranger pushed with `cmd:put` and this station
   accepted as custody: losing one costs a delivery someone else may still
   make, exactly as custody mail does.
3. **Declared bytes**: a file whose recipient declared this station as its
   mailbox (§9.12), a file the operator pinned, and the station's own content.
   The last dropped, and inside its `until:` it should not be.

Within a class the least recently served goes first (a file's read count is the
signal a packet's `ts:` is), and no file outlives its own `until:`. A host that
cannot accept a `cmd:put` without touching class 3 refuses it out loud,
`code:429`, with `m:try` naming a peer with room, exactly as §12.11 refuses
mail.

**The location index follows the bytes.** A holder advertises the files it
keeps as signed provider records (§12.9.2, §12.9.4); when it evicts a file it
lets that record expire rather than answering `q:have` for bytes it no longer
holds. A provider record is therefore soft state with a short `ttl`, refreshed
while the bytes are held and gone shortly after they are dropped, so the index
never points at an empty store. A reader that is redirected to a stale holder
falls back to the next holder the index names, the same `m:try` list a miss
already carries.

## Also observed, and NOT a spec change (implementation to-do)

§12.11's "refuse new mail with `code:429` rather than evict class 3" is
specified but the reference admission path does not yet refuse: it evicts in
class order and would reach class 3 only when classes 1 and 2 are exhausted.
The fix is admission-side (check the quota against class 3 before accepting),
not a spec change. Tracked in the app, not here.
