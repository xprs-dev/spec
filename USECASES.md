# XPRS use cases

What must XPRS be able of doing


## A. Around the station

### 1. Talk to people nearby from a browser
The station makes its own WiFi network and serves a chat page on it, so
somebody standing next to the box can talk to other XPRS users without
joining any network or installing anything.

### 2. Know which users are nearby
Say once a minute, for each radio separately, which other XPRS users it
can hear directly right now.

### 3. Set the station up from a phone
A new station is claimed, named and joined to a real WiFi network from a
phone, with no cable and nothing to type on the box.

### 4. Look after the station from a browser
From a browser on the same WiFi, see which users the station hears, read
what it has stored, read its log, and give it a message to send.

### 5. Update the station's software
Install a new version of its own software over the network, either when
asked or on its own schedule.


## B. Between stations within reach

### 6. Talk to other XPRS devices nearby
Hold conversations in XPRS with every station in range, over Bluetooth,
XWiFi and the WiFi network at the same time.

### 7. Pass on messages it hears
When it hears a message it cannot deliver directly, repeat it so
stations further away get it too, recording that it did.

### 8. Introduce itself to strangers
Announce who it is and what it is able to do, so that anybody listening
can tell a fixed station from somebody's phone.

### 9. Answer "what did I miss?"
Keep what it hears, and replay it to a station that asks what happened
while that station was switched off or asleep.

### 10. Hold a message for someone who is away
Keep a message addressed to a user it cannot reach right now, and hand
it over as soon as that user comes back into range.

### 11. Repeat a message for people who just arrived
After a quiet spell, repeat one stored message, so somebody who walked
into range a moment ago still hears it.


## C. Out to the internet

### 12. Reach the internet over Reticulum
Open an outbound connection to a Reticulum hub and announce itself,
politely enough not to be ignored.

### 13. Send its own messages out to the internet
Hand everything it has published, plus its list of who it hears, to the
archives its owner chose, and to nobody else.

### 14. Say where to send things to it
Publish an address on Reticulum so that a station anywhere on the
internet can send it something without ever having heard it.

### 15. Act as a small archive
Keep its own short archive and answer questions from other stations, so
it counts as an archive alongside the large ones on the internet.

### 16. Catch up on what it missed while it was off
After a restart or a power cut, ask each archive what happened while it
was gone, and back off when told it is asking too much.


## D. Joining the two worlds

### 17. Tell the internet who it can hear
Report which users it can hear, so that somebody on another continent
can learn which station on the internet is closest to the person they
want to reach.

### 18. Bring nearby devices onto the internet
Carry the announcements of nearby Bluetooth and XWiFi stations up into
Reticulum, so a device in the room is reachable from the other side of
the world, without flooding the radio with Reticulum's own traffic.

### 19. Deliver internet messages to nearby devices
A message sent from anywhere on the internet to a user in this room
arrives on that user's phone.

### 20. Prove who it heard instead of being trusted
Sign the list of who it hears, so nobody can lie about having heard a
user and redirect other people's traffic.

### 21. Talk to other kinds of radio mesh
On a board with a LoRa radio, translate between XPRS and other mesh
networks such as MeshCore or Meshtastic, carrying conversations and
names both ways, but never sending anything back out again.

### 22. Keep off amateur radio without a licence
Never transmit on amateur bands under a self-generated callsign, and
never put encrypted messages there.


## E. Finding an archive

### 23. Get an archive chosen for it automatically
A station with no archive of its own finds one that is offering to be an
archive, prefers one it can reach over the internet over one that would
need a radio in the room, and keeps the one it found instead of picking
a new one every hour.

### 24. Let the owner choose favourite archives
The owner decides which archives this station hands its messages to and
which ones it asks for what it missed. Choosing none is allowed: the
station then keeps everything for itself, serves it to whoever asks over
the radio, and is simply not findable by somebody who was not listening.

### 25. Let a user say who should hold their messages
A user publishes the stations that should keep their waiting messages
when they cannot be reached, in order of preference, and those stations
become the mailboxes. A boat naming the marina it checks into can then
be reached by somebody who only knows the marina.

### 26. Notice that a station is back and catch it up
When a station that offers an archive is heard again after a silence,
ask it for everything that happened while it was away, so both copies
end up holding the same history without either having promised to
remember anything.


## F. Archives talking to each other

### 27. Publish which users it keeps
Each archive publishes a list of the users whose words it holds and when
it last heard each of them, as a file anybody can fetch and check
against the signature of the archive that published it. A quiet
archive's list never changes, so checking on it costs nothing.

### 28. Never copy each other's stored messages
Archives exchange lists and sightings, never the messages themselves.
Each one keeps only what its own owner agreed to hold, so a mistake or a
deliberate poisoning stays with the archive that made it.

### 29. Share sightings of who was heard where
Each archive keeps a small table of which user was heard by which
station, on which radio, and when, and passes those sightings to the
other archives. The answer to "where can I reach this person" becomes
the sum of many small tables rather than one server that has to be
trusted by everybody.

### 30. Say who to try instead
Asked about a user it does not have, an archive says plainly that it
does not have it and names the archives that do. The reader then goes
and asks them directly, and the archive that redirected never carries
the messages itself.

### 31. Find a user nobody has heard for months
Each archive remembers the stations that used to hear a given user
regularly. A message sent long after the last live sighting can still
find its way, because the marina, the repeater or the hill that always
saw that person is still remembered.

### 32. Keep a neighbourhood's notices alive together
Two archives placed near each other can keep each other's public
notices, warnings, events and town chatter alive, so a community does
not lose its noticeboard when one archive goes dark. Neither is obliged
to, and private messages never take part.


## G. How far a message may go

### 33. Keep a conversation inside the building
Mark a message so it only travels on short-range radios and the local
network, and never onto a radio band, a satellite or the internet. A
question asked in a marina should not arrive in the next county.

### 34. Keep a conversation across the valley
Mark a message so it travels on any short-range or long-range radio but
never onto the internet: a flooded road, a lost dog, a market that moved
to Saturday.

### 35. Let a conversation travel as far as it can
Leave a message unmarked and it may go anywhere, on any radio, which is
what most messages are. Anything more private has to say so, because
silence is not a restriction.

### 36. Keep a message inside one country
Mark a message with a country and it is not carried out of that country,
which is what an event, a road closure or a public meeting needs.

### 37. Know which radios may carry what
Every radio is one of three kinds: short-range like Bluetooth and WiFi,
long-range like LoRa and VHF, or worldwide like the internet and
satellites. A mark of short-range or long-range allows its own kind and
everything narrower.

### 38. Refuse to carry something that should not travel
A station that moves packets out of its area must obey the mark on
each one: never publish a message marked short-range, never put a
valley message on the internet. Silence and an unmarked message are
very different things.

### 39. Show three conversations, not one
A client shows short-range traffic as the room of whoever is actually
here, long-range traffic as the valley, and unmarked traffic as the
conversation that travels. Mixing them into one list throws away the
only thing the mark was for.

### 40. Carry a message nowhere on purpose
A station holding a message for someone it cannot reach drops it rather
than carrying it to another town if it was marked short-range, and never
hands a valley message to an archive across the internet.


## H. Warnings and notices

### 41. Warn about danger in a place
Publish a fire, a flood, a storm or an outage as a circle on the map
with what kind it is and how bad it is, so a receiver knows whether
it is inside the danger without asking anybody.

### 42. Say what is worth knowing but not yet dangerous
Publish a queue, a stopped vehicle, standing water or fog as the same
shape but a quieter kind, so a reader can ask for hazards without also
being handed every road closure in the district.

### 43. Let a warning travel further and louder than a chat message
A warning or a call for help is repeated up to nine times instead of
three, and is never encrypted, because being read late by a stranger is
better than not arriving.

### 44. Know whether a warning is still true
Show when a warning was issued and when it is expected to end, so a fire
warning that arrives three days late is not plotted as happening now.

### 45. Give a newcomer the warnings of the place it just walked into
A station standing in a place keeps repeating its warnings and notices
to each user who arrives, once each, until the alert ends. Somebody
who reaches the marina an hour after the harbour master warned about
the lower car park never heard it, and nobody is going to repeat it.

### 46. Decide whose warnings it will repeat
By default a station repeats only the warnings posted by its owner.
An owner can open it to anybody whose signature checks out, which is
what a campsite wants and a private house does not.

### 47. Take a warning back when it turns out to be wrong
Withdraw a warning or a notice, or correct it, so that a station which
kept the original stops giving it out. The withdrawal is kept for
exactly as long as the warning it cancels.

### 48. Never give a place's warning to somebody from far away
Warnings and notices about a place are marked short-range and are only
given to users heard on a local radio, never to somebody arriving over
LoRa, a satellite or the internet, which are not the place.


## I. Making room when the archive fills

### 49. Throw away the oldest chatter first
When storage runs out, the first to go is ordinary heard traffic, oldest
before newest, because any other station's copy overlaps it and the
missing part can be asked for again.

### 50. Keep mail for people who chose this archive longest
A message held for a user who named this archive as their mailbox is
the last thing thrown away, because that user checks here first. Mail
held for somebody who did not choose it goes before that.

### 51. Refuse new mail out loud rather than lose somebody's
An archive that cannot take another message without dropping the
messages it promised to keep says so, and names another archive with
room, rather than quietly losing somebody's mail.

### 52. Throw away photos and downloads before words
Files are kilobytes to megabytes and messages are at most 250 bytes, so
a full archive gives up the pictures it downloaded for its own reading
first, then files deposited for others, and keeps its own content and
anything an owner pinned until last.

### 53. Stop offering a file it has already deleted
When it gives up a file it stops saying it holds it, so nobody is sent
across the internet to an archive that no longer has the picture.

### 54. Never keep anything past its own expiry
A message, a warning, a file or a mailbox declaration is dropped when
the time it named ends, whatever the pressure on storage, and an alert
that nobody has withdrawn outlives the rest of the archive only as long
as its own expiry.


## J. Callsigns the government gave me

### 55. Transmit under the callsign on my licence
Set the station to put the licence callsign in place of its own name,
keeping the same key underneath, and announce once which key belongs to
that callsign. Every packet from then on is checkable as the licence
holder's, and the station keeps answering to its old name so nothing
that already knew it breaks.

### 56. Prove the licence is mine and that I am here now
The announcement shows which key belongs to the callsign. A challenge
shows the holder of that key is at the transmitter now, so a packet
replayed from a recording is not mistaken for a live station. That
challenge is a sealed question and is never sent on a licensed band, so
it is done on licence-free spectrum and the result carried across.

### 57. Keep the amateur band lawful
Signing is fine there: the words stay in clear for anyone listening.
Sealing is not, and neither is carrying anybody else's traffic there
under a name nobody issued. The station signs, never seals, and drops
what it cannot legally transmit rather than repeating it for somebody
else, because the licence answers for the bridge and not for the
sender.
