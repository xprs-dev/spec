# XPRS

The XPRS specification: an APRS-successor text packet format for radio and
mesh networks — 250-byte `key:value` packets carrying messages, observations,
files, commands and services across LoRa, BLE, WiFi, HF/VHF/UHF and the
internet.

The specification is [XPRS.md](XPRS.md). The conformance corpus is
[xprs_corpus.json](xprs_corpus.json): every worked example in the document as
a wire with its byte count and derived identifier — an implementation that
replays all of them byte-exact and identifier-exact reads the format.

Reference implementations live in the
[geograms](https://github.com/geograms) project (Dart host and ESP32 C
codec); both replay the corpus in their test suites.
