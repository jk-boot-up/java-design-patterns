# Idempotent Consumer — Video

Sixteen scenes, narrated end to end.

## Scenes

| # | Key | Kind | What it does |
| --- | --- | --- | --- |
| 1 | `01-poster` | poster | Title card and thumbnail. States what the video is, who made it, what the pattern is in plain words, and what it means for an online shop. |
| 2 | `02-at-least-once` | bullets | Why the broker sends the same message twice, and why that is a contract rather than a bug. |
| 3 | `03-the-set` | code | The version everybody writes: a set of message ids, held in a field. |
| 4 | `04-act-one` | console | It works. The duplicate is skipped, the test is green, and this is what ships. |
| 5 | `05-act-two` | console | A deploy lands between the two deliveries. The database survived it; the set did not. |
| 6 | `06-not-unlucky` | quote | The restart is often *why* the acknowledgement went missing, so the two arrive together. |
| 7 | `07-act-three` | console | No restart at all — just a crash between doing the work and recording the id. |
| 8 | `08-one-cause` | quote | The hinge. Wrong place, wrong moment, one cause: they are being treated as two things. |
| 9 | `09-one-commit` | code | The whole mechanism. The effect and the record, in one transaction. |
| 10 | `10-the-shape` | diagram | The four consumers, and where the memory lives in each. |
| 11 | `11-act-four` | console | The redelivery is ignored, and the two failures that beat the `HashSet` bounce off. |
| 12 | `12-exactly-once` | quote | Exactly-once processing out of at-least-once delivery — and where that guarantee lives. |
| 13 | `13-did-you-need-it` | console | The handler that needed no store, and the one rewritten until it needed none either. |
| 14 | `14-the-window` | console | The store's own cost: a table to operate, and an expiry window that is a guess. |
| 15 | `15-the-handover` | quote | One stable message id is everything the sending side owes you. |
| 16 | `16-outro` | outro | Three things you get, two things you pay, and the cheaper question to ask first. |

## Building

```bash
cd video
python3 make_slides.py      # 16 PNGs into build/
./build_video.sh            # narration + slides -> idempotent-consumer-pattern-explained.mp4
python3 make_subtitles.py   # .srt alongside the mp4
```

The narration uses the macOS `say` voice Samantha at 145 words per minute, and
`ffmpeg` stitches the audio to the slides. Rendered output — the mp4, the m4a,
the srt — is deliberately not committed; only the sources and `poster.png` are.

## Notes On The Shape

**Scenes 3 to 8 come before the mechanism on purpose.** The commit is a boring
idea until the room has watched a green test ship a bug twice over, for two
different reasons. Scene 8 is the hinge that names the single cause underneath
both failures.

**Scene 6 exists because the failure sounds like bad luck and is not.** A
restart is frequently why the acknowledgement went missing, so the redelivery
and the wiped memory arrive as a pair far more often than chance suggests.

**Scenes 13 and 14 must not be cut.** Thirteen is the handler that needed no
dedupe store at all, and the rewrite from "add seventy points" to "set the
points for this order to seventy" — a viewer who leaves adding a dedupe table
to every consumer has been made worse at this. Fourteen is the expiry window,
which is chosen rather than derived, and it is the honest ending.

**Every number is exact.** Every figure spoken or shown comes from the real
output of `./gradlew run` — two confirmations for one order in acts two and
three, one in act four, a hundred and forty loyalty points for a seventy pound
order, and the duplicate that gets through after a thirty-second memory expires.

**The outro names no other pattern.** It closes on what the sending side owes
the receiving side, without announcing what comes next, because the publishing
order of these videos is not fixed.

Suggested description:

> Learn the idempotent consumer in Java 21, starting with why a broker sends
> the same message twice — which is a contract rather than a bug. The
> version everybody writes is a set of message ids held in a field. It
> works, the duplicate is skipped, the test is green, and that is what
> ships. Then a deploy lands between the two deliveries: the database
> survived it and the set did not. And it is not bad luck, because a restart
> is often the very reason the acknowledgement went missing, so the two
> arrive together. A second failure needs no restart at all — just a crash
> between doing the work and recording the id. One cause underneath both:
> the effect and the record are being treated as two things. So the
> mechanism is to put them in one transaction, and the two failures that
> beat the in-memory set bounce off. That is exactly-once processing built
> out of at-least-once delivery. We finish on the store's own cost — a table
> to operate and an expiry window that is a guess — and on the cheaper
> question to ask first, which is whether your handler needed any of this.
