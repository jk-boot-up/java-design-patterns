# Strangler Fig with NGINX Pattern — Teaching Video

A narrated, slide-based video that teaches Strangler Fig on a real NGINX —
one route moved at a time with a reload while the old shop serves the rest, a
request in progress finishing on the old configuration, an old rule that
quietly cancels a move, one slash that rewrites a path, a new service that is
down on its own, and a cookie only the old shop understands — and argues for
when not to use it, using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `strangler-fig-with-nginx-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `strangler-fig-with-nginx-pattern-explained.m4a` | Audio-only version. |
| `strangler-fig-with-nginx-pattern-explained.srt` | Subtitles, from `make_subtitles.py`. |
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
| 1 | Strangler Fig with NGINX | Title card and the definition |
| 2 | The Scenario | The old shop, the new service, no cutover weekend |
| 3 | The Big Bang | Act one |
| 4 | NGINX's Words | Reverse proxy, location, prefix, reload, through an office receptionist |
| 5 | One Route At A Time | Act two: a move, a reload, a request in progress |
| 6 | A Reload Has A Shape | Main process, workers, and the moment both take connections |
| 7 | Where Each Request Goes | One address, the new service, the old shop |
| 8 | A Regular Expression Wins | Act three |
| 9 | How NGINX Picks A Location | The matching order, and `^~` |
| 10 | One Slash | Act four |
| 11 | The New Service Goes Down | Act five: 502, and a rollback |
| 12 | The Bill | Act six: the cookie, and three things to run |
| 13 | What The Simulation Left Out | The contrast with the plain-Java twin |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | NGINX 1.31.6 in a container the demo owns, and when this is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, regenerate `narration.md` with the
course's narration generator, then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term NGINX introduces before using NGINX's name for it, and never points at a
picture the listener cannot see. Every figure is the output of `./gradlew run`.

## Publishing Notes

Upload `strangler-fig-with-nginx-pattern-explained.mp4`, with the project's
thumbnail and the `.srt` as the captions. Title, description, chapters and tags
live in the project's `docs/youtube.md`.

Suggested description:

> Learn the Strangler Fig pattern in Java with a real NGINX web server as
> the front door. You replace an old system without switching it off,
> growing the new one beside it one piece at a time, while the front door
> decides which system answers each route. In our online store, prices move
> to a new service while the old shop keeps the basket, checkout and past
> orders. We move a route with a reload that restarts nothing, then hear the
> traps: an older regular-expression rule that quietly cancels the move, one
> slash that changes what the new service is asked for, a new service that
> goes down, and a cookie only the old shop understands.
