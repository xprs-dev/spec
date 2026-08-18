# XPRS

The XPRS specification: an APRS-successor text packet format for radio and
mesh networks — 250-byte `key:value` packets carrying messages, observations,
files, commands and services across LoRa, BLE, WiFi, HF/VHF/UHF and the
internet.

The specification is [XPRS.md](XPRS.md). Reference implementations live in
the [geograms](https://github.com/geograms) project (Dart host and ESP32 C
codec), where every worked example in the document is a test fixture replayed
byte-exact through both.
