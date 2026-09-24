# Idempotent Consumer with Kafka Pattern — Teaching Video

A narrated, slide-based video that teaches the Idempotent Consumer pattern on a
real Kafka broker and a real Postgres database — why Kafka hands the same order
out again, why a list of ids in memory never sees the repeat, and how one
database transaction and one primary key keep it to one confirmation email,
even when two copies of the service hold the same order at once — using this
project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `idempotent-consumer-with-kafka-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `idempotent-consumer-with-kafka-pattern-explained.m4a` | Audio-only version. |
| `idempotent-consumer-with-kafka-pattern-explained.srt` | Subtitles. |
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
| 1 | Idempotent Consumer with Kafka | Title card and the definition |
| 2 | The Scenario | One email per order, from several copies that restart |
| 3 | Kafka's Words | Topic, offset, consumer group, committing the offset, through a notebook and a bookmark |
| 4 | Kafka Sends It Again | Act one: 6 deliveries and 6 emails for 3 orders |
| 5 | A List Of Ids In Memory | Act two, the headline: the repeat lands on a copy with an empty list |
| 6 | Postgres's Words | Transaction, primary key, lock |
| 7 | A Table, One Transaction | Act three: 6 deliveries, 3 emails |
| 8 | Where The Memory Lives | The id and the email together, the bookmark after |
| 9 | Where The Crash Lands | Act four: a second step against one transaction |
| 10 | The Pattern In Two Statements | `on conflict do nothing`, then the offset commit |
| 11 | Two Copies At Once | Act five: the patience limit, the lock, the refused commit |
| 12 | The Bill | Act six: the cleanup window against the topic's retention |
| 13 | What The Simulation Left Out | The contrast with the plain-Java version |
| 14 | The Verdict | |
| 15 | What Is Real Here | Kafka 4.3.1 and Postgres 18.6 in containers the demo owns; when this is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 docs/make_narration.py --force idempotent-consumer-with-kafka`
from the `gradle-java` directory, then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term Kafka and Postgres introduce before using the tool's name for it, and
never points at a picture the listener cannot see.

## Publishing Notes

Upload `idempotent-consumer-with-kafka-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
