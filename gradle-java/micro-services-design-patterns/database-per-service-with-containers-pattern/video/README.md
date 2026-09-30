# Database per Service with Containers Pattern — Teaching Video

A narrated, slide-based video that teaches Database per Service on two real
databases, PostgreSQL and MongoDB. It shows one shared database working and
then breaking when one team renames a column, the split surviving the same
change, the old join tried from both sides — refused by Postgres, quietly
answered with nothing by MongoDB — a delete no foreign key can stop, and a
rollback that reaches one engine and not the other. It also argues for when
not to use it. The examples come from this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `database-per-service-with-containers-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `database-per-service-with-containers-pattern-explained.m4a` | Audio-only version. |
| `database-per-service-with-containers-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Not the thumbnail. |

None of these is committed except `poster.png`. The rest are rebuilt from the
source in this directory.

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

## Rebuilding

```bash
./build_video.sh
```

A build takes eight to ten minutes. It runs in five steps:

1. **Slides.** `make_slides.py` renders one 1920×1080 PNG per scene into
   `build/`, from the text in `scenes.py`.
2. **Narration text.** Each scene's narration is written to its own text file.
   The `[[slnc 250]]` marks in it are pauses, in milliseconds, that `say` obeys.
3. **Voice and scene clips.** macOS `say` reads each scene aloud. The voice is
   lightly cleaned on its way to 48 kHz: a careful resample, a high-pass filter
   at 75 Hz to drop rumble, and a small lift around 3 kHz where consonants live.
   There is deliberately no denoiser. Synthesised speech has almost no noise
   floor, so a denoiser ends up removing parts of the voice and leaves it
   sounding underwater. Each slide is then held for exactly as long as its
   narration, to the frame.
4. **Joining.** The scenes are joined into one timeline. The audio is joined as
   uncompressed sound first and compressed once, because clips compressed
   separately each carry a few samples of padding, which would click at every
   join.
5. **Levelling.** The whole narration is brought to −16 LUFS, the loudness
   YouTube plays at, with ffmpeg's `loudnorm` filter. This is done once over the
   whole timeline, not per scene, because levelling each scene on its own would
   push quiet scenes up and loud ones down, and the level would jump at every
   cut. It runs in two passes: the first measures the whole narration, the
   second applies the measured figures as one constant gain, so the result
   lands on the target and nothing rides up and down within it. The narration
   is compressed to AAC exactly once, here.

At the end the script checks the audio track packet by packet and prints
`audio timeline continuous: NNNNN packets, no gaps`. If that line is missing,
or reports a gap, the build has failed even if an mp4 was written: a gap is a
click or a silence in the video. Subtitles are written by `make_subtitles.py`,
which splits each scene's narration into caption-sized cues and spreads them
across that scene's measured length in the finished timeline.

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

The video itself needs no container runtime; only the demo does.

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Database per Service with Containers | Title card and the definition |
| 2 | The Scenario | cust-7's two orders, a page owned by Orders, names owned by Catalog |
| 3 | Postgres's Words | Table, SQL, join, foreign key, transaction, rollback, error codes, through a spreadsheet |
| 4 | One Shared Database | Act one: one join, 1 round trip, a delete refused with 23503 |
| 5 | The Rename | Act two: a correct rename, and somebody else's page fails with 42703 |
| 6 | MongoDB's Words | Document, collection, find, lookup, through a drawer of filled-in forms |
| 7 | Two Services, Two Engines | Act three: two shapes of product, 2 round trips, a rename that changes 2 documents and nothing else |
| 8 | Who Can Reach What | Each service reaches its own engine only |
| 9 | The Whole Pattern, In Two Constructors | What each service is handed, and what it is not |
| 10 | The Join, Tried Anyway | Act four: 42P01 and 0A000 from Postgres; no error and 0 orders from MongoDB |
| 11 | No Foreign Key Between Engines | Act five: MongoDB deletes the kettle, and nothing refuses |
| 12 | The Bill | Act six: a rollback that leaves 38 mugs, a page half there, 2 of everything |
| 13 | What The Simulation Left Out | The contrast with the hand-built twin |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | Postgres 18.6 and MongoDB 8.3.11 in containers the demo owns, and when one database is better |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 docs/make_narration.py --force database-per-service-with-containers` from the
`gradle-java` directory, then re-run `./build_video.sh`.

Every narration line speaks its counts, outcomes and error codes in words,
explains each term Postgres and MongoDB introduce before using the tool's name
for it, and never points at a picture the listener cannot see. Every number
matches the output of `./gradlew run`.

## Publishing Notes

Upload `database-per-service-with-containers-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Database per Service pattern in Java: each service keeps its own data in its
> own database, no other service may read it directly, and if you want
> somebody else's data you ask them. Explained with two real databases,
> PostgreSQL and MongoDB, running in containers. In our online store, the
> Orders team and the Catalog team each get a database of their own, of two
> different kinds. We watch one shared database work well and then break on a
> rename, the split survive the same change, and the old join tried against
> two real engines: one refuses it out loud, the other says nothing at all.
