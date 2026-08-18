# TODO

Known gaps between this specification and the reference implementations.

## Implement the redaction profile (xr:, section 9.2.1)

Specified, not implemented. Needed: composer support for ((...)) marking in
m: and in field values; the wire transform (block-character runs in m:,
deletion inside values); PBKDF2-HMAC-SHA256 key derivation (salt
"xprs-xr" || nonce, 100000 iterations, first 16 bytes); AES-128-CTR with
the 12-byte nonce and 32-bit big-endian counter from zero; base64url
framing; the packet-order line rule on reassembly (one bare line per bar
run, field runs first then m: runs, exact character-count match and a
post-substitution type check); bar-stripping in every value parser
(section 4.3 amendment); the -> sentinel as the sole success test; the
permitted-fields table enforced on composition and on restoration.
Default passphrase is sixteen number signs. Done when the section 9.2.1
worked packet (fixed nonce 000102030405060708090a0b) round-trips in the
implementation and the corpus wire decrypts to 223 / 393 / Max / pier2.
