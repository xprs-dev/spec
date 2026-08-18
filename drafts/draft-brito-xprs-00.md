---
title: "XPRS: eXtended Packet Radio System"
abbrev: "XPRS"
category: exp

docname: draft-brito-xprs-00
submissiontype: independent
number:
date:
v: 3
keyword:
 - packet radio
 - mesh network
 - store and forward
 - delay tolerant
 - APRS

author:
 -
    fullname: Max Brito
    organization: xprs.dev
    email: maxbrito.x1@gmail.com

normative:

informative:
  XPRS-SPEC:
    title: "XPRS Specification, edition XPRS-2026"
    target: https://xprs.dev
  RFC9171:

--- abstract

XPRS is a text packet format for radio and mesh networks. It extends and
modernizes the Automatic Packet Reporting System (APRS) with proven
identity, custody-based store-and-forward delivery, content-addressed
files, operator-chosen indexers in place of a central backbone, and
bearer neutrality across LoRa, Bluetooth Low Energy, WiFi, HF/VHF/UHF,
wired networks and the internet. Every packet is at most 250 bytes of
key:value text, readable without a decoder. This document introduces the
format and specifies its core: the packet grammar, derived message
identifiers, signatures, relaying, and custody. The complete
specification, including files, indexers, gateways and partial
redaction, is maintained at xprs.dev and summarized here.

--- middle

# Introduction

APRS demonstrated that a small text packet, heard by everyone and
repeated by volunteers, is enough to build a live map of who is where,
doing what, needing what. Three decades of operating it also exposed its
limits: identity is asserted rather than proven, a missed packet is
gone, the internet side is one central system that sees every packet,
content stops at 67 characters, and the design assumes one band.

XPRS keeps the core idea and rebuilds those parts:

- Identity is proven. Packets are signed with a key the station holds;
  a licensed callsign can be bound to a key and proven on air.
- Delivery is tracked. Stations carry mail for absent peers in custody
  and hand it over against signed receipts; a station that was away
  asks for the traffic it missed.
- There is no central server. Stations publish to indexers they choose;
  indexers federate by exchanging directories, never content.
- Files of any size are carried by SHA-256 content address: described,
  located by asking who holds them, fetched in verified pieces, or sent
  inline when small.
- The format is bearer-neutral. The same packet travels LoRa, Bluetooth
  Low Energy, WiFi, amateur bands, wired networks and the internet,
  with airtime discipline owned per bearer.

No licence is needed on licence-free spectrum, with identity derived
from a keypair generated on the device. On amateur bands XPRS operates
under amateur rules: plain text, a government-issued callsign, no
ciphertext.

This document specifies the core of the format. The complete
specification with worked examples for every construct, and a
conformance corpus in which every example is a test fixture, is
maintained at xprs.dev {{XPRS-SPEC}}.

## Relationship to Delay-Tolerant Networking

XPRS shares the problem space of the Bundle Protocol {{RFC9171}}:
intermittent links, store-and-forward custody, and delivery to nodes
that are unreachable at send time. It differs in operating point: XPRS
packets are human-readable text bounded at 250 bytes, designed to fit
one LoRa frame or one Bluetooth Low Energy extended advertisement, and
the network's actors are ordinary pocket devices playing several roles
at once rather than provisioned infrastructure.

# Conventions and Terminology

{::boilerplate bcp14-tagged}

Station: one device speaking XPRS under a callsign.
Relay: a station that repeats a packet on the medium it heard it.
Carrier: a station holding a message in custody for an absent station.
Gateway: a station that republishes packets onto another network.
Indexer: a station that archives chosen depositors' publications and
answers queries.

# Packet Format

A packet is a sequence of key:value fields separated by exactly one
space, encoded in UTF-8, at most 250 bytes on every transport:

~~~
t:message f:X1QZ3N d:LISBOA ts:2026-08-08_14:26:40 m:net at eight
~~~

- A key is 1 to 8 characters, lowercase letters and digits, beginning
  with a letter, followed by ":".
- A value contains no space and is never empty.
- Field order is free, except that "t:" (the packet type) is first and
  "m:" (the human-readable message), when present, is last. Everything
  after "m:" is the message, so it may contain spaces and any
  punctuation without escaping.
- Every key has a declared value type, fixed by the specification and
  never transmitted. Every measurement carries its unit.
- An unknown key is skipped with its value; an unknown packet type is
  ignored; a value that does not match its declared type is skipped. A
  packet is never rejected as a whole because one field is malformed.
- Values are text. Compression is not used. Content that does not fit
  one packet is split into at most nine numbered parts; content that
  does not fit nine parts is carried as a file.

Packet types include message, observation (position, movement, weather,
telemetry), receipt, request, identity, file, command, result, channel,
service, mailbox, track, sos, warning, info, blog, status, and others
defined in {{XPRS-SPEC}}.

# Message Identifiers

Every packet has an identifier, and it is never transmitted. Both ends
compute it from the packet itself:

1. Take the packet as transmitted: the UTF-8 bytes on the wire.
2. Remove the "sig:" field and the "via:" field where present, deleting
   the key, its value, and the one space before the key.
3. Compute SHA-256 over the remaining bytes.
4. The identifier is the first 6 characters of the digest in lowercase
   hexadecimal.

A reply, receipt or reaction names the identifier of the packet it
refers to in "r:". Because the identifier is derived, a replayed or
relayed copy collapses onto the copy already held, which removes the
need for cursors, sequence numbers, and deduplication state.

# Signatures

Signing is the default. "sig:" carries a 48-byte short Schnorr
signature over secp256k1 in the classic (e, s) form: the challenge
truncated to 16 bytes and the full 32-byte scalar, encoded as exactly
60 characters of an APRS-safe base85 alphabet. The signature covers the
packet with "sig:" and "via:" removed: the same canonical form the
identifier is derived from, so relaying alters neither.

The digest is SHA-256 of the canonical text. The nonce is derived from
the private scalar, the digest and 32 bytes of fresh randomness through
a BIP-340-style tagged hash (tags "XPRS/nonce" and "XPRS/challenge").
The scheme is deliberately not interoperable with BIP-340 verifiers:
truncating the challenge to the 128-bit security level is what makes a
secp256k1 signature fit a packet with room left for content.

A receiver MUST accept unsigned packets: the network carries traffic
from sensors with no key. What a receiver must never do is present an
unsigned packet as though its origin were established.

# Relaying and Custody

A relay forwards a packet only while "via:" holds fewer callsigns than
the limit for its type: nine relays for sos and warning, three for
everything else. The relay appends its callsign to "via:". A station
that finds its own callsign in "via:" does not relay; a relay drops a
packet whose identifier it has relayed within the last few minutes; and
a station waits a short random moment before re-airing, dropping its
copy if it hears the packet again during the wait.

A carrier holding a message for an unreachable station stores it under
quota, carries it physically or waits, and hands it over when it can.
Delivery is acknowledged with a signed receipt naming the message's
identifier; the receipt releases held copies everywhere it is heard.
"scope:" bounds how far a packet may travel (local, country, or global)
and binds gateways; a local packet is never carried off its bearers and
never republished.

A station back from days away asks any station holding a spool
(advertised as serve:history) to re-air what it kept, bounded by a time
window; replayed packets are the originals, unchanged, and duplicates
collapse on their identifiers.

# Further Mechanisms

The complete specification {{XPRS-SPEC}} additionally defines: files of
any size by SHA-256 content address, with piece-wise verification,
folder listings, an inline lane for files under about 900 bytes, and a
deterministic bridge to BitTorrent; gateways that publish which
radio-only stations they hear, making them reachable through an indexer
without any central registry; indexer federation by directory exchange,
never content; working-channel negotiation, moving a long transfer off
the shared calling channel with an invitation, acceptance, and an
arrival confirmation; and partial redaction, where marked spans of a
packet become visible bars recoverable with a passphrase, while parsers
read the remaining coarse value.

# Editions

The specification is edited continuously and released by year: the
current edition is XPRS-2026, and the first change made in a later year
opens the next edition and freezes this one. Interoperability across
editions rests on the reading rules: unknown keys and words are skipped
rather than rejected.

# Security Considerations

The signature scheme is a non-standard short Schnorr form; its 128-bit
challenge truncation is a deliberate trade of interoperability for
packet fit, and it uses the same secp256k1 key that stands behind the
station's callsign. Unsigned packets are accepted by design and must be
presented as unverified. Redaction bars leak the length of hidden
content by design; authors who must hide length pad before marking. The
redaction profile's default passphrase provides obfuscation against
automated harvesting, not secrecy, and the specification states this
plainly. Mailbox declarations, group grants and channel invitations are
acted on only when signed, because each is an instruction that would
otherwise let a stranger redirect mail, membership or a rendezvous.

# IANA Considerations

This document has no IANA actions. The format maintains its own
registries of packet types, keys and vocabulary words in {{XPRS-SPEC}};
unknown entries are skipped by rule, so registration is a matter of
documentation rather than interoperability.

--- back

# Acknowledgments
{:numbered="false"}

XPRS builds on the operating experience of the APRS network and its
community.
