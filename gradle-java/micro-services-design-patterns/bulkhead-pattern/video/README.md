# Video — Bulkhead

Everything needed to rebuild the narrated teaching video for this project. The
rendered video, its audio-only version and the subtitle file are deliberately not
committed; run `./build_video.sh` and they appear here in about ten minutes.

## Building it

```bash
cd video
./build_video.sh
```

Requirements are macOS (for the `say` voice), `ffmpeg`, and Python with Pillow.
Nothing else, and no network.

Outputs:

| File | What it is |
| --- | --- |
| `bulkhead-pattern-explained.mp4` | 1080p H.264 + AAC, ready for YouTube |
| `bulkhead-pattern-explained.m4a` | audio-only, for listening rather than watching |
| `bulkhead-pattern-explained.srt` | subtitles, one cue per narrated sentence |
| `poster.png` | the first frame, lifted out for use as the thumbnail |
| `build/` | one PNG and one clip per scene, kept for inspection |

Runtime is approximately seventeen minutes across sixteen scenes.

## The files

| File | What it holds |
| --- | --- |
| `scenes.py` | the sixteen scenes: title, kind, body and narration |
| `make_slides.py` | renders each scene to a 1920×1080 PNG |
| `make_subtitles.py` | turns the narration into timed `.srt` cues |
| `build_video.sh` | narrates, renders, concatenates and muxes |

The narration is also lifted out to [`narration.md`](narration.md), which is the
readable version — useful for reviewing the wording without opening Python.

## The scenes

| # | Scene | Kind | What it does |
| --- | --- | --- | --- |
| 1 | `01-poster` | poster | States what the video is, credits the author, gives the plain definition, then the e-commerce framing |
| 2 | `02-scenario` | bullets | One pool, and two jobs with nothing in common: checkout, and an overnight supplier feed |
| 3 | `03-the-shared-pool` | code | The shared pool, presented fairly: no bug, every test passes, nobody would object in review |
| 4 | `04-act-one` | console | Four batches take four threads, and the shopper is still waiting after 300ms |
| 5 | `05-absence` | bullets | Checkout has no line at all — starved and broken look identical from outside |
| 6 | `06-the-hull` | quote | The ship's hull, in full, and the part people skip: the walls take up space |
| 7 | `07-tempting-fixes` | bullets | A bigger pool moves the number; an unbounded queue moves the failure somewhere worse |
| 8 | `08-the-mechanism` | code | The whole mechanism, deliberately an anticlimax: a fixed pool, a bounded queue, a name |
| 9 | `09-act-two` | console | Same bad night, and the sale goes through on `checkout-worker` while the feed jams |
| 10 | `10-roles` | diagram | Bulkhead, the executor underneath it, the two jobs, and the gate that stands in for the slow partner |
| 11 | `11-still-stuck` | quote | How we know it was the wall and not luck: the test that asserts the feed is *still* jammed |
| 12 | `12-act-three` | console | A fifth batch with nowhere to go, refused in 0ms — four accepted, one refused |
| 13 | `13-refusing` | bullets | Why refusing immediately is a feature: a named pot, a caller with options, a chosen blast radius |
| 14 | `14-act-four` | console | The bill — two idle threads beside two jobs waiting for a thread |
| 15 | `15-costs` | bullets | Where the walls go, why fifteen of them is a failure mode, and the circuit breaker beside it |
| 16 | `16-outro` | outro | The one-line exercise, the question to sit with, and the sign-off |

## Notes on the shape

Scenes 3, 4, 8, 9, 12 and 14 are not plain text — they are real source and real demo
output. If the project's code or its printed output changes, those slides go stale
silently, because nothing in the build checks them against the source. Re-run
`./gradlew run` and compare before rebuilding.

Scene order is the argument, and it is shaped differently from the rest of the
series. The mechanism in scene 8 is deliberately an anticlimax, and it is placed
late so that it lands as a decision rather than as a technique: everything before
it is about a failure you cannot see, and everything after it is about what the fix
costs. Scene 11 is the one that turns the demo from anecdote into evidence, and it
has to stay immediately after act two while the good result is still fresh enough
to be doubted. Scene 14 — the bill — must not move earlier or be dropped. A viewer
who leaves thinking bulkheads are free has learned something worse than nothing.

One caution specific to this project: the timestamps on the act one and act two
slides are real milliseconds from real threads, not a simulated clock, so a rebuild
on a different machine will print numbers a millisecond or two away from the ones
on the slides. That is expected. What the tests assert is order and thread name,
never an exact duration, and the slides quote a representative run.

On `bullets` and `quote` slides the body starts at y=260 and steps 60 pixels a
line, with the footer at y≈1022 — so twelve body lines is the hard maximum, and
nothing warns you if you exceed it.

Suggested description:

> Learn the bulkhead pattern in Java 21, starting from one thread pool doing
> two jobs with nothing in common: taking a customer's order, and importing
> an overnight supplier feed. The shared pool is presented fairly — no bug,
> every test passing, nobody would object in review — and then four slow
> batches take four threads and the shopper is still waiting. Notice what
> the logs show: nothing. Starved and broken look identical from outside. We
> use a ship's hull for the analogy, including the part people skip, which
> is that the walls take up space. A bigger pool only moves the number and
> an unbounded queue moves the failure somewhere worse. The mechanism itself
> is deliberately an anticlimax: a fixed pool, a bounded queue, and a name.
> The same bad night now sells the espresso machine while the feed jams, a
> fifth batch is refused in zero milliseconds, and the bill is two idle
> threads sitting beside two jobs waiting for a thread.
