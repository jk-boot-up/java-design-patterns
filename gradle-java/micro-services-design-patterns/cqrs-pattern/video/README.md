# Video — CQRS

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
| `cqrs-pattern-explained.mp4` | 1080p H.264 + AAC, ready for YouTube |
| `cqrs-pattern-explained.m4a` | audio-only, for listening rather than watching |
| `cqrs-pattern-explained.srt` | subtitles, one cue per narrated sentence |
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
| 2 | `02-scenario` | bullets | One page, two services behind it, and the ratio: written once, read a thousand times |
| 3 | `03-every-view` | code | `ComposingOrderHistory`, read generously — the catalog call is batched and nobody would object to it |
| 4 | `04-act-one` | console | Three identical views, 270ms and six service calls, and the quieter problem: the page needs other services to be up |
| 5 | `05-the-obvious-fix` | bullets | So cache it — stated as the good idea it is, and taken seriously before it is taken apart |
| 6 | `06-the-cache` | code | The cache in full, and the question it cannot answer: how would it ever find out it is wrong? |
| 7 | `07-act-four` | console | A rename. One copy is still saying the old name; the other was corrected by the event that made it wrong |
| 8 | `08-cannot-know` | quote | Cache versus read model, stated without the word "fast", plus why no expiry setting bridges them |
| 9 | `09-the-mechanism` | code | Publish what you did, switch over a sealed event type, keep the answer ready. It should feel small |
| 10 | `10-act-two` | console | 15ms and zero service calls — and the honest line that the work moved to write time rather than vanishing |
| 11 | `11-what-it-costs` | bullets | The bill: the ratio, a second copy to keep, and a window where that copy is behind |
| 12 | `12-act-three` | console | Placed, paid for, final — and zero rows on the customer's page. The window, shown rather than described |
| 13 | `13-roles` | diagram | The composing design and the cache on one side; the write side, the bus, the read model and `rebuildFrom` on the other |
| 14 | `14-act-five` | console | The last kettle, the read model saying yes, and the ledger refusing — the rule with a price tag |
| 15 | `15-the-rule` | quote | Five sentences to carry away, ending on "show a read model's number, never decide with it" |
| 16 | `16-outro` | outro | The break-the-rule exercise, the read-to-write ratio question, and the sign-off |

## Notes on the shape

Scenes 3, 4, 6, 7, 9, 10, 12 and 14 are not plain text — they are real source and
real demo output. If the project's code or its printed output changes, those slides
go stale silently, because nothing in the build checks them against the source.
Re-run `./gradlew run` and compare before rebuilding.

Scene order is the argument, and the middle of it is the part that matters. Scenes
5 to 8 exist to give the cache its best case before dismantling it, and they are
not padding. A viewer who suspects the cache was a straw man will hear everything
after it as marketing — and worse, the audience has to *invent* this pattern by
asking what would have to be true for a copy to know it is wrong.

Two scenes must not be cut or moved earlier. Scene 12 is the frame where an order
is placed, paid for and final while the customer looks at a page with nothing on
it; a viewer who leaves believing this pattern is free has learned something worse
than nothing. Scene 14 is the rule with a price tag, and the video exists as much
for that rule as for the mechanism.

Every number on these slides is exact and repeatable. Nothing in this project
sleeps; `SimulatedClock` advances thirty milliseconds for an Orders call, sixty for
Catalog and five for a read-model lookup, so act one prints 270ms and act two
prints 15ms on any machine.

On `bullets` and `quote` slides the body starts at y=260 and steps 60 pixels a
line, with the footer at y≈1022 — so twelve body lines is the hard maximum, and
nothing warns you if you exceed it.
