# Cache-Aside with Redis Pattern — Teaching Video

A narrated, slide-based video that teaches Cache-Aside on a real Redis server —
a cache every shop process can see, entries removed on Redis's own clock, the
plain write that switches that clock off, and a stampede nobody arranged — and
argues for when not to use it, using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `cache-aside-with-redis-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `cache-aside-with-redis-pattern-explained.m4a` | Audio-only version. |
| `cache-aside-with-redis-pattern-explained.srt` | Subtitles, from `make_subtitles.py`. |
| `poster.png` | The video's opening frame, also used as the thumbnail. |

The mp4, m4a and srt are not committed; `poster.png` is.

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute — the pace educational YouTube settles on.

## Rebuilding

```bash
./build_video.sh
python3 make_subtitles.py
```

A build takes eight to ten minutes. It needs no container runtime; only the
demo does.

### How the audio is made

Everything below happens inside `build_video.sh`; nothing outside this
directory is read.

1. **Narration.** Each scene's text from `scenes.py` is spoken by macOS `say`
   with the `Samantha` voice at 145 words per minute. `[[slnc 250]]` in the
   text is a pause of 250 milliseconds.
2. **Clean-up, per scene.** Each clip is resampled to 48 kHz with a long
   filter, passed through a high-pass filter at 75 Hz to drop rumble, and given
   a small lift around 3 kHz, where consonants live. There is deliberately no
   denoiser: synthesised speech has no real noise floor, and a spectral
   denoiser subtracts parts of the voice instead, leaving it warbling.
3. **Lossless joins.** Each scene's narration is kept as WAV, and the whole
   narration is encoded to AAC exactly once. Encoding each scene separately
   would put a few milliseconds of encoder padding at every join, which is an
   audible click.
4. **Levelling, once, in two passes.** `loudnorm` to −16 LUFS integrated, −1.5
   dB true peak, loudness range 11, is run over the whole assembled narration:
   the first pass measures, the second applies the measured figures. Run per
   scene, it would push quiet scenes up to match loud ones and the level would
   step at each cut.
5. **Continuity check.** The script reads every audio packet's timestamp in
   the finished file and prints `audio timeline continuous: N packets, no
   gaps`. If that line is missing or reports a gap, the build failed even if an
   mp4 exists.

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Cache-Aside with Redis | Title card and the definition |
| 2 | The Scenario | Prices in a database, a shop in more than one process |
| 3 | No Cache | Act one |
| 4 | Redis's Words | Redis, key and value, through a kitchen whiteboard |
| 5 | Look Aside, In Redis | Act two |
| 6 | Another Process Can See It | Act three: a second Java process and redis-cli |
| 7 | Where The Price Lives | Two shops, one Redis, one database |
| 8 | Real Expiry | Act four: time to live, removed on Redis's clock |
| 9 | A Plain Write | Act four, continued: a plain SET erases the expiry |
| 10 | One Argument | The two writes side by side |
| 11 | A Real Stampede | Act five: fifty requests, and a lock kept in Redis |
| 12 | The Bill | Act six: cold start, no size limit, text, one more system |
| 13 | What The Simulation Left Out | The contrast with the plain-Java twin |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | Redis 8.10.2 in a container the demo owns, and when a cache is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, regenerate `narration.md` with the
course's narration generator, then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term Redis introduces before using Redis's name for it, and never points at a
picture the listener cannot see. Every figure is the output of `./gradlew run`.

## Publishing Notes

Upload `cache-aside-with-redis-pattern-explained.mp4`, with the project's
thumbnail and the `.srt` as the captions. Title, description, chapters and tags
live in the project's `docs/youtube.md`.

Suggested description:

> Cache-Aside pattern in Java, explained with a real Redis cache server. In
> our online store every product page needs a price that lives in the
> database, so the shop asks the cache first, and on a miss reads the
> database and leaves a copy in the cache on the way back. We hear a second
> shop process find the cache already filled, a price removed by Redis on
> its own clock, one ordinary write that makes an old price last forever,
> and fifty requests stampede the database with nobody arranging it. The
> shop fills the cache, every shop sees what it filled, and an entry only
> expires if every write remembers to say so.
