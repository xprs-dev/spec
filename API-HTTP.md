# XPRS station HTTP API

Reference for the HTTP interface an XPRS station may offer on its local
network. Implementations that follow it stay compatible: a tool written
against one station works against every other, whether the station is a
desktop application or a microcontroller.

This is a convenience interface, not the protocol. The wire protocol needs
no HTTP: stations speak 250-byte text packets over their bearers, and a
station reachable over IP answers on port 4242 (XPRS.md section 24.4), where
everything is an ordinary packet. The HTTP API exists for people and tools on
the same network: browsing what a station heard, reading its log, handing it
a packet to transmit. Nothing here adds vocabulary to the protocol.

Reference implementations: the XPRS application (desktop and phone) and the
XPRS station firmware. Where they differ today, the table at the end says which
side has to move.

## General rules

- Port 80, plain HTTP. The audience is the operator's own LAN; a station on
  a hostile network turns the API off, not the encryption on.
- Responses are JSON, `Content-Type: application/json`, with
  `Access-Control-Allow-Origin: *` so browser tools work from anywhere.
- Every response carries `"ok": true` or `"ok": false` plus `"error"` with a
  short reason.
- Timestamps are UTC epoch seconds. A station without a synchronised clock
  reports what it has: `0` in row timestamps, `"+<milliseconds since boot>"`
  in log timestamps, and `"time": "unsynced"` in any response that carries
  timestamps, so a client is never left guessing which scale it is reading.
- Unknown query parameters are ignored. Unknown endpoints are 404. A station
  states what it implements in `/api/services`; a client asks that first
  rather than probing.
- Budgets and limits are the station's own. A small station may cap `limit`
  lower than this document's defaults; the response's `count` tells the
  client what it actually got.

## Endpoints

### GET /api/status

Who and how this station is.

```json
{
  "ok": true,
  "app": "xprs-esp32",
  "board": "m5stack-core",
  "callsign": "X3LTSH",
  "uptime_s": 4211,
  "heap_free": 41200,
  "time": { "synced": true, "epoch": 1755556270, "tz": "+00:00" },
  "radios": { "espnow": true, "lan": true },
  "archiver": { "enabled": true, "count": 132, "epoch": "A" }
}
```

`app`, `callsign`, `uptime_s` and `time` are required; the rest is what the
station has. The application reports its own shape today (see the table); its `app`
and callsign fields are the stable part.

### GET /api/services

What this station serves and what can be asked of it -- the HTTP mirror of
the `t:service serve:` announcement (XPRS.md sections 24 and 36).

```json
{
  "ok": true,
  "serve": ["index", "history", "mailbox"],
  "features": { "digipeater": false, "bridge": true, "igate": true,
                "archiver": true, "share": false },
  "api": ["status", "services", "history", "mail", "send", "log"]
}
```

- `serve` is exactly the list the station would put in its `serve:` field on
  the air. Empty when it serves nothing.
- `features` are the station's own switches, named as its settings name them.
- `api` lists the endpoint names from this document that the station
  implements, so a client feature-detects with one request.
- `station` is the station's own callsign, which the web chat shows beside its
  title. A station that leaves it out is asked `/api/status` (`callsign`).
- `page` says what the web chat page may offer here (the webchat repo's
  README): `tabs`, `session` (a visitor can prove their key, `/api/session`),
  `admin` (this station has an administrator, `/api/admin`), `moderation`
  (its rooms have moderators, XPRS.md section 10.10), `rooms` (it hosts
  closed groups of its own, `/api/rooms`, section 10.10.1), `alerts` (who may
  post a `t:warning` or `t:info` through it: `moderators` or `everyone`,
  section 10.10.2; the page lists the ones it holds as a feed), and `app`.

### GET /api/xprs/history

The station's archive of packets, newest first.

Query parameters, all optional:

- `since`, `until` -- epoch seconds, or the packet timestamp form
  `YYYY-MM-DD_hh:mm:ss` (XPRS.md section 4.3). Both accepted everywhere.
- `only` -- one packet type name (`message`, `observation`, `status`, ...).
- `call` -- only packets FROM this callsign (base form matches suffixed).
- `dir` -- `in` (heard) or `out` (this station transmitted it).
- `room` -- `local`, `regional` or `global`: one chat room (XPRS.md 9.11),
  undirected records heard in range, by the scope their author wrote before
  `m:` (no scope, `scope:global` or a country is `global`). A page asks a room
  at a time so one busy room cannot fill the window; an unknown room matches
  nothing. A hosted room's callsign (below) reads that room.
- `root` -- a thread (XPRS.md 7.4, 18.5): the packet with this identifier
  and every row carrying `root:<id>` or `r:<id>`, oldest first within the
  window. With `room=`, inside that room.
- `limit` -- rows to return; default 30, cap 200.

```json
{
  "ok": true,
  "count": 2,
  "held": 132,
  "time": "synced",
  "rows": [
    { "ts": 1755556210, "bearer": "espnow", "rssi": -49,
      "from": "X1RD89", "to": "", "type": "observation",
      "sig": "unverified", "own": false,
      "wire": "t:observation f:X1RD89 link:ble peers:1 ..." },
    { "ts": 1755556190, "bearer": "lan", "rssi": 0,
      "from": "X16JK8", "to": "X3LTSH", "type": "command",
      "sig": "verified", "own": false,
      "wire": "t:command f:X16JK8 d:X3LTSH cmd:history ..." }
  ]
}
```

Row keys are the application's: `ts` (the sender's claim, 0 when it made none),
`bearer`, `rssi` (0 when the bearer has none), `from`, `to` (empty for a
broadcast), `type`, `sig` (`verified`, `unverified`, `forged`, `none`),
`own` (true when this station originated it), `wire` (the packet verbatim --
the author's bytes, the author's signature). `held` is the archive's total.

Mail in the general history listing follows the station's own policy. The
radio rule (XPRS.md section 36) hands mail only to its two parties; an HTTP
API answering on the operator's own LAN may show everything it holds, and a
station that instead applies the radio rule here must say so in its
documentation. The reference ESP32 implementation shows everything: whoever
can reach the API owns the station.

### GET /api/xprs/mail

Store-and-forward: what the station holds FOR a callsign.

- `call` -- required; the callsign whose waiting mail is listed.
- `limit` -- as above.

Response is the history shape, filtered to records that carry `d:` naming
that callsign. This is the question a returning station asks first, and the
question an operator asks when deciding whether the mailbox is doing its
job.

### GET /api/xprs/devices

Who is in reach: the stations heard recently, which is what a station's own
screen shows and what a visitor on its hotspot most wants to know.

- No parameters. The window is the station's own -- the reference ESP32
  uses 300 seconds, the same one its Reachable panel uses.

```json
{"ok":true,"heard":1843,"count":2,"devices":[
  {"call":"X1QZ3N","bearer":"lora","rssi":-92,"dist_m":84,"hops":0,"age_s":14},
  {"call":"X1MB7K","bearer":"lan","rssi":0,"dist_m":-1,"hops":0,"age_s":62}]}
```

`heard` counts every packet since boot. `rssi` is 0 where the bearer has
none, and `dist_m` is then -1. Where there is a signal, `dist_m` is an
estimate from it and nothing better: a log-distance model knows nothing
about the wall in the way. `hops` is the `via:` length when last heard, so
0 is a neighbour and 1 is somebody a relay carried.

### GET /api/stats

Traffic over time: the three series a station charts for itself.

- `view` -- 0 ten-minute buckets, 1 hourly, 2 daily. Default 0.

```json
{"ok":true,"view":0,"bucket_s":600,"points":24,
 "devices":[2,3,1],"rx":[41,50,12],"tx":[3,9,0]}
```

Oldest bucket first, `points` entries in each array. A station that has no
wall clock has nothing to bucket by and answers `points":0` with empty
arrays -- it is not an error, and the caller should say so rather than draw
a flat line.

### POST /api/xprs/send

Hand the station a finished packet to transmit. The body is the packet
itself: either raw text, or JSON `{"wire": "..."}`.

The station validates syntax and nothing else: the packet parses under
XPRS.md section 4, is at most 250 bytes, and carries `t:` first and an `f:`.
It does not compose, complete, sign or rewrite -- the caller owns the
content, including the callsign it chose to write into `f:`. A station MAY
refuse wires whose `f:` is not its own; the reference implementations
transmit what they are given, because the API answers only on the
operator's network and the operator already owns the radio.

```json
{ "ok": true, "id": "a3f21c", "wire": "t:status f:X1AB3 ts:... hello" }
```

`id` is the section 5 identifier of what was aired. A packet that fails
validation gets HTTP 400 and `{"ok": false, "error": "<reason>"}`; nothing
is transmitted.

### GET /api/admin, POST /api/admin

The station's administrator and the settings it holds for visitors. The
administrator is a visitor who proved their key with a session (`/api/session`,
the webchat repo's README), so the station never holds a password; it keeps the
callsign and the key it was claimed with, and a session for that callsign
signed by another key is not the administrator.

`GET /api/admin?session=<token>`:

```json
{ "ok": true, "admin": "X1ALIC", "you": true, "local": true,
  "claimable": false,
  "settings": { "local_private": true, "who_may_post": "everyone" } }
```

- `admin` is null when the station has none. `you` says whether the session is
  the administrator's; only then are the `settings` included.
- `local` says whether the asker is on the station's own network: a private
  address (RFC 1918, loopback, link-local, IPv6 unique-local), or an address in
  one of the IPv6 prefixes the station itself holds.
- `claimable` is true when there is no administrator and the asker is local.

`POST /api/admin` with JSON `{"action": ..., "session": "<token>"}`:

- `claim`: become the administrator. Only while there is none, and only from
  the station's own network: the moment after a board is flashed or a server
  installed. From the internet it is refused (403), or the first stranger to
  find a public station would own it.
- `set` with `"settings": {...}`: the administrator changes settings. Unknown
  names or values are refused (400) and nothing changes.
- `release`: the administrator gives the station up; it is claimable again.
- `appoint`, `dismiss`, `lift` with `"call": "<callsign>"`: on a station whose
  rooms are moderated (XPRS.md section 10.10), the station signs, as itself,
  `grant:<call> role:mod` (appoint) or `grant:<call>` (dismiss a moderator, or
  lift a removal), files it and airs it. Only the administrator may ask.

Claiming also has the station offer the new administrator `role:mod`, which
their page accepts with their own signature, so the administrator moderates
like anybody appointed.

On such a station the state also carries the asker's place in the record:
`station` (the callsign that is `d:` of every act), `role` (`admin`, `mod`,
`invited` or `none`) and, when invited, `offer` (the identifier of the grant
to accept). A moderator or the administrator also gets `moderators`,
`invited`, and `away` (`[{"call": ..., "until": ...}]`, no `until` meaning
until lifted).

Moderators do not go through `/api/admin`: they sign `t:moderate` acts about
the station's rooms in the browser and post them to `/api/xprs/send` like any
wire. The station takes one only when `d:` is its own callsign, the signature
verifies against a key it holds, and the signer is a moderator now (or is
accepting an offer made to them, `r:<grant> accept:mod`); a grant from anybody
but the station is refused. It then enforces the record on what it serves: a
removed message (`r:<id> remove:message`) and the publications of somebody sent
away (`revoke:<call>`, with or without `until:`) are left out of
`/api/xprs/history`, except `sos`, `warning` and `info`; a post from somebody
sent away is refused (403); and the history answer carries
`"moderation": {"removed": [ids], "away": [callsigns]}` so a page already
showing them takes them down.

Each answers with the state, as GET does. The settings:

| Setting | Values | Default | What it does |
|---|---|---|---|
| `local_private` | true, false | true | visitors who are not local do not get `scope:local` rows from `/api/xprs/history`; asked for `room=local` they get no rows and `"private": true` |
| `who_may_post` | `everyone`, `local`, `nobody` | `everyone` | who `/api/xprs/send` accepts a wire from |
| `who_may_alert` | `moderators`, `everyone` | `moderators` | who may post a `t:warning` or `t:info` through `/api/xprs/send` (XPRS.md 10.10.2); the administrator and the moderators always may, and an author always withdraws their own |

### GET /api/rooms, POST /api/rooms

The closed groups this station hosts (XPRS.md section 10.10.1): ordinary `X5`
groups whose key the station holds and whose traffic it files and serves but
never airs. `GET /api/rooms?session=<token>` lists the rooms the asker may see:
every public room, and the private rooms the asker is in (or all of them, to
the administrator).

```json
{ "ok": true, "rooms": [ { "call": "X5A3F2", "name": "Block C", "about": "residents",
  "kind": "chat", "visibility": "public", "posting": "members",
  "shared": false, "role": "member", "can_post": true } ] }
```

`kind` is `chat` (the default: a conversation) or `forum` (topics and
comments, XPRS.md 18.5, with the conversation beside them). `shared` says
whether other stations may hold a copy (below); a room this station mirrors
from another carries `owner` (that station's callsign) instead, and
`mirrored: true`.

`role` is the asker's place in the room (`admin`, `mod`, `member`, `invited`
with the `offer` to accept, or `none`); `can_post` says whether a message from
the asker would be taken. A moderator or the administrator also gets `members`,
`moderators` and `invited`.

`POST /api/rooms` is the administrator's (JSON, `session` required):

- `create` with `name`, optional `about`, `kind` (`chat` or `forum`, default
  chat), `visibility` (`public` or `private`, default public) and `posting`
  (`members` or `anyone`; a private room is always `members`). The station
  makes the group's key and offers the administrator `role:mod`, which their
  page accepts. The answer names the new room in `room`.
- `update` with `call` and any of `name`, `about`, `kind`, `visibility`,
  `posting`.
- `share` with `call`, `shared` (true or false) and `peers` (callsigns of the
  stations that may hold a copy; required for a private room, optional for a
  public one, where an empty list means any station). The station then
  answers `cmd:history only:<call>` to those stations and asks them the same
  (XPRS.md 10.10.1). Sharing a private room is served-to-members at two
  operators, and the page says so before it asks.
- `mirror` with `call` (the room's `X5`), `owner` (the station that holds
  its key) and optionally `name`, `about`, `kind`, `visibility`, `posting`
  (the copy's own serving options): this station fetches the group's
  identity from the owner, then its record and its posts, and serves the room
  as the owner's record says, with no authority of its own in it. `unmirror`
  with `call` stops that and forgets the copy's options; what was filed stays
  filed. `sync` with `call` asks the room's peers now rather than at the next
  period. A shared room lists `peers` and `seen` (stations that asked for it
  and were answered); a mirrored one carries `mirrored: true` and `owner`.
- `close` with `call`: the station stops serving the room and forgets its
  options; the key and the signed record stay.
- `add`, `appoint`, `remove` with `call` and `member`: the station signs, as
  the room, `grant:<member>`, `grant:<member> role:mod` or `revoke:<member>`.
  A grant is an offer the person accepts by posting
  `t:moderate f:<them> d:<room> r:<offer> accept:member` (or `accept:mod`)
  through `/api/xprs/send` (XPRS.md 10.3.1).

Reading a room is `GET /api/xprs/history?room=<call>&session=<token>` (a
private room answers 404 to anybody not in it); posting is a signed
`t:message` (or `t:reaction`) with `d:<call>` through `/api/xprs/send`, taken
from a member (or anybody, where `posting` is `anyone`) whose key the station
has heard, filed and not aired. A room's moderators act as in section 10.10:
`r:<id> remove:message`, `revoke:<call> [until:]`, signed by them.

**A forum room** takes `t:blog` as well, under the same posting rule: with
`title:` it opens a topic (or replaces the author's earlier one of that
title, XPRS.md 18.1); without a title and with `r:` (and `root:` below the
first level) it is a comment on a topic (18.5); a long one arrives in parts,
signed on the last (9.1.1): each part but the last is answered `202` with
`held`, and the last `200` with the whole's `id`, which is what the station
files and serves. `t:message` to the room stays its conversation.
`GET /api/rooms?topics=<call>&session=<token>` is the room's index, the
newest 100 topics by last activity:

```json
{ "ok": true, "room": "X5F0RM", "topics": [
  { "id": "5f2c1a", "title": "balun-question", "from": "X1RD89",
    "ts": 1754668930, "replies": 2, "last": 1754671200, "edited": false } ] }
```

A topic's thread is `GET /api/xprs/history?room=<call>&root=<id>` (the
opening post in every edition, then the comments), and `kind=blog` on the
room lists the posts alone. Removal and sending away are the room's as above;
a moderator's `r:<id> remove:message` names an identifier, so it takes a
topic or a comment down as it takes a message.

### GET /api/log

The station's own log, machine readable, newest first.

- `limit` -- lines to return; default 50, cap 500.

```json
{
  "ok": true,
  "time": "synced",
  "lines": [
    { "t": 1755556270, "m": "W m5xprs: alive 61s heap=42628 ..." },
    { "t": "+61708",   "m": "I m5xprs: lan 192.168.178.102 146B t:..." }
  ]
}
```

`t` is epoch seconds when the line was written under a synchronised clock,
or `"+<milliseconds since boot>"` when it was not -- the two forms are
distinguishable by type and by the leading `+`. `m` is the line, plain text,
no colour escapes.

## Per-station extras

A station may add endpoints beyond this document. They stay out of the
shared names above and are listed in `/api/services` under `api` only when
they follow this document. Current extras:

- T-Dongle: `GET /api/xprs/dir` (the XDIR1 directory of XPRS.md 36.9),
  `GET /api/xprs/key`.
- ESP32 config share: `GET /` (editor page), `GET/POST /config.ini`,
  `GET /log.txt` (the raw rotating log, newest first).
- The XPRS application: `POST /api/xprs/ask` (compose and air a signed `cmd:history` at
  another station), `POST /api/xprs/mailbox` (declare favourite archivers),
  and its application-specific surface.
- A camera or doorbell (the `url:` target of XPRS.md section 11.7.2):
  `GET /door/snapshot.jpg` returns a current still as `image/jpeg`, and
  `GET /door/stream.mjpeg` returns the live view as `multipart/x-mixed-replace`
  motion-JPEG a browser can open. These are the resources a `q:snapshot` or
  `q:stream` answer names in its `url:`. A station that serves them lists
  `snapshot` and `stream` under `api` in `/api/services`. They return image
  bytes, not JSON, so the general JSON rule above does not apply to them; an
  error still answers with the JSON `{"ok":false,"error":...}` shape. The camera
  never puts its RTSP credentials in any URL it hands out.

## Compatibility today

| Endpoint | The application | xprs-firmware | Note |
|---|---|---|---|
| GET /api/status | yes (own shape) | yes | shared keys: app, callsign |
| GET /api/services | no | yes | the application should adopt |
| GET /api/xprs/history | yes | yes | ESP32 adds `call`, `dir` params; the application should adopt |
| GET /api/xprs/mail | no | yes | the application should adopt |
| POST /api/xprs/send | composes a packet | validates only | the application should also accept a raw `wire` |
| GET /api/log | yes (plain strings) | yes (typed `t`/`m`) | converge on typed lines |
| GET /api/session, POST /api/session | yes (core `WebChatApi`) | yes (`common/xprs_webchat`) | a signed nonce; the page proves its key to read its mail and to administer or moderate |
| GET/POST /api/admin | yes (share server and server edition, core `WebChatApi`) | yes (`common/xprs_webchat`, `xapi_wc.c`) | the page offers it where `page.admin` says so |
| GET/POST /api/rooms | yes (server edition; the share server once it hands the core its keys) | yes (`common/xprs_webchat`) | the page offers it where `page.rooms` says so; `kind`, `share`, `mirror` and `topics` are specified and not implemented by either engine |

**One page, several engines.** The web chat page is the same file on every
platform; a phone, a server or a board is an engine behind this API. Two
implementations exist because the platforms do, the Dart core's `WebChatApi`
and the ESP32's `xwc` (plain C), and what keeps them one API is the
conformance suite in the webchat repo, `contract/conformance.py`: it drives
every endpoint above from outside with keys of its own, signing with the
page's crypto, and is run against each engine. A rule added to one engine is
added to the suite first, and the other engine fails until it has it.
