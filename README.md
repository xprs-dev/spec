# XPRS

The XPRS specification: an APRS-successor text packet format for radio and
mesh networks -- 250-byte `key:value` packets carrying messages, observations,
files, commands and services across LoRa, BLE, WiFi, HF/VHF/UHF and the
internet.

The specification is [XPRS.md](XPRS.md); every section is linkable, as
[XPRS.md#3-callsigns](XPRS.md#3-callsigns). [API-HTTP.md](API-HTTP.md)
specifies the HTTP interface stations offer on their LAN.

The conformance corpus is [xprs_corpus.json](xprs_corpus.json): every worked
example in the document as a wire with its byte count and derived identifier
-- an implementation that replays all of them byte-exact and
identifier-exact reads the format.

Reference implementations:
[xprs-flutter](https://github.com/xprs-dev/xprs-flutter) for phones and
desktops, [xprs-firmware](https://github.com/xprs-dev/firmware) for boards,
[reticulum-dart](https://github.com/xprs-dev/reticulum-dart) for the shared
networking library, and [wapps](https://github.com/xprs-dev/wapps) for the
applications that run inside the host. The Dart and C codecs both replay the
corpus in their test suites.

## Editions

The specification is edited continuously and released by year. The current
edition is **XPRS-2026**, and that name refers to the document as it stands
at any point during 2026 -- changes land in the current edition for as long
as its year runs. The first change made in a later year opens a new edition:
an edit in 2027 makes the document XPRS-2027, and XPRS-2026 is frozen as it
last stood.

A new edition is not mandatory every year. A year with no changes produces
no edition, and the expectation is that new editions become rarer as the
specification stabilises. A format for radios in sheds and trackers on
ridges is trusted because it rarely changes.

An implementation states the edition it reads (for example "XPRS-2026").
Within the format's own rules that claim is rarely load-bearing: unknown
keys and words are skipped rather than rejected, so a reader of one edition
degrades gracefully against a writer of another.


## Citing XPRS

The document is edited continuously and has no DOI, no publisher and no
release tags, so a citation names the edition, the draft it stood at when you
read it, and the date you read it. Replace the access date with your own.

```
Brito, M. (2026). XPRS: eXtended Packet Radio System.
    Protocol specification, edition XPRS-2026, Draft 10.
    https://xprs.dev/ [accessed YYYY-MM-DD]
```

```bibtex
@misc{xprs,
  author       = {Max Brito},
  title        = {{XPRS}: {eXtended} {Packet} {Radio} {System}},
  howpublished = {Protocol specification, edition XPRS-2026, Draft 10},
  year         = {2026},
  url          = {https://xprs.dev/},
  note         = {Accessed: YYYY-MM-DD}
}
```

To cite one rule rather than the format, give the section number -- they are
stable within an edition and every section is linkable, as
[XPRS.md#3-callsigns](XPRS.md#3-callsigns). Link the commit you read, so the
sentence you quote is the sentence a reader finds.

## Author and licence

XPRS is written by Max Brito.

The specification is licensed under [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/) (CC BY 4.0):
share it and adapt it for any purpose, including commercially, as long as
you credit Max Brito, link the licence and say what you changed. Full text
in [LICENSE](LICENSE).

Implementations are separate works under their own licences. Writing one
needs no permission, and an implementation is not a derivative of this
document.
