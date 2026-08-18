# XPRS

The XPRS specification: an APRS-successor text packet format for radio and
mesh networks -- 250-byte `key:value` packets carrying messages, observations,
files, commands and services across LoRa, BLE, WiFi, HF/VHF/UHF and the
internet.

The specification is [XPRS.md](XPRS.md). The conformance corpus is
[xprs_corpus.json](xprs_corpus.json): every worked example in the document as
a wire with its byte count and derived identifier -- an implementation that
replays all of them byte-exact and identifier-exact reads the format.

Reference implementations live in the
[geograms](https://github.com/geograms) project (Dart host and ESP32 C
codec); both replay the corpus in their test suites.

## Editions

The specification is edited continuously and released by year. The current
edition is **XPRS-2026**, and that name refers to the document as it stands
at any point during 2026 -- changes land in the current edition for as long
as its year runs. The first change made in a later year opens a new edition:
an edit in 2027 makes the document XPRS-2027, and XPRS-2026 is frozen as it
last stood.

A new edition is not mandatory every year. A year with no changes produces
no edition, and the expectation is that new editions become rarer as the
specification stabilises -- a format for radios in sheds and trackers on
ridges earns trust by changing less, not more.

An implementation states the edition it reads (for example "XPRS-2026").
Within the format's own rules that claim is rarely load-bearing: unknown
keys and words are skipped rather than rejected, so a reader of one edition
degrades gracefully against a writer of another.
