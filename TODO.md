# TODO

Known gaps between this specification and the reference implementations.

## Update the Dart signer to use the XPRS tag strings

The specification (XPRS.md section 9.1.2) defines the tagged-hash domain
strings as `XPRS/nonce` and `XPRS/challenge`. The shipping Dart signer still
uses the older strings `APRX/nonce` and `APRX/challenge`, so signatures it
produces do not verify under the spec's algorithm and spec-computed
signatures (including the worked example and corpus wire) read as forged to
it.

Where: `reticulum-dart/lib/src/util/aprx_sign.dart`, three occurrences --
the nonce derivation in `sign()` and the challenge computation in both
`sign()` and `verify()`.

Side effects to plan for, not discover:

- Every signature stored before the cut (spooled wires in the XPRS archive,
  carried mail, corpus-independent test data) flips from verified to forged
  under the new tags. The archive drops forged packets at flush and the
  courier drops forged carried mail, so old signed data is not merely
  unbadged, it is discarded.
- The ESP32 station transmits unsigned and its codec does not verify, so
  firmware is unaffected.

Recommended cut: sign with the new tags immediately; verify new-tag first
and fall back to the old tags for a transition window, so stored and
in-flight signatures stay valid while the fleet updates; remove the fallback
once nothing old remains. Alternatively, as a pre-release protocol, cut hard
and accept the loss of old signed test data.

Done when: the Dart signer and verifier use the XPRS strings, the aurora
signing tests pass against the spec's worked example (aux fixed to zero,
toy key d=7 must reproduce the section 9.1.2 values), and the corpus wire
verifies in the implementation.

## Implement the redaction profile (xr:, section 9.2.1)

Specified, not implemented. Needed: composer support for ((...)) marking in
m: and in field values; the wire transform (block-character runs in m:,
deletion inside values); PBKDF2-HMAC-SHA256 key derivation (salt
"xprs-xr" || nonce, 100000 iterations, first 16 bytes); AES-128-CTR with
the 12-byte nonce and 32-bit big-endian counter from zero; base64url
framing; the order-first line rule on reassembly (first N lines fill the N
bar runs, remaining key=value lines replace field values whole); the ->
sentinel as the sole success test. Default passphrase is sixteen number
signs. Done when the section 9.2.1 worked packet (fixed nonce
000102030405060708090a0b) round-trips in the implementation and the
corpus wire decrypts to Max / pier2 / pos=38.7223,-9.1393.
