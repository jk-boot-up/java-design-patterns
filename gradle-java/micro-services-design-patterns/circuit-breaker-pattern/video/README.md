# Video — Circuit Breaker

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
| `circuit-breaker-pattern-explained.mp4` | 1080p H.264 + AAC, ready for YouTube |
| `circuit-breaker-pattern-explained.m4a` | audio-only, for listening rather than watching |
| `circuit-breaker-pattern-explained.srt` | subtitles, one cue per narrated sentence |
| `poster.png` | the first frame, lifted out for use as the thumbnail |
| `build/` | one PNG and one clip per scene, kept for inspection |

Runtime is approximately eighteen minutes across sixteen scenes.

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
| 2 | `02-scenario` | bullets | Recommendations has stopped answering — not refusing, which would be easy |
| 3 | `03-just-retry` | code | The retry loop, presented fairly: no bug, correct page, every test passes |
| 4 | `04-act-one` | console | Nine seconds for a page identical to the one you'd have had immediately |
| 5 | `05-three-costs` | bullets | The third cost — idle threads — is the one that stops checkout working |
| 6 | `06-fuse-box` | quote | The analogy, in full, before any class name is spoken |
| 7 | `07-vocabulary` | bullets | Closed, open, half-open — think of a wire, not a door |
| 8 | `08-the-breaker` | code | The three questions inside `call`, and why a success resets rather than decrements |
| 9 | `09-act-two` | console | Six pages, three calls, three refusals — and the clock stops moving |
| 10 | `10-roles` | diagram | One breaker class, three states, four callers, and where the decision lives |
| 11 | `11-act-three` | console | Five seconds later, one probe, and nobody deployed anything |
| 12 | `12-fail-fast` | quote | The hinge: it makes failures fast, not invisible |
| 13 | `13-act-four` | console | Checkout has no fallback, so speed buys a fast honest "no" |
| 14 | `14-act-five` | console | The same wiring, one different catch block, and a receipt for money that never moved |
| 15 | `15-costs` | bullets | What it costs, how it is tuned badly, and when not to bother |
| 16 | `16-outro` | outro | The exercise, the question to sit with, and the sign-off |

## Notes on the shape

Scenes 3, 8, 13 and 14 are not plain text — they are real source and real demo
output. If the project's code or its printed output changes, these four slides go
stale silently, because nothing in the build checks them against the source.
Re-run `./gradlew run` and compare before rebuilding.

Scene order is the argument, and it has two halves. The mechanism is shown
*working* in scenes 6 to 11 before the word *fallback* is used for anything harder
than an empty list of suggestions. Only then do scenes 12 to 14 ask what the speed
is actually for. Moving the checkout scenes earlier turns the video into a warning
rather than an explanation, so scenes 12 and 14 are the ones to be careful with if
you ever rearrange it.

On `bullets` and `quote` slides the body starts at y=260 and steps 60 pixels a
line, with the footer at y≈1022 — so twelve body lines is the hard maximum, and
nothing warns you if you exceed it.

Suggested description:

> Learn the circuit breaker pattern in Java 21, starting from a service that
> has stopped answering — not refusing, which would be easy, but simply not
> replying. The retry loop is presented fairly: no bug, the right page,
> every test passing, and nine seconds spent producing a page you could have
> had immediately. The third cost is the one that actually breaks the shop:
> while those threads wait, checkout cannot get one. We use a fuse box as
> the analogy and then build the breaker as three questions inside one
> method, with the states named as a wire rather than a door — closed, open,
> half open — and a success that resets rather than decrements. Six pages,
> three calls, three refusals, and the clock stops moving. Then the hinge: a
> breaker makes failures fast, not invisible. Checkout has no fallback, so
> speed buys it a fast honest no, and the same wiring with one different
> catch block prints a receipt for money that never moved.
