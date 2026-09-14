# Transactional Outbox — Video

Sixteen scenes, about eleven minutes, narrated end to end.

## Scenes

| # | Key | Kind | What it does |
| --- | --- | --- | --- |
| 1 | `01-poster` | poster | Title card and thumbnail. States what the video is, who made it, what the pattern is in plain words, and what it means for an online shop. |
| 2 | `02-scenario` | bullets | Two things that must happen together: save the order, tell everybody else. Two systems, no shared transaction. |
| 3 | `03-two-lines` | code | The version everybody writes first. Save, then publish, on two lines. |
| 4 | `04-act-one` | console | It works. One order, one event, one email — and this is what every test will see. |
| 5 | `05-act-two` | console | A deploy lands between the two lines. The order is real, and nobody will ever be told. |
| 6 | `06-nothing-to-retry` | quote | The hinge. Nothing recorded that a message was owed, so nothing can retry it. |
| 7 | `07-the-tempting-fixes` | bullets | "Swap the lines" and "wrap it in a transaction", taken seriously and taken apart. |
| 8 | `08-the-out-tray` | quote | The analogy: the letter goes in the tray at the same moment you file your copy. |
| 9 | `09-two-rows-one-commit` | code | The whole mechanism. Two rows, one commit, and no broker anywhere in sight. |
| 10 | `10-the-shape` | diagram | The two halves — the checkout, and the relay that runs later for a different reason. |
| 11 | `11-act-three` | console | One commit writes both rows; the sweep delivers the message afterwards. |
| 12 | `12-act-four` | console | The broker is down. Checkout does not notice, and the retry nobody wrote works. |
| 13 | `13-act-five` | console | The bill. The relay dies after publishing, and the customer gets two emails. |
| 14 | `14-at-least-once` | quote | Why the duplicate cannot be removed, only pointed in a direction. Never lost, sometimes twice. |
| 15 | `15-the-handover` | console | The stable message id, and what it is worth if the receiver is Payments. |
| 16 | `16-outro` | outro | Three things you get, four things you pay. |

## Building

```bash
cd video
python3 make_slides.py      # 16 PNGs into build/
./build_video.sh            # narration + slides -> transactional-outbox-pattern-explained.mp4
python3 make_subtitles.py   # .srt alongside the mp4
```

The narration uses the macOS `say` voice Samantha at 145 words per minute, and
`ffmpeg` stitches the audio to the slides. Rendered output — the mp4, the m4a,
the srt — is deliberately not committed; only the sources and `poster.png` are.

## Notes On The Shape

**Scenes 3 to 6 come before the mechanism on purpose.** The outbox is a boring
idea until the room has watched an order get lost with no error and nothing to
retry. Scene 6 is the hinge: the point is not that the send failed, it is that
nothing anywhere knew a send was owed.

**Scene 7 answers the room out loud.** "Swap the lines" is the most common
suggestion in any session on this pattern, so the video makes it and refutes it
rather than waiting for a comment thread to.

**Scenes 13, 14 and 15 must not be cut.** They are the reason this video exists.
Most explanations of the outbox stop at scene 12, with the message safely
delivered, and leave the viewer believing they have bought exactly-once
delivery. The duplicate is not a bug in the demo; it is the guarantee.

**Every number is exact.** Every figure spoken or shown comes from the real
output of `./gradlew run` — fifteen milliseconds for a publish, seven for a
notification, seventy pounds ninety-five for the order, two emails in the inbox.

**The outro names no other pattern.** It says what the outbox hands over to
whoever receives the message, without announcing what comes next, because the
publishing order of these videos is not fixed.
