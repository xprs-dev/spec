# A Wikipedia article for XPRS

Draft text for an English Wikipedia article on XPRS, plus what a new account
has to do to get it published. The article itself is in wikitext (Wikipedia
does not use Markdown), in the block under "The article" below: paste it into
the Wikipedia editor as is.

Its shape follows the English Wikipedia article on APRS
(<https://en.wikipedia.org/wiki/Automatic_Packet_Reporting_System>), read on
2026-09-10: the closest existing article, and the one a reviewer will compare
this with. "What the APRS article teaches" below says what was taken from it
and what was deliberately not.

Facts as of 2026-09-10, edition XPRS-2026, Draft 10.

---

## Before you paste anything

### 1. A new account cannot publish this directly, and should not try

- **Article creation is gated.** A new account is not *autoconfirmed* until it
  is 4 days old and has made 10 edits, and until then it cannot create a page
  in the main article space. Even once it can, going straight to mainspace is
  the wrong move here (point 2).
- **Use Articles for Creation (AfC).** Start the page as
  `Draft:XPRS (protocol)` through the Article Wizard
  (<https://en.wikipedia.org/wiki/Wikipedia:Article_wizard>), paste the
  wikitext, preview, save, then press "Submit for review". An independent
  reviewer decides whether it moves to mainspace. The queue can take weeks to
  months.
- **Title.** "XPRS" is also the name of SATEL's XPRS radio router product
  line, so `XPRS (protocol)` avoids an ambiguity a reviewer would otherwise
  raise. A reviewer can rename it if they disagree.
- **Username.** A personal username is fine. A username that is the name of
  the project or an organisation ("XPRS", "xprs.dev") is not allowed and gets
  blocked on sight.

### 2. You have a conflict of interest, and you must say so

You wrote XPRS, so Wikipedia treats you as having a conflict of interest
(WP:COI). This is permitted, but only openly:

- Put a disclosure on your user page, e.g.
  `{{UserboxCOI|1=XPRS (protocol)}}`, or a sentence: "I am the author of the
  XPRS protocol and have a conflict of interest regarding the article
  Draft:XPRS (protocol)."
- Put `{{Connected contributor|User1=YourUsername|U1-declared=yes}}` on the
  draft's talk page (`Draft talk:XPRS (protocol)`).
- Submit through AfC (as above) rather than moving the page yourself.
- After it is published, do not edit the article directly beyond fixing
  obvious errors. Request changes on its talk page with `{{Edit COI}}` and let
  someone else make them.
- Do not add XPRS to other articles yourself, not to the APRS article's
  "See also", not to the `{{Packet radio}}` navigation box, not a link to
  xprs.dev anywhere. From a COI account that reads as promotion and is the
  fastest way to get the account blocked and the site blacklisted. If the
  article is accepted, suggest those links on the other articles' talk pages
  and let their editors decide.

### 3. Notability is the hard part, and today it is not met

This is the point most likely to decide the outcome, so it is stated plainly.

Wikipedia keeps an article only if the subject has received **significant
coverage in reliable sources independent of the subject** (WP:GNG). Every
source in the draft below is a primary source: the specification, the
project's website, its GitHub repositories. Those may be used to support
plain technical facts, but they do not count at all towards notability. A web
search on 2026-09-10 for "eXtended Packet Radio System" found no independent
coverage, and `draft-brito-xprs` is not yet on the IETF Datatracker.

The APRS article shows the same split. Its technical sections cite aprs.org,
the APRS protocol reference and aprs-is.net, all primary; what makes APRS
notable is what sits beside them: the *ARRL Handbook*, ARRL news coverage, and
a book published by the ARRL (Horzepa, *APRS Tracks, Maps and Mobiles*, 1999).
XPRS has the first kind of source and none of the second.

Submitted now, the draft will very probably be declined with "submission's
references do not show the subject qualifies". A decline is not a
punishment, you can resubmit, but repeated resubmission without new sources
gets a draft rejected outright.

What would change that, roughly in order of weight:

- An article in an independent publication with editorial control: QST
  (ARRL), RadCom (RSGB), CQ, a national amateur-radio society's journal,
  Hackaday, Ars Technica, a technology newspaper section.
- A paper in the TAPR Digital Communications Conference proceedings, or any
  peer-reviewed venue, especially if others then cite it. TAPR published the
  APRS protocol reference, and the APRS article cites a DCC seminar.
- Published discussion by others: a talk at a conference someone else
  organised, a review, a book chapter.
- An RFC from the Independent Submission stream. The Internet-Draft alone
  (anyone can post one) is a primary source and adds little; the RFC, which
  the Independent Submissions Editor reviews, is stronger but still needs
  secondary coverage alongside it.

Blogs, forum threads, Reddit, YouTube channels without editorial oversight,
press releases and anything you write yourself do not count.

Recommendation: keep this draft ready, and submit once two or three sources
of the first kind exist. Add them as references to the sentences they support
(the lead, "History" and "Reception" are where they belong) before
submitting.

### 4. Two more things reviewers check

- **Machine-written text.** Wikipedia removes unreviewed AI-generated pages
  quickly (speedy-deletion criterion G15), and reviewers look for it. This
  draft was prepared with Claude Code. Read every sentence, change anything
  that does not sound like you, and open every reference to confirm it says
  what the sentence claims. You answer for the text, not the tool.
- **Copying.** The article paraphrases the specification rather than quoting
  it. Keep it that way: long passages copied from xprs.dev trip the copyright
  checker even though the specification is BSD-licensed.

### 5. Things to verify before submitting

- The origin paragraph dates XPRS from the specification's first commit in
  its own repository, 18 August 2026. Correct it if the real story is longer,
  and add a source if one exists. The APRS article's History section is the
  model: who, on what, first used for what, and how the name came about, each
  with a date.
- When the Internet-Draft is posted, add it (a `{{cite IETF}}` reference) to
  the History section. Do not claim it exists before it does.
- Categories are disabled while the page is a draft (the `{{Draft categories}}`
  wrapper does this). Leave the wrapper in; the reviewer removes it on
  acceptance.

---

## What the APRS article teaches

### Taken from it

- **A short description that is a category, not a pitch.** APRS: "Amateur
  radio telemetry forwarding protocol". XPRS: "Packet radio messaging and
  position reporting protocol".
- **A picture where an infobox would be.** The APRS article has no infobox;
  it opens with a photograph of a beacon transmitter, and later shows a
  screenshot of client software with raw packets visible. The XPRS draft
  follows suit: no infobox, and a commented-out image line for a photo of a
  board running the firmware or a screenshot of the app. Upload it to
  Wikimedia Commons yourself as your own work under CC BY-SA 4.0, and keep
  anything with a third-party map or logo out of the frame.
- **A lead in four short paragraphs**: what it is and what it carries; how a
  packet gets around; who developed it and when; who looks after it now. The
  lead is a summary a reader can stop after.
- **"Network overview" before the packet details.** APRS explains the
  unconnected broadcast model, digipeaters, hop limits and IGates before it
  lists packet types, because the packet types only make sense once a reader
  knows how packets move. The draft does the same with relays, carriers,
  gateways and archivers.
- **Anticipate the reader's objection.** The best paragraph in the APRS
  article begins "While it would seem that using unconnected and unnumbered
  packets ... would result in poor reliability ... this is not the case,
  because ...". The draft uses that shape where XPRS is counter-intuitive:
  an identifier that is never transmitted, and a signature that survives
  relaying.
- **Concrete details over adjectives.** APRS gives the path string
  (`WIDE1-1,WIDE2-1`), the modem (1,200 bit/s Bell 202 AFSK) and a list of
  frequencies. The draft gives a real packet, its byte count, the 250-byte
  limit and the reason for it, and the TCP/UDP port.
- **Claims about intent are attributed.** "Bruninga has also stated that
  APRS was not meant to be a vehicle position tracking system". The draft
  says "the specification describes" or "according to the specification"
  wherever it reports why XPRS is the way it is, rather than asserting it in
  Wikipedia's voice.
- **"See also" in alphabetical order, each entry glossed in a few words.**
- **Only one category the article is plainly in** (APRS has just
  `Category:Packet radio`); the draft proposes three.

### Not taken from it

The APRS article is old and much edited, and it gets away with things a new
article from a COI account will not:

- **Sentences with no reference.** Its whole "Capabilities" section is
  unsourced. In the draft, every paragraph has a citation.
- **Editorialising.** "should not be overlooked", "the all-important PATH
  setting", "the robust network". The draft has no evaluative adjectives about
  XPRS at all; a reader decides whether it is robust.
- **How-to content.** "Recommended path" tells operators how to configure
  their stations, which Wikipedia is not for (WP:NOTHOWTO). The draft
  describes rules, never instructs.
- **Weak sources.** A tweet and a YouTube video carry facts there. The draft
  cites only the specification and the repositories, and says so.
- **A long external-links list** of software, maps and databases. The draft
  links the official site and the specification, nothing else.
- **A navigation box** (`{{Packet radio}}`). A navbox belongs on an article
  only when the box lists that article, and adding XPRS to the box is exactly
  the kind of edit point 2 rules out.
- **A Capabilities section at all.** For APRS it is backed by decades of
  use. For XPRS it would be a list of what the software could be used for,
  which reads as advertising; what XPRS carries is covered, factually, under
  "Packet types".

---

## The article

```wikitext
{{Short description|Packet radio messaging and position reporting protocol}}

<!-- [[File:XPRS firmware on a LoRa board.jpg|thumb|right|200px|A LoRa board running XPRS firmware as a relay station.]] -->

'''XPRS''' ('''eXtended Packet Radio System''') is a protocol for exchanging
short text packets between stations over radio, [[mesh networking|mesh
networks]] and the [[Internet]].<ref name="spec">{{cite web |last=Brito
|first=Max |title=XPRS, eXtended Packet Radio System
|url=https://xprs.dev/spec/ |website=xprs.dev |edition=XPRS-2026
|access-date=2026-09-10}}</ref> Packets can carry text messages,
[[Global Positioning System|GPS]] positions and tracks, [[weather station]]
readings, [[telemetry]], calls for help, warnings, polls, commands to remote
devices and references to files.<ref name="spec-packet">{{cite web |last=Brito
|first=Max |title=XPRS, eXtended Packet Radio System
|url=https://xprs.dev/spec/ |at=§4 Packet |website=xprs.dev
|access-date=2026-09-10}}</ref> The specification presents it as an extension
of the [[Automatic Packet Reporting System]] (APRS).<ref name="spec-purpose">{{cite
web |last=Brito |first=Max |title=XPRS, eXtended Packet Radio System
|url=https://xprs.dev/spec/ |at=§1 Purpose |website=xprs.dev
|access-date=2026-09-10}}</ref>

The same packet, at most 250 bytes of human-readable text, is used unchanged
on [[LoRa]], [[Bluetooth Low Energy]], [[Wi-Fi]], amateur HF, VHF and UHF
radio, wired networks and the Internet.<ref name="spec-packet" /> Any station
may repeat what it hears, hold messages for stations that are out of range and
deliver them later, or keep packets for others to retrieve. There is no
central server: each station chooses which others keep its
traffic.<ref name="spec-purpose" />

XPRS was developed by Max Brito and first published as a separate
specification in August 2026. Stations are identified by callsigns derived
from a [[public-key cryptography|cryptographic key]] generated on the device,
which allows the protocol to be used on licence-free spectrum without an
[[amateur radio licensing|amateur radio licence]]; on amateur bands, amateur
rules apply.<ref name="spec-callsigns">{{cite web |last=Brito |first=Max
|title=XPRS, eXtended Packet Radio System |url=https://xprs.dev/spec/
|at=§3 Callsigns |website=xprs.dev |access-date=2026-09-10}}</ref>

The specification is published at xprs.dev under the [[BSD licenses|BSD
3-Clause License]], and is revised in yearly editions, the first being
XPRS-2026.<ref name="readme">{{cite web |title=xprs-dev/spec: README
|url=https://github.com/xprs-dev/spec |website=[[GitHub]]
|access-date=2026-09-10}}</ref>

==History==
XPRS was developed by Max Brito. The specification and its conformance test
corpus were first published in their own repository on 18 August 2026,
alongside a messaging application for phones and desktops that implements
the format.<ref name="spec-repo">{{cite web |title=xprs-dev/spec: commit
history |url=https://github.com/xprs-dev/spec/commits/main
|website=[[GitHub]] |access-date=2026-09-10}}</ref>

The specification describes its motivation as the limits that three decades of
APRS operation had exposed: an APRS callsign is asserted rather than proven, a
packet that is missed is lost, the Internet side of the network depends on one
central system (APRS-IS), message text stops at 67 characters, and the
network is built around a single band. It gives the accumulation of APRS
encodings over time, among them several incompatible position formats and a
mixture of imperial and metric units, as the reason for adopting a single
syntax.<ref name="spec-purpose" />

The document is edited continuously and released by calendar year: changes
made during 2026 belong to the edition XPRS-2026, and the first change made in
a later year opens a new edition and freezes the previous one. Implementations
state the edition they read.<ref name="readme" />

==Network overview==
The specification describes the network in terms of roles rather than kinds of
equipment. One device usually performs several at once, each is volunteered by
its operator, and none is required:<ref name="spec-purpose" />

* a '''relay''' repeats a packet on the medium it heard it on and appends its
  callsign to the packet's <code>via:</code> field, within a hop limit, as an
  APRS [[digipeater]] does;
* a '''carrier''' holds a message for a station that is absent and hands it
  over when that station is heard again, in exchange for a signed receipt;
* a '''gateway''' passes traffic between XPRS and something that is not XPRS,
  such as an archiver on the Internet or APRS-IS, as an APRS IGate does;
* an '''archiver''' keeps packets it has heard, the publications of stations
  that chose it, and mail waiting for absent recipients, and answers requests
  for them;
* a '''file server''' holds files identified by their content hash and serves
  them in pieces.

The specification contrasts this with APRS, where a packet that is missed is
lost. XPRS adds [[store and forward]] custody: a carrier keeps its copy until a
receipt shows that the message arrived, and a station that was away can ask
for the traffic it missed.<ref name="spec-purpose" /> In place of APRS-IS, each
station deposits its traffic with archivers its operator chooses, or with
none. Archivers exchange directories of which station keeps what, rather than
copies of one another's traffic, so that no single archiver holds the whole
network.<ref name="spec-archiver">{{cite web |last=Brito |first=Max
|title=XPRS, eXtended Packet Radio System |url=https://xprs.dev/spec/
|at=§12 Archiver |website=xprs.dev |access-date=2026-09-10}}</ref>

Each transport is governed by its own airtime rules, and a station sending on
several is bound by the strictest of them; for LoRa in the [[ISM radio
band|ISM bands]] that is often a legal [[duty cycle]] of one per cent. The
specification allows a station to refuse or ration requests from strangers,
since answering one spends its own battery and airtime.<ref name="spec-airtime">{{cite
web |last=Brito |first=Max |title=XPRS, eXtended Packet Radio System
|url=https://xprs.dev/spec/ |at=§30 Airtime |website=xprs.dev
|access-date=2026-09-10}}</ref>

==Packet types==
Every packet declares its type in its first field, <code>t:</code>. The
specification defines about thirty types; types it does not list are reserved,
and a receiver ignores a type it does not know.<ref name="spec-packet" />

* '''Observations''' (<code>t:observation</code>) carry position, movement,
  weather and telemetry in one packet type. New kinds of data are added as new
  fields rather than new types, and every measurement carries its unit, such as
  <code>temp:14.2C</code> or <code>spd:48km/h</code>.<ref name="spec-rules">{{cite
  web |last=Brito |first=Max |title=XPRS, eXtended Packet Radio System
  |url=https://xprs.dev/spec/ |at=§2 Design rules |website=xprs.dev
  |access-date=2026-09-10}}</ref> Related types describe named tracks, places,
  and where a vessel is bound.
* '''Messages''' (<code>t:message</code>) go to one station, to a group, or to
  everyone in range, and can reply to, react to or quote an earlier packet.
  Text too long for one packet is split into numbered parts.<ref name="spec-packet" />
* '''Receipts and requests''' acknowledge delivery and ask a station for data
  it holds, such as a file or past traffic.
* '''Safety''' types are calls for help (<code>t:sos</code>), warnings about
  hazards and notices about conditions.
* '''Community''' types include status posts, polls, blog posts, events, and
  offers of and requests for goods or help.
* '''Station''' types include identity announcements, the frequencies a
  station uses, the services it offers, commands to remote devices and their
  results, and challenges that ask a station to prove its callsign on air.

Files are not sent inside ordinary packets. A packet refers to a file by its
[[SHA-2|SHA-256]] hash, and the file is then located by asking which stations
hold it and fetched in verified pieces; a file of a few bytes can be sent
inline.<ref name="spec-packet" />

==Identity and signatures==
A self-generated XPRS callsign is <code>X1</code> to <code>X5</code> followed
by two to five characters (four by default) taken from the [[Bech32]] encoding
of the holder's public key. The digit states what the callsign belongs to: a
person (X1), a moving station such as a vehicle or vessel (X2), a fixed
station or relay (X3), an automated device (X4) or a group (X5). No authority
issues or revokes these callsigns.<ref name="spec-callsigns" /> Because short
callsigns can collide, or be forged by generating keys until one matches, the
specification treats a callsign as a label and relies on signatures to
establish who sent a packet. A callsign issued by a national radio authority,
such as <code>CT1ABC-9</code>, is equally valid in the format and can be bound
to a key.<ref name="spec-callsigns" />

APRS's numeric suffixes are kept. A suffix such as <code>-9</code>
distinguishes one of an operator's devices from the others, and the suffixes
<code>-1</code> to <code>-15</code> keep their conventional APRS meanings; the
bare callsign addresses the person on whichever device is in
reach.<ref name="spec-callsigns" />

Although no packet carries an identifier field, every packet has one: each
station computes it as the first six hexadecimal characters of the SHA-256
hash of the packet, and replies and receipts refer to a packet by it. Because
the timestamp is part of the hashed text, two identical short messages sent a
second apart receive different identifiers.<ref name="spec-ids">{{cite web
|last=Brito |first=Max |title=XPRS, eXtended Packet Radio System
|url=https://xprs.dev/spec/ |at=§5 Message identifiers |website=xprs.dev
|access-date=2026-09-10}}</ref>

Stations sign packets by default, and a receiver accepts unsigned packets but
may not present their sender as established. The signature is a shortened
[[Schnorr signature]] over the [[secp256k1]] curve, 48 bytes written as 60
characters, which the specification notes is not compatible with
[[Bitcoin]]'s BIP-340 verifiers. It would seem that relaying, which adds the
relay's callsign to the packet, would invalidate a signature; it does not,
because the signature and the relay path are both removed before the packet is
signed or its identifier computed.<ref name="spec-sig">{{cite web |last=Brito
|first=Max |title=XPRS, eXtended Packet Radio System
|url=https://xprs.dev/spec/ |at=§6 Signing and privacy |website=xprs.dev
|access-date=2026-09-10}}</ref>

A message can be sealed so that only its recipient can read it. The sender,
recipient and time stay in clear text, which lets a carrier hold and route the
message without reading it. A separate redaction feature replaces chosen
words with block characters of the same length, which readers holding a
passphrase can restore.<ref name="spec-sig" />

==Technical information==
A packet is a list of <code>key:value</code> fields separated by single
spaces, with no binary framing, no positional fields and no escaping. The
type, <code>t:</code>, is always first, and the message text, <code>m:</code>,
is always last, so that it can contain spaces and any punctuation. A receiver
skips a key it does not know, and skips a field whose value is malformed
rather than rejecting the whole packet.<ref name="spec-packet" /> A direct
message reads:

<syntaxhighlight lang="text">
t:message f:X1QZ3N d:X1RD89 ts:2026-08-18_09:15:00 m:arrived at the marina
</syntaxhighlight>

where <code>f:</code> is the sender, <code>d:</code> the destination and
<code>ts:</code> the time of composition in [[Coordinated Universal
Time|UTC]].<ref name="spec" />

The 250-byte limit applies on every transport. It was chosen to fit in one
LoRa packet and one [[Bluetooth Low Energy|Bluetooth 5]] extended
advertisement; values are not compressed.<ref name="spec-packet" /> Numbers
always use a full stop as the decimal separator and no thousands separator,
because the comma already separates latitude from longitude and items in a
list.<ref name="spec-packet" /> As a flat list of names and values, a packet
converts directly to a [[JSON]] object.<ref name="spec" />

XPRS does not assign frequencies. A station announces the channels it uses in
a <code>t:channel</code> packet, which can also arrange for two stations to
move a long exchange off the shared channel.<ref name="spec-channels">{{cite
web |last=Brito |first=Max |title=XPRS, eXtended Packet Radio System
|url=https://xprs.dev/spec/ |at=§14 Channels |website=xprs.dev
|access-date=2026-09-10}}</ref> Over IP, a station listens on TCP and UDP port
4242, the port already used by hubs of the Reticulum network stack; one
listener tells the two protocols apart by the first byte it
receives.<ref name="spec-services">{{cite web |last=Brito |first=Max
|title=XPRS, eXtended Packet Radio System |url=https://xprs.dev/spec/
|at=§13.4 One port on an IP network |website=xprs.dev
|access-date=2026-09-10}}</ref>

==Relationship to APRS==
A licensed amateur may bridge XPRS and APRS under their own callsign. Traffic
from self-generated callsigns may not be originated onto amateur radio
infrastructure, because no authority assigned those callsigns, and
self-generated callsigns may not transmit on licensed spectrum at all.
Encrypted content is never passed to APRS, both because amateur rules forbid
obscuring the meaning of a transmission and because APRS is a seven-bit
protocol that would corrupt it.<ref name="spec-aprs">{{cite web |last=Brito
|first=Max |title=XPRS, eXtended Packet Radio System
|url=https://xprs.dev/spec/ |at=§32 Operating alongside APRS
|website=xprs.dev |access-date=2026-09-10}}</ref>

==Implementations==
The reference implementations are open-source software published under the
xprs-dev organisation on GitHub:<ref name="readme" />

* an application for [[Android (operating system)|Android]], [[Linux]] and
  [[Microsoft Windows|Windows]], written with [[Flutter (software)|Flutter]];
* firmware in C for low-cost [[ESP32]] and LoRa boards, which run as
  stations, relays and mailboxes;
* a networking library in [[Dart (programming language)|Dart]], which
  provides the mesh transport, file sharing and signature scheme.

The specification includes a conformance corpus: every example packet in the
document, with its length in bytes and its identifier. The Dart and C
implementations both replay it in their test suites.<ref name="readme" /> As of
September 2026 the specification's own implementation-status section lists a
number of features as specified but not yet implemented, among them signed
receipts by default, callsign suffixes for multiple devices, and publishing to
chosen archivers.<ref name="spec-status">{{cite web |last=Brito |first=Max
|title=XPRS, eXtended Packet Radio System |url=https://xprs.dev/spec/
|at=§37 Implementation status |website=xprs.dev |access-date=2026-09-10}}</ref>

==See also==
<!-- Please respect alphabetical order -->
* [[Automatic Packet Reporting System]], the amateur radio system XPRS extends
* [[AX.25]], the link-layer protocol APRS is carried on
* [[Delay-tolerant networking]], networking with intermittent links and store-and-forward delivery
* [[Meshtastic]], a LoRa mesh messaging project
* [[Packet radio]]

==References==
{{Reflist}}

==External links==
* {{Official website|https://xprs.dev}}
* [https://xprs.dev/spec/ XPRS specification]

{{Draft categories|
[[Category:Packet radio]]
[[Category:Mesh networking]]
[[Category:Network protocols]]
}}
```

---

## Notes on the wikitext

- **Claims about APRS are XPRS's claims.** Where the draft says what APRS
  lacks, it says "the specification contrasts" or "the specification
  describes", because the only source is the XPRS specification. Wikipedia
  does not accept its own APRS article as a source (WP:CIRCULAR). If you want
  those sentences in Wikipedia's own voice, cite the APRS Protocol Reference
  (TAPR, 2000) or the ARRL Handbook instead, as the APRS article does.
- **The image.** Uncomment the `[[File:...]]` line once a photo is on
  Wikimedia Commons, and change the filename and caption to match it.
- **No Reception section.** An article normally says how others received the
  subject, but there is nothing independent to cite yet. When sources exist,
  add `==Reception==` after "Implementations" and summarise them there; that
  section is what establishes notability.
- **Links.** Every wikilink, category and template in the draft was checked
  to exist on 2026-09-10. Reticulum and APRS-IS are left unlinked because
  neither has an English Wikipedia article; do not create them.
- **What was left out on purpose.** Download links, "why you would use it"
  arguments, comparisons that favour XPRS over other systems, the roadmap to
  recognition, and the list of supported boards by brand name. Wikipedia
  describes, it does not persuade, and an article that argues for its subject
  is declined as promotional.
