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

Reference implementations: the Aurora application (desktop and phone) and the
xprs-firmware boards. Where they differ today, the table at the end says which
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
  "indexer": { "enabled": true, "count": 132, "epoch": "A" }
}
```

`app`, `callsign`, `uptime_s` and `time` are required; the rest is what the
station has. Aurora reports its own shape today (see the table); its `app`
and callsign fields are the stable part.

### GET /api/services

What this station serves and what can be asked of it -- the HTTP mirror of
the `t:service serve:` announcement (XPRS.md sections 24 and 36).

```json
{
  "ok": true,
  "serve": ["index", "history", "mailbox"],
  "features": { "digipeater": false, "bridge": true, "igate": true,
                "indexer": true, "share": false },
  "api": ["status", "services", "history", "mail", "send", "log"]
}
```

- `serve` is exactly the list the station would put in its `serve:` field on
  the air. Empty when it serves nothing.
- `features` are the station's own switches, named as its settings name them.
- `api` lists the endpoint names from this document that the station
  implements, so a client feature-detects with one request.

### GET /api/xprs/history

The station's archive of packets, newest first.

Query parameters, all optional:

- `since`, `until` -- epoch seconds, or the packet timestamp form
  `YYYY-MM-DD_hh:mm:ss` (XPRS.md section 4.3). Both accepted everywhere.
- `only` -- one packet type name (`message`, `observation`, `status`, ...).
- `call` -- only packets FROM this callsign (base form matches suffixed).
- `dir` -- `in` (heard) or `out` (this station transmitted it).
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

Row keys are Aurora's: `ts` (the sender's claim, 0 when it made none),
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
- Aurora: `POST /api/xprs/ask` (compose and air a signed `cmd:history` at
  another station), `POST /api/xprs/mailbox` (declare favourite indexers),
  and its application-specific surface.

## Compatibility today

| Endpoint | Aurora | xprs-firmware | Note |
|---|---|---|---|
| GET /api/status | yes (own shape) | yes | shared keys: app, callsign |
| GET /api/services | no | yes | Aurora should adopt |
| GET /api/xprs/history | yes | yes | ESP32 adds `call`, `dir` params; Aurora should adopt |
| GET /api/xprs/mail | no | yes | Aurora should adopt |
| POST /api/xprs/send | composes a packet | validates only | Aurora should also accept a raw `wire` |
| GET /api/log | yes (plain strings) | yes (typed `t`/`m`) | converge on typed lines |
