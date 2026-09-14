# Video — Database per Service

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
| `database-per-service-pattern-explained.mp4` | 1080p H.264 + AAC, ready for YouTube |
| `database-per-service-pattern-explained.m4a` | audio-only, for listening rather than watching |
| `database-per-service-pattern-explained.srt` | subtitles, one cue per narrated sentence |
| `poster.png` | the first frame, lifted out for use as the thumbnail |
| `build/` | one PNG and one clip per scene, kept for inspection |

Runtime is approximately seventeen and a half minutes across sixteen scenes.

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
| 2 | `02-scenario` | bullets | Two teams, one schema, and the page that reads both tables |
| 3 | `03-one-query` | code | The join, and the constant that names another team's column |
| 4 | `04-act-one` | console | Two complete rows and one round trip — the number the rest of the video is measured against |
| 5 | `05-be-fair` | bullets | The shared database at its best: one trip, a join that cannot forget a name, a foreign key |
| 6 | `06-act-two` | console | Tuesday. A correct migration, a green build, and a dead page in another repository |
| 7 | `07-nobody-wrong` | quote | Nobody did anything wrong — and the passing test called `aRenameBreaksTheOrderHistoryPage` |
| 8 | `08-filing-cabinet` | quote | The shared filing cabinet, including the part people skip: the second cabinet costs something |
| 9 | `09-tempting-fixes` | bullets | A test (in whose repo?), a rule nobody writes down, and a view that does not change who decides |
| 10 | `10-the-mechanism` | code | The whole mechanism, and the sentence that matters most: in production nothing throws it |
| 11 | `11-act-three` | console | The same page rebuilt without a join — 20ms and two service calls instead of one query |
| 12 | `12-ask-once` | bullets | Why `namesFor` takes a list, and how a fifty-row page becomes fifty network calls |
| 13 | `13-roles` | diagram | The shared schema and its exception on one side; the two services, the page and the refusal on the other |
| 14 | `14-act-four` | console | The payoff, and being precise about it: no speed, no correctness, only the right to change your mind |
| 15 | `15-act-five` | console | The bill — the join, and then the foreign key, which is the expensive one |
| 16 | `16-outro` | outro | The un-batching exercise, the question about your own schema, and the sign-off |

## Notes on the shape

Scenes 3, 4, 6, 10, 11, 14 and 15 are not plain text — they are real source and
real demo output. If the project's code or its printed output changes, those slides
go stale silently, because nothing in the build checks them against the source.
Re-run `./gradlew run` and compare before rebuilding.

Scene order is the argument, and the first third of it is unusual for this series.
Scene 5 exists to make the shared database look *good*, and it is not padding: a
viewer who suspects the shared schema is a straw man will hear everything after it
as marketing. The pattern cannot be introduced until its alternative has been given
its best case.

Two scenes must not be cut or moved earlier. Scene 10 is the honest statement that
in production nothing throws the exception — the rule is database credentials —
and without it the audience leaves thinking this pattern is a coding convention.
Scene 15 is the bill, and it is two separate losses rather than one: the join, and
then the foreign key. The second is the one people forget, and a viewer who leaves
believing the split is free has learned something worse than nothing.

Unlike the bulkhead video, every number on these slides is exact and repeatable.
Nothing in this project sleeps; `SimulatedClock` advances ten milliseconds per
service call, so act three prints 0, 10 and 20 milliseconds on any machine.

On `bullets` and `quote` slides the body starts at y=260 and steps 60 pixels a
line, with the footer at y≈1022 — so twelve body lines is the hard maximum, and
nothing warns you if you exceed it.
