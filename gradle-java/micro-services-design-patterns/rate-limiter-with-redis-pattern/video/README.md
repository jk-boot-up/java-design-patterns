# Rate Limiter with Redis Pattern — Teaching Video

A narrated, slide-based video that teaches Rate Limiter on a real Redis server
with Bucket4j. It shows why a bucket in each server leaks, how one bucket in
Redis holds across three and six servers and ninety searches at the same instant,
why a plain number read and written in two steps spends the last token twice,
and how one server with a fast clock refills the bucket for everyone. It also
argues for when not to use it. The examples come from this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `rate-limiter-with-redis-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `rate-limiter-with-redis-pattern-explained.m4a` | Audio-only version. |
| `rate-limiter-with-redis-pattern-explained.srt` | Subtitles. |
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
| 1 | Rate Limiter with Redis | Title card and the definition |
| 2 | The Scenario | Product search, a robot client, three servers behind a load balancer |
| 3 | A Bucket In Each Server | Act one: 30 allowed, not 10; 60 on six servers |
| 4 | The Tools' Words | Redis, key, time to live, Bucket4j, proxy manager, compare-and-swap, client clock, through a shared whiteboard |
| 5 | One Bucket In Redis | Act two: 10 allowed on three servers and on six; a restart does not refill |
| 6 | Where The Bucket Lives | Redis keeps the bucket, the servers do the sums |
| 7 | All At The Same Moment | Act three: 90 searches on 90 threads, exactly 10 allowed |
| 8 | Why Not Just A Number? | Act four: the lost update, and the conditional write |
| 9 | The Whole Pattern, In One Builder | The Bucket4j builder chain on each server |
| 10 | Whose Clock? | Act five: a server one hour fast refills the bucket for everyone |
| 11 | The Clocks Must Agree | Why the twin could never show it |
| 12 | The Bill | Act six: a key per client, Redis stopped, a network trip per search |
| 13 | What The Simulation Left Out | The contrast with the hand-built twin |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | Redis 8.10.2 in a container the demo owns, and when a shared store is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 docs/make_narration.py --force rate-limiter-with-redis` from the
`gradle-java` directory, then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term Redis and Bucket4j introduce before using the tool's name for it, and never
points at a picture the listener cannot see. Every number matches the output of
`./gradlew run`.

## Publishing Notes

Upload `rate-limiter-with-redis-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Learn the Rate Limiter pattern in Java with a real Redis server and the
> Bucket4j library. Each caller gets a bucket of tokens, every request
> spends one, and an empty bucket means a refusal until it refills. In our
> online store a price-comparison robot hammers the product search, and ten
> searches an hour must mean ten however many copies of the search are
> running. We watch the limit leak when each server keeps its own bucket,
> hold when the bucket moves into Redis, survive ninety searches at the same
> instant, and break when one server's clock disagrees.
