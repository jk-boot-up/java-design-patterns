# Event Sourcing with EventStoreDB Pattern — Teaching Video

A narrated, slide-based video that teaches Event Sourcing on a real KurrentDB
server, the database once called EventStoreDB. It covers a stream read back
from the start, two checkouts spending the same points with and without the
expected revision, a retry the server recognises, a catch-up subscription, and
a delete that hides rather than erases. It also argues for when not to use it,
using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `event-sourcing-with-eventstoredb-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `event-sourcing-with-eventstoredb-pattern-explained.m4a` | Audio-only version. |
| `event-sourcing-with-eventstoredb-pattern-explained.srt` | Subtitles, from `make_subtitles.py`. |
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
| 1 | Event Sourcing with EventStoreDB | Title card, the rename, and the definition |
| 2 | The Scenario | Loyalty points, no stored balance, two places to pay |
| 3 | KurrentDB's Words | The rename; stream, revision and append, through numbered ledgers |
| 4 | A Real Log, Read Back | Act one |
| 5 | Two Checkouts, No Check | Act two: both accepted, balance -60 |
| 6 | The Expected Revision | Act three: one accepted, one refused |
| 7 | One Number Decides | Two checkouts, one stream, one revision |
| 8 | One Argument | `StreamState.any()` against `streamRevision(3)`, and which is the default |
| 9 | A Retry It Recognises | Act four: event ids |
| 10 | A Screen That Catches Up | Act five: a catch-up subscription and a read model |
| 11 | The Bill: Deleting A Stream | Act six: not found, still in the whole log, numbering carries on |
| 12 | What Else It Costs | Erasure, the default, insecure mode, one more database |
| 13 | What The Simulation Left Out | The contrast with the plain-Java twin |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | KurrentDB 26.1.2 in a container the demo owns, and when this is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, regenerate `narration.md` with the
course's narration generator, then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term KurrentDB introduces before using KurrentDB's name for it, and never points at a
picture the listener cannot see. Every figure is the output of `./gradlew run`.

## Publishing Notes

Upload `event-sourcing-with-eventstoredb-pattern-explained.mp4`, with the project's
thumbnail and the `.srt` as the captions. Title, description, chapters and tags
live in the project's `docs/youtube.md`.
