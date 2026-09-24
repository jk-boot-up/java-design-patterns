# Transactional Outbox with Debezium Pattern — Teaching Video

A narrated, slide-based video that teaches the Transactional Outbox pattern on a
real Postgres database and a real Kafka broker, with Debezium reading Postgres's
own log in between — why saving the order and sending the event by hand can
half-happen, how one transaction and change data capture keep them together,
why a deleted outbox row is still sent, what the replication slot does while
Debezium is down, and why an event can arrive twice — using this project's
online store.

## Output Files

| File | What it is |
| --- | --- |
| `transactional-outbox-with-debezium-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `transactional-outbox-with-debezium-pattern-explained.m4a` | Audio-only version. |
| `transactional-outbox-with-debezium-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Not the thumbnail. |

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

## Rebuilding

```bash
./build_video.sh
```

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

The video itself needs no container runtime; only the demo does.

## How the audio is made

Everything below happens inside `build_video.sh`; nothing is read from any
other project.

1. **Slides.** `make_slides.py` draws one 1920×1080 PNG per scene into `build/`.
2. **Voice.** Each scene's narration from `scenes.py` is spoken by macOS `say`
   with the `Samantha` voice at 145 words per minute. The `[[slnc N]]` markers
   in the text are pauses of N milliseconds for `say`; they are not words and
   never reach the subtitles.
3. **Clean-up, per scene.** The voice is resampled to 48 kHz with a long filter
   so the upsampling adds no grit, a high-pass at 75 Hz removes rumble, and a
   small lift around 3 kHz makes consonants clearer. There is deliberately no
   denoiser: synthesised speech has almost no noise floor, and a denoiser ends
   up removing parts of the voice and making it warble.
4. **Frame-exact scenes.** Each scene's audio gets a short tail of silence and
   is padded to a whole number of video frames, so the slide changes cannot
   drift away from the voice over sixteen scenes. Audio stays as lossless WAV
   at this stage.
5. **One join, one encode.** All the WAV files are joined losslessly, and the
   whole narration is encoded to AAC exactly once. Encoding each scene
   separately and joining the results would leave a tiny gap at every scene
   change, because each AAC clip carries padding at its start and end.
6. **Loudness, once, over the whole video.** The joined narration is measured
   first, and then brought to −16 LUFS, the level YouTube plays at, as one
   constant gain (`loudnorm` in two passes, with `linear=true`). Levelling
   each scene on its own would make quiet scenes jump up to match loud ones.
7. **The continuity check.** At the end the script reads every audio packet
   timestamp in the finished mp4 and fails the build if there is any gap. A
   good build prints `audio timeline continuous: N packets, no gaps`.
8. **Subtitles** are timed from the finished scene clips by
   `make_subtitles.py`, so they cannot drift either.

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Transactional Outbox with Debezium | Title card and the definition |
| 2 | The Scenario | Every saved order announced, nothing else, each order's events in order |
| 3 | Two Writes, One Crash | Act one: both halves of the dual write failing |
| 4 | Postgres's Words | The write-ahead log, `wal_level=logical`, the replication slot, through a building's journal |
| 5 | Debezium's Words | Change data capture, the outbox event router, the offset, the embedded engine |
| 6 | One Transaction, And Debezium Sends | Act two: 3 events for 3 commits, 0 for the rolled-back ORD-4 |
| 7 | The Log, Not The Table | Act three, the headline: outbox rows 0, events in Kafka 3 |
| 8 | Where Each Piece Lives | One commit, the log, Debezium, Kafka, and the position written down after |
| 9 | Debezium Is Down | Act four: the slot keeps the log, limit -1, and all 3 are sent on restart |
| 10 | The Pattern In One Transaction | The two inserts and the one commit, with no Kafka code |
| 11 | Sent, But Not Written Down | Act five: 4 events for 2 orders, the same ids |
| 12 | Order Per Key, And The Bill | Act six: partitions by key, and what it costs |
| 13 | What The Simulation Left Out | The contrast with the plain-Java version |
| 14 | The Verdict | |
| 15 | What Is Real Here | Postgres 18.6, Kafka 4.3.1 and Debezium 3.6.3.Final; when this is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 docs/make_narration.py --force transactional-outbox-with-debezium`
from the `gradle-java` directory, then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term Postgres, Debezium and Kafka introduce before using the tool's name for
it, and never points at a picture the listener cannot see.

## Publishing Notes

Upload `transactional-outbox-with-debezium-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
