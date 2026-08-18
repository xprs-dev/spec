# Getting XPRS recognized

Working notes on standardization paths. The concrete first move is the
IETF, below. TAPR/IARU outreach (amateur-radio community legitimacy) and
later options (ETSI ISG, OASIS, ISO fast-track) are follow-ups once the
draft exists and has been discussed in public.

## IETF

### Why the IETF

Wire protocols and text formats are its core business, participation is
free and individual (no membership, no fees), and the output is an RFC
number: the most citable form of internet-protocol recognition. APRS
never got one.

### The working group with the strongest chances: DTN

Delay/Disruption Tolerant Networking (dtn), active, charter at
https://datatracker.ietf.org/wg/dtn/about/ and mailing list dtn@ietf.org.

Why it is the best room for XPRS:

- Their protocol suite (Bundle Protocol, RFC 9171) is built on the same
  concepts XPRS ships: store-and-forward, custody transfer, signed
  delivery acknowledgment, nodes unreachable at send time, intermittent
  links. The XPRS custody sections read natively to this audience.
- XPRS occupies an operating point they do not cover: human-readable
  250-byte text packets on LoRa/BLE-class bearers, pocket devices as
  infrastructure. It complements rather than competes with the Bundle
  Protocol, which is the healthy position for a newcomer draft.
- Second-best room: tvr (Time-Variant Routing), for the scheduled-window
  and reachability-freshness material. Worth joining the list; not the
  primary target.

Realistic expectation, stated honestly: WG adoption of an outside
full-stack format is unlikely and NOT required. The goal in dtn is
review, credibility and citations; the RFC itself comes through the
Independent Submission stream, which needs no working group.

### The steps, in order

1. **Datatracker account.** https://datatracker.ietf.org/accounts/create/
   with the author email. This is the identity everything else hangs on.

2. **Tooling.** The draft source here (`draft-brito-xprs-00.md`) is in
   kramdown-rfc format, the markdown flavor from https://authors.ietf.org.
   Install and convert:

       gem install kramdown-rfc     (needs ruby)
       pip3 install xml2rfc
       kdrfc draft-brito-xprs-00.md     -> produces .xml and .txt

   Fix any nits it reports; the submission checker enforces them. The
   idnits tool (https://author-tools.ietf.org) runs the same checks
   online without installing anything.

3. **Submit the -00.** https://datatracker.ietf.org/submit/ with the
   generated XML. Individual submissions need no approval: the draft is
   published within minutes and announced on i-d-announce. Naming is
   already correct (draft-brito-xprs-00: individual draft, author
   surname, topic, revision). A draft expires after 185 days; each
   revision (-01, -02...) resets the clock, so expiry is a rhythm, not a
   deadline.

4. **Introduce it on the dtn list.** Subscribe at
   https://www.ietf.org/mailman/listinfo/dtn, then one short mail: what
   XPRS is (two sentences), the operating point relative to BP (one
   sentence), link to the draft and to xprs.dev, and a concrete ask --
   review of the custody and identifier sections. Concrete asks get
   answers; "please look at my protocol" does not. Cross-post nothing;
   a separate, adapted mail to tvr@ietf.org later if the first lands.

5. **Iterate in public.** Fold list feedback into -01 with an explicit
   acknowledgments note. Two or three revisions with visible responses
   to review is what builds standing. The running code and the
   247-wire conformance corpus are the strongest cards: IETF culture is
   "rough consensus and running code", and most drafts show up with
   neither.

6. **Optional but valuable: present it.** IETF meetings run three times
   a year, remote participation supported. Ask the dtn chairs for ten
   minutes on the agenda, or failing that book a side meeting. One
   presentation puts faces to the draft and typically doubles list
   engagement.

7. **The RFC: Independent Submission stream.** When the draft is stable
   (typically after -02/-03), submit it to the Independent Submissions
   Editor per https://www.rfc-editor.org/about/independent/ requesting
   Experimental (fits a format with running code and an evolving
   edition model; Informational also acceptable). The ISE arranges its
   own expert review; expect months and one or two revision cycles. The
   result is an RFC number in the Independent stream -- exactly the
   recognition target.

### What NOT to do

- Do not request WG adoption in the first mail; let the room ask.
- Do not submit the full 6800-line specification as the draft; the -00
  here is deliberately the core plus pointers, which is what gets read.
- Do not let the draft expire silently while discussion is live; a
  refresh costs one command.

## After the IETF (parallel and later)

- **TAPR** (tapr.org): paper and talk at the DCC conference; the
  community that stewards AX.25 and APRS. Parallel to the IETF work.
- **IARU member societies** (ARRL, RSGB, REP): articles and liaison for
  the amateur-band operating rules of sections 9.4 and 33.
- **ETSI ISG or OASIS Open Project**: if industry adoption appears;
  membership-based; carries the format toward regulators.
- **ISO/IEC JTC 1 fast-track**: the endgame, realistic only via a
  consortium or national body (IPQ) once the ecosystem is established.
