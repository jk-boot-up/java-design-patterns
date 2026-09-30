# Externalised Configuration with Spring Cloud Config Pattern — Teaching Video

A narrated, slide-based video that teaches Externalised Configuration with a
real Spring Cloud Config Server — a setting served over HTTP from a git
repository, a commit that is served but not yet in force, a refresh with no
restart, the banner the refresh never reaches, and what the shop does when the
server is gone — and argues for when not to use it, using this project's
online store.

## Output Files

| File | What it is |
| --- | --- |
| `externalised-configuration-with-spring-cloud-config-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `externalised-configuration-with-spring-cloud-config-pattern-explained.m4a` | Audio-only version. |
| `externalised-configuration-with-spring-cloud-config-pattern-explained.srt` | Subtitles, from `make_subtitles.py`. |
| `poster.png` | The video's opening frame, also used as the thumbnail. |

The mp4, m4a and srt are not committed; `poster.png` is.

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute — the pace educational YouTube settles on.

## Rebuilding

```bash
./build_video.sh
python3 make_subtitles.py
```

A build takes eight to ten minutes. Neither the build nor the demo needs a container
runtime.

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
| 1 | Externalised Configuration with Spring Cloud Config | Title card and the definition |
| 2 | The Scenario | Free delivery over £50.00, and marketing's weekend |
| 3 | Spring Cloud Config's Words | Git, config server, refresh, through a bakery head office |
| 4 | Served Over HTTP | Act one |
| 5 | Committed, Not In Force | Act two |
| 6 | The Refresh | Act three: POST /actuator/refresh |
| 7 | Where The Value Lives | Git, the server, the shop |
| 8 | Two Thresholds, One Shop | Act four: the banner the refresh missed |
| 9 | Two Ways To Read One Value | @RefreshScope beside a constructor @Value |
| 10 | A Value Nobody Checked | Act five: -1, five failed quotes, git's log |
| 11 | The Server Stops | Act six: running shop, fail fast, optional |
| 12 | The Bill | Four decisions Spring leaves to you |
| 13 | What The Simulation Left Out | The contrast with the plain-Java twin |
| 14 | The Verdict |  |
| 15 | What Is Real, And When Not | Config Server 5.0.5 as a second Java process, and when it is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, regenerate `narration.md` with the
course's narration generator, then re-run `./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term Spring introduces before using Spring's name for it, and never points at a
picture the listener cannot see. Every figure is the output of `./gradlew run`.

## Publishing Notes

Upload `externalised-configuration-with-spring-cloud-config-pattern-explained.mp4`, with the project's
thumbnail and the `.srt` as the captions. Title, description, chapters and tags
live in the project's `docs/youtube.md`.

Suggested description:

> Externalised Configuration pattern in Java: a value that changes on somebody
> else's calendar should live outside the program and be read while it runs,
> so changing it needs no rebuild and no release. Explained with a real Spring
> Cloud Config server. In our online store, marketing decides the
> free-delivery threshold of fifty pounds and wants thirty-five for the
> weekend. We serve the value over HTTP, watch a change that is committed but
> not yet in force, refresh it with no restart, and find one running shop
> believing two different numbers at the same time. We also hear what happens
> to a value nobody checked, and when the server stops.
