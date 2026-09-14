# Video — Saga

The narrated teaching video for this project: sixteen scenes, about eighteen
minutes, built entirely offline from the sources in this folder.

## Scenes

| # | Key | Kind | What it does |
| --- | --- | --- | --- |
| 1 | `01-poster` | poster | Title card and YouTube thumbnail. States what the video is, credits the author, gives the plain definition, then the shop |
| 2 | `02-scenario` | bullets | One checkout, five services, and the sentence everything follows from: there is nothing to roll back |
| 3 | `03-the-try-block` | code | `NaiveCheckoutService` — four calls in a `try` block, taken seriously |
| 4 | `04-act-five` | console | The courier refuses. £70.95 taken, no parcel, and nothing threw |
| 5 | `05-transactional` | bullets | Why `@Transactional` does not help, and why nobody uses two-phase commit |
| 6 | `06-holiday` | quote | The holiday booking: flight, hotel, hire car, and the word "approximately" |
| 7 | `07-the-step` | code | `SagaStep` — execute, compensate, and whether it can be compensated at all |
| 8 | `08-the-orchestrator` | code | Forward keeping a list, backwards undoing it, and it never throws |
| 9 | `09-the-shape` | diagram | The whole cast: the design being replaced on the left, the mechanism on the right |
| 10 | `10-act-one` | console | The happy path, and the line that makes the rest necessary |
| 11 | `11-act-two` | console | The same refusal, walked backwards — and why reverse order is the only safe order |
| 12 | `12-in-reverse` | bullets | The turn: three things undoing costs you, named before they are shown |
| 13 | `13-the-ledger` | console | A charge and a refund. Two lines, not zero. Compensation is not rollback |
| 14 | `14-needs-human` | console | The refund fails too. The unwinding carries on, and there is a third outcome |
| 15 | `15-the-email` | console | There is no unsend, so steps that cannot be undone go last |
| 16 | `16-outro` | outro | Sign-off, one exercise, and the harder question |

## Building it

```bash
cd video
./build_video.sh
```

Needs macOS (for `say`), `ffmpeg`, and Python with Pillow. Output lands in
`build/`: `saga-pattern-explained.mp4`, an audio-only `.m4a`, and a `.srt`. The
poster is lifted out as `poster.png`, which is also the YouTube thumbnail.

Rendered media is deliberately not committed. The sources here are enough to
reproduce all of it.

Individual pieces, if you want to iterate on one part:

```bash
python3 make_slides.py      # slides only, into build/
python3 make_subtitles.py   # .srt from the narration timings
```

## Notes On The Shape

**Scenes 3 and 4 come before the mechanism, on purpose.** The pattern is boring
until the problem has been felt. Those two scenes are ten minutes of a live
session compressed, and cutting them leaves a viewer memorising an interface
they have no reason to want.

**Scene 12 is the hinge.** Most explanations of this pattern end at scene 11
with a happy summary. That does real damage, because everything up to there is
the easy half. Scene 12 names the three costs, and scenes 13, 14 and 15 pay
them one at a time.

**Scenes 13, 14 and 15 must not be cut or reordered.** The two-line ledger, the
compensation that itself fails, and the email that cannot be unsent are the
three facts that separate someone who can use this pattern from someone who has
heard of it.

**The outro names no other pattern.** Publishing order is not fixed, so no video
in this series announces what comes next.

**Every number is exact.** `SimulatedClock` advances by fixed amounts — 30ms for
Stock, 100ms for Payments, 20ms for Orders, 60ms for Shipping, 40ms for Email —
so the timelines on the console slides match `./gradlew run` on any machine,
and the £70.95 is the real total of the demo basket.
