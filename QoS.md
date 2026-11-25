# XPRS quality of service on constrained bearers

How a station decides what to transmit when a bearer cannot carry everything
it hears: which packets are admitted, in what order they leave, how an hour's
airtime is shared, and what is dropped. These are the guiding rules for the
implementations of the scheduling algorithm and for the test harness that
measures them.

## 1. Introduction

A LoRa channel is not a network cable. On LongFast in Europe a 200-byte
packet occupies the air for well over a second, the law allows a station a
fraction of each hour, and the channel is shared with every other station and
every other network in range. A Bluetooth or LAN neighbourhood next to it
produces traffic at a rate no radio can repeat: on the reference bench
(2026-11-25) a single relay heard several packets a second on Bluetooth and,
filtered only by packet type, spent its whole hourly LoRa budget re-airing
other stations' history requests while a person's message waited behind them.

A digipeater therefore cannot repeat every packet. XPRS.md already says what
a station **may** relay, how far, and in what order it airs what it has
queued. It deliberately leaves to each station what it **admits** onto a
scarce bearer and how it **spends** its budget (XPRS.md 9.5: "a carrier is
free to ... carry only `low` traffic for its own reasons"). Left to each
implementation, that freedom produces stations that behave differently under
load, and a network whose behaviour under load nobody can predict. This
document fixes the behaviour so that every implementation (the station
firmware, the application, the server) sheds load the same way.

What this document is:

- **Rules for one shared component.** The algorithm is written once per code
  base and used by every bearer with a limit: LoRa in any mode, APRS on
  VHF/UHF, slow Reticulum links, and any future medium with a budget. Bearers
  without one (Bluetooth, LAN, ESP-NOW) pass through it and are only subject
  to the scope, duplicate and repeat rules.
- **Built from existing words.** Every decision is made from keys packets
  already carry: `t:`, `f:`, `d:`, `urg:`, `scope:`, `ts:`, `until:`,
  `dest:`, `near:`, `via:`, `k:`, and the station policy keys `owner:` and
  `first:` (XPRS.md 11.10). Nothing here adds vocabulary to the protocol.
- **Testable.** Every rule has a measurable consequence, and section 8 says
  how the harness checks it.

What it is not: it does not change XPRS.md. Where the two appear to disagree,
XPRS.md wins and this document is wrong.

Numbers in this document are **reference values**, in the sense of XPRS.md
30.2: what the reference implementations ship, chosen from bench
measurement, and adjustable per bearer profile (section 6). The rules are not
adjustable; the numbers are.

## 2. Terms

| Term | Meaning |
|---|---|
| **bearer** | one medium a station transmits on (LoRa, BLE, LAN, ESP-NOW, Reticulum, APRS) |
| **constrained bearer** | a bearer with an airtime or byte budget |
| **budget** | the transmit time a station allows itself on a bearer per rolling hour |
| **rolling hour** | the last sixty minutes, measured continuously, not the clock hour |
| **owner traffic** | packets this station signs itself, and packets from one of its owners (`owner:` / `own1`..`own4`) handed to it directly |
| **third-party traffic** | everything else this station relays or bridges |
| **periodic packet** | a packet whose content is mostly "I am still here": `observation`, `service`, `identity`, `track`, a bridged node's announcement. Not `status`: XPRS.md counts it as presence for archiving, but it carries a person's words and each one is new |
| **admit** | accept a packet into a bearer's queue |
| **shed** | decide not to transmit a packet on this bearer; it is not an error and nothing is owed to its sender |

"Handed to it directly" means heard with no `via:` on a short-range bearer
(Bluetooth, USB, the station's own access point). A packet relayed from afar
that merely carries an owner's callsign in `f:` is third-party traffic: the
same rule XPRS.md applies to an owner's commands.

## 3. What XPRS.md already fixes

The component obeys these unchanged. They are listed so an implementer reads
them in one place, not to restate them.

| Rule | Section | Consequence here |
|---|---|---|
| Hop budget by type | [9.1](XPRS.md#91-how-far-a-packet-travels) | `sos`/`warning` 9 relays, everything else 3 |
| Loops and duplicates | [9.2](XPRS.md#92-loops) | never relay a packet naming us in `via:`, never twice |
| Random wait, cancel on a copy | [9.2.1](XPRS.md#921-when-to-re-air) | a queued relay is withdrawn when another station airs it first |
| Carried packets | [9.4](XPRS.md#94-carrying-toward-a-place) | `dest:`/`near:` decide who carries; `until:` ends it |
| Urgency | [9.5](XPRS.md#95-urgency) | `urg:` is a request; a stranger's counts no higher than `high` |
| Retries | [9.7.2](XPRS.md#972-when-to-stop-trying) | only against evidence the peer is reachable |
| Scope | [9.11](XPRS.md#911-how-far-a-packet-may-go) | `scope:local` never goes on a radio; LoRa is regional |
| Who goes first | [11.10](XPRS.md#1110-setting-up-a-station) | `sos`/`warning`, then `first:`, then `urg:`, then oldest `ts:` |
| Cadence | [30.1](XPRS.md#301-cadence-belongs-to-the-bearer) | the strictest bearer binds; a beacon is not free; a retry costs as much as the first send |
| Serving strangers | [30.2](XPRS.md#302-what-a-station-owes-a-stranger) | answers metered per caller; refuse with `code:429` |

## 4. The rules

### 4.1 The budget is a rolling hour

**Every constrained bearer has one budget, measured over a rolling hour, and
every transmission on that bearer is charged to it:** relays, bridged
translations, our own packets, answers, retries, and frames a bridge sends on
behalf of another network sharing the radio (a Meshtastic NodeInfo, a native
relay). A station that keeps one ledger per subsystem can exceed the law with
every ledger in order.

The budget is the legal limit for the sub-band or a lower figure the operator
sets, never higher. Reference: 10% (360 s per hour) on EU 869.4-869.65 MHz,
where Meshtastic's LongFast sits; 1% (36 s) on sub-bands limited to 1%.

### 4.2 The owner's reserve

**A tenth of the budget is reserved, at every moment, for the owner and for
calls for help.** Third-party traffic stops at 90% of the rolling hour.

| Traffic | May spend up to | Leaves the queue |
|---|---|---|
| `t:sos`, `t:warning`, from anyone | 100% | first, always |
| owner traffic | 100% (the reserve plus whatever the shared part has left) | second |
| third-party traffic | 90% | after both, in the order of 4.3 |

- The reserve exists for the unexpected message. Because the hour rolls, it
  is always available, not only at the start of a clock hour, and a station
  whose relays filled the channel can still say something itself.
- A call for help may consume the reserve. The owner's traffic outranks a
  stranger's, never a stranger's call for help (XPRS.md 11.10: the owner is
  "not entitled to bury a call for help under their own mail").
- The final slice of the budget (reference: 2%) is spendable by `sos` and
  `warning` only, so that a station that has spent everything on its owner
  can still relay an emergency.
- The reserve is not lent to third parties when idle. An idle reserve is the
  point of a reserve.

Reference: reserve 10%, emergency-only slice 2%.

### 4.3 Who goes first

The airing order of XPRS.md 11.10 is applied with the owner ahead of
strangers, as 4.2 requires:

1. `t:sos` and `t:warning`;
2. owner traffic;
3. packets whose `f:` is in `first:`;
4. by `urg:`, `urgent` > `high` > `normal` > `low`, a stranger's counted no
   higher than `high`;
5. by `ts:`, oldest first.

The order decides only **which admitted packet goes next**. Whether a packet
is admitted at all is decided before it (4.4 to 4.6), and nothing in the order
can lift a packet past the 90% line of 4.2.

### 4.4 Admission: worth this bearer

**A packet enters a constrained bearer's queue only if somebody on that
bearer is waiting for it.** Each packet is placed in one class; a bearer
profile names which classes it admits.

| Class | Packets | Admitted on a constrained bearer |
|---|---|---|
| **L0 life** | `sos`, `warning` | always |
| **L1 owner** | owner traffic (2) | always |
| **L2 conversation** | `message`, `status`, `receipt`, `reaction`, a direct message | always, subject to scope |
| **L3 transaction** | `command`, `result`, `request` | only when the destination `d:` was heard on this bearer and not on a cheaper one |
| **L4 keys** | `identity` | under the repeat rule of 4.5 |
| **L5 presence** | `observation`, `service`, `track` | under the repeat rule of 4.5 |
| **L6 bulk** | history replays, `file` chunks, `mailbox` catch-up, anything whose `ts:` is older than the profile's freshness limit | only when the budget is mostly unspent (4.7) |

Further, whatever the class:

- **Not for somebody already reached.** A packet addressed (`d:`) to a station
  heard directly on a cheaper bearer is not admitted: it reached them the way
  it reached us.
- **Not out of scope.** `scope:local`, or a scope word the station does not
  know, is never admitted to a radio (XPRS.md 9.11).
- **Not old news.** A `ts:` older than the class's freshness limit (section 6)
  is a carousel or a replay; with no clock, "now" is the newest `ts:` heard
  lately.
- **Not twice.** A packet aired on this bearer in the last 30 minutes is not
  admitted again, beyond the 9.2 duplicate ring, which forgets after minutes.

### 4.5 Repeats that are not worth repeating

**A periodic packet is aired on a bearer no more often than that bearer's
repeat interval, per author and per type. A repeat that arrives sooner is
dropped, not queued.**

| Bearer | Repeat interval |
|---|---|
| Bluetooth, LAN, ESP-NOW | 5 min |
| LoRa, ordinary | 30 min |
| LoRa, crowded | 60 min |

- It applies to the station's own beacons and to the ones it would relay or
  bridge, including a bridge's announcements of its stand-in nodes on
  another network.
- **Crowded** is measured, not configured: 8 or more stations heard directly
  on the bearer in the last 10 minutes, or a channel utilisation above 25%
  (on a channel shared with Meshtastic, that network's own figure counts).
  The state clears when both are below the thresholds again.
- **A real change is not a repeat.** An `identity` carrying a different `k:`
  goes out at once (XPRS.md 29.1); so does a packet whose content changed in
  a way somebody acts on. A changed uptime or counter is not such a change.
- Messages, receipts, commands, results and requests are never "repeats" in
  this sense: each is a new packet, and duplicates of one are the 9.2 ring's
  business.
- A scheduler's own drift is not a repeat: a beacon on a 300 s timer that
  fires a fraction of a second early is on time. Reference: 5% of the
  interval.
- The rule holds for copies still waiting too: a queue keeps one copy of a
  packet and one periodic packet per author and type. Two copies of the same
  identity heard over two relays before the first is aired are one
  transmission, not two.

Reference: the table above; thresholds 8 stations, 25% utilisation.

### 4.6 Fair share among third parties

**No single third party may take more than its share of the third-party part
of the budget.** Within the 90%:

- each author's share per rolling hour is the third-party budget divided by
  the number of authors heard on the bearer in that hour, but never by fewer
  than four;
- a share an author does not use is available to the others (the allocation
  is work-conserving: max-min fair, not a fixed slice);
- a packet whose author is over its share waits, and is shed if it expires
  waiting.

L0 and L1 are not subject to fair share. Reference: minimum divisor 4.

### 4.7 Spending smoothly

**The budget is spent across the hour, not at its start.** A station that
spends its hour in ten minutes is silent for fifty, and the next message
arrives into that silence.

- No more than one tenth of the budget is spent in any six minutes, except by
  L0 and L1.
- Keys, presence and bulk (L4-L6) may use only the first half of that pace;
  the second half is always there for conversation and transactions. The
  airing order of 4.3 sends the oldest `ts:` first, and a replayed history
  page or a re-said identity is old by construction: without this, the
  replay harness measured fresh messages waiting five minutes behind them.
  Eligibility, not order, is what changes, as with fair share.
- **Spare capacity is used, not wasted.** L6 bulk is admitted only while more
  than 60% of the budget is unspent and the channel is not crowded; it is the
  first traffic shed as the hour fills.

Reference: one tenth per six minutes, half of it for L4-L6; bulk above 60%
unspent.

### 4.8 Expiry and eviction

- A queued packet expires at its `until:`, or at its class's queue limit,
  whichever is sooner: L0 10 min, L1 30 min, L2 30 min, L3 2 min, L4/L5 the
  repeat interval, L6 1 min.
- When the queue is full, the packet evicted is the lowest class, then the
  lowest `urg:`, then the one furthest from being due. **L0 is never evicted
  by anything else**, and L1 never by third-party traffic.
- A retry is admitted as a new packet of the same class and charged like the
  first transmission (XPRS.md 30.1), and only while there is evidence the
  peer is reachable (9.7.2).

### 4.9 A relay must extend reach

A digipeater's transmission is worth its airtime only when it reaches
somebody the original did not. Among admitted relays:

- the station that heard a packet faintly re-airs first, the one standing
  next to the sender last or never (XPRS.md 9.2.1);
- a queued relay is withdrawn as soon as another station's copy is heard;
- a carried packet (`dest:`) is relayed only by a station that reduces the
  distance to `dest:` (XPRS.md 9.4).

### 4.10 Other networks on the same radio

A station bridging to another network on the same channel (Meshtastic,
MeshCore) charges that network's frames to the same budget, by the same
classes: a translated text is L2, a native relay is third-party L2, a node
announcement is L5 under the repeat rule. The other network's own politeness
rules (for Meshtastic, its channel-utilisation limits) are honoured in
addition, never instead.

## 5. Refusing and saying why

Shedding is silent on the air: a relay owes nothing to a packet it does not
carry, and announcing every drop would cost the airtime it saved. Shedding is
**not** silent to the station's owner:

- every constrained bearer counts, per class: admitted, aired, shed (with the
  reason: scope, repeat, fair share, budget, expired, evicted, reached
  elsewhere) and the current reserve;
- these counters are shown wherever the station reports its state (its
  status endpoint, console, and the station panel of the web chat);
- an answer that is refused for budget is refused out loud, as XPRS.md 30.2
  requires (`code:429`), because there the asker is waiting.

## 6. Bearer profiles

Each constrained bearer is described by one profile. The rules are the same
for all; only these values differ.

| Profile | Budget/h | Reserve | Repeat ordinary / crowded | Freshness (L3 / L6) | Notes |
|---|---|---|---|---|---|
| LoRa `meshtastic` (EU LongFast) | 360 s | 10% | 30 / 60 min | 30 min / 30 min | shared with Meshtastic: watch its utilisation |
| LoRa `xprs` (SF7) | 360 s | 10% | 30 / 60 min | 30 min / 30 min | |
| LoRa `meshcore` | 360 s | 10% | 30 / 60 min | 30 min / 30 min | shared with MeshCore |
| LoRa, 1% sub-band | 36 s | 10% | 60 / 120 min | 30 min / off | bulk is never worth it here |
| APRS VHF/UHF 1200 bd | per local band plan | 10% | 30 / 60 min | 30 min / off | |
| Reticulum, slow link | per link | 10% | 30 / 60 min | as link allows | |
| Bluetooth, LAN, ESP-NOW | none | none | 5 min | none | scope, duplicate and repeat rules only |

## 7. Placement in an implementation

- **One component per code base**, platform-free, used by every bearer; not a
  filter per board or per bearer. In the station firmware it sits inside the
  shared bearer (`xprs_bearer`) so every bearer and every board gets it at
  once, and the per-board filters that preceded it are removed.
- **Pure decisions, injected facts.** The component decides from the packet,
  the bearer profile and a context the caller supplies (which bearer the
  packet came from, its signal, whether it came direct, where its
  destination was heard, the ledger, the channel's utilisation, the current
  time). It owns no radio and no clock, so the same code runs on a
  microcontroller, in the application and in the harness.
- **Bounded memory.** Tables (repeat intervals per author, fair-share
  accounts, the aired ring) have fixed sizes chosen per platform, and evict
  their least recently used rows.
- **An exact ledger.** The hour and the six-minute pace are measured over the
  transmissions themselves, not over minute buckets: a window that starts at
  a minute boundary misses up to a minute of earlier sends, which the
  harness showed as 61 s spent in six minutes against a limit of 36.

Implementations:

| Code base | Component | Harness |
|---|---|---|
| XPRS core (Dart: the app and the Linux server) | `lib/src/services/xprs/xprs_qos.dart` | `test/xprs_qos_test.dart`, `test/xprs_qos_replay_test.dart`, traces made by `tool/qos_trace.py` |
| Station firmware (C) | not yet: today `lr_worth` and `nrf_hears` apply part of 4.4 and 4.5 | |

## 8. The test harness

Every rule above is checked by a harness that runs the component on a host,
against both synthetic cases and recorded traffic.

**Recorded traffic.** Bench captures (packets with arrival time, bearer and
signal, as the station consoles log them) are replayed into the component
with a simulated constrained bearer: the profile's airtime per byte, its
budget, and a channel shared with a configurable amount of foreign traffic.
The reference capture is the 2026-11-25 bench (about 6,000 packets heard by
a T-Deck among sixteen stations).

**What it measures**, per profile and per run:

- airtime spent per rolling hour, and its largest six-minute burst;
- per class: offered, admitted, aired, shed by reason, and the delay from
  arrival to transmission (median and 95th percentile);
- per third-party author: share of airtime against its fair share;
- the reserve's low-water mark across the run.

**What must hold** (the pass criteria):

1. The budget is never exceeded over any rolling hour.
2. Third-party traffic never spends past 90% of any rolling hour.
3. With the third-party part saturated, an owner message injected at any
   moment is aired within the profile's ordinary delay (reference: 30 s on
   LoRa), and an `sos` within the jitter of 9.2.1.
4. No `sos` or `warning` is shed for any reason but its hop budget or its
   expiry.
5. Every L2 packet that is in scope and not reached elsewhere is aired, unless
   the run is deliberately overloaded with L2 alone, in which case the order
   of 4.3 decides and fair share holds.
6. No periodic packet is aired on a bearer more often than its repeat
   interval for its author and type, crowded or not, except on a real change.
7. No author exceeds its fair share while another author with waiting
   traffic is under its own.
8. No six-minute window spends more than one tenth of the budget on L2-L6.
9. The airing order of every transmitted pair agrees with 4.3.

**Synthetic cases** cover what recordings rarely contain: a burst of `sos`
on a spent budget, an owner writing into a saturated channel, a single
chatty author, a crowded channel flipping state, an identity whose key
changes, a clockless station, and queue overflow with every class waiting.

A change to the algorithm or to a reference value is accepted when the
harness passes on the reference capture and the synthetic cases, and the
report of the run is kept with the change.
