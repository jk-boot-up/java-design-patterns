# Video — API Composition

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
| `api-composition-pattern-explained.mp4` | 1080p H.264 + AAC, ready for YouTube |
| `api-composition-pattern-explained.m4a` | audio-only, for listening rather than watching |
| `api-composition-pattern-explained.srt` | subtitles, one cue per narrated sentence |
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
| 2 | `02-scenario` | bullets | One ordinary order page, three services that own it, and no join any more |
| 3 | `03-three-calls` | code | The three-line version, presented fairly: no bug, right page, every test passes |
| 4 | `04-act-one` | console | 210ms — and the question of which call needed the one before it |
| 5 | `05-sixty-wasted` | bullets | Shipping waited 60ms for an answer it never looked at |
| 6 | `06-sandwich` | quote | The analogy, in full, before any class name is spoken |
| 7 | `07-not-flat` | bullets | Why it is one call then two together, not one flat burst of three |
| 8 | `08-the-fanout` | code | Handing work to the fan-out, and the word *branch* introduced early |
| 9 | `09-act-two` | console | Both leave at 30ms, the page costs 150ms, and the sum becomes a maximum |
| 10 | `10-roles` | diagram | Composer, fan-out, branch, and the three services labelled required or optional |
| 11 | `11-act-three` | console | The same outage: an error page built from two good answers, versus a page with a named hole |
| 12 | `12-name-the-gap` | quote | The hinge: it may say it does not know, it may not make something up |
| 13 | `13-act-four` | console | Orders down, the composer refusing, and why that is correct |
| 14 | `14-act-five` | console | 99.700% and 129.5 minutes — three good services make a worse page than any of them |
| 15 | `15-costs` | bullets | The slowest dependency, the extra load, and the decision that must be revisited |
| 16 | `16-outro` | outro | The one-line exercise, the question to sit with, and the sign-off |

## Notes on the shape

Scenes 3, 4, 8, 9, 11, 13 and 14 are not plain text — they are real source and real
demo output. If the project's code or its printed output changes, those slides go
stale silently, because nothing in the build checks them against the source. Re-run
`./gradlew run` and compare before rebuilding.

Scene order is the argument, and it has two halves. The first half, scenes 3 to 9,
is arithmetic: sequential calls cost the sum, parallel calls cost the maximum. The
second half, scenes 11 to 14, is a product argument rather than a technical one —
what a page is allowed to do when a dependency is missing. The two must stay in
this order, because "make the delivery section optional" means nothing until the
viewer has seen the fan-out work. Scene 14 is the one to be careful with if you
rearrange: the availability arithmetic is what turns the classification from a
nicety into the only lever there is, so it is the payoff and not the setup.

On `bullets` and `quote` slides the body starts at y=260 and steps 60 pixels a
line, with the footer at y≈1022 — so twelve body lines is the hard maximum, and
nothing warns you if you exceed it.

Suggested description:

> Learn API composition in Java 21: one ordinary order page, three services
> that own the parts of it, and no join available any more. The three-line
> version is presented fairly — no bug, right page, every test passing — and
> it takes two hundred and ten milliseconds, of which sixty were spent
> waiting for an answer nothing looked at. So we ask which call actually
> needed the one before it, and the shape turns out to be one call and then
> two together rather than one flat burst of three: both branches leave at
> thirty milliseconds, the page costs a hundred and fifty, and the sum
> becomes a maximum. The second half is about failure. A page may say it
> does not know; it may not make something up. So one outage produces a page
> with a named hole rather than an error page built from two good answers,
> and a different outage produces an honest refusal. We finish on the
> arithmetic that surprises people: three services at 99.9% make a page that
> is worse than any of them.
