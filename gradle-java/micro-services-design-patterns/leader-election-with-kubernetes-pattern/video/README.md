# Leader Election with Kubernetes Pattern — Teaching Video

A narrated, slide-based video that teaches Leader Election on a real Kubernetes
API server — who holds the lease, who decides it has run out, and what a leader
that froze can still do after it has lost it — and argues for when not to use
it, using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `leader-election-with-kubernetes-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `leader-election-with-kubernetes-pattern-explained.m4a` | Audio-only version. |
| `leader-election-with-kubernetes-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Not the thumbnail. |

None of these is committed except `poster.png`; the script below rebuilds them.

## Rebuilding

```bash
./build_video.sh
```

It runs five steps: render one slide per scene with `make_slides.py`, write each
scene's narration to a text file, speak it and join it to its slide, join the
scenes into one video, and finally level the sound, add the audio-only file,
the poster and the subtitles.

### The audio pipeline

Everything below is in `build_video.sh` itself, with a comment beside each
choice.

- **Voice.** macOS `say`, voice `Samantha` (female, US English), at 145 words
  per minute — the pace educational videos settle on. Both can be changed with
  the `VOICE` and `RATE` environment variables.
- **Clean-up, per scene.** The voice comes out at 22 kHz. Each scene's speech is
  upsampled to 48 kHz with a long resampling filter so the upsampling adds no
  grit, passed through a high-pass filter at 75 Hz to drop rumble, and given a
  small lift around 3 kHz, where consonants live. There is deliberately no
  denoiser: synthesised speech has almost no noise to remove, and a denoiser
  ends up removing parts of the voice instead, which makes it sound under water.
- **A beat of silence.** Each scene ends with 0.9 seconds of silence so slides
  do not snap past.
- **Continuity.** Each scene's audio is padded to a whole number of video
  frames, so sound and picture agree at every join and cannot drift apart over
  sixteen scenes. The scenes' audio is joined as uncompressed sound first and
  encoded to AAC once, at the end, because separately encoded AAC clips each
  carry a little lead-in that turns into a click at every join. At the very
  end the script reads every audio packet of the finished video and checks that
  each one starts exactly where the one before it ended. A good build prints
  `audio timeline continuous: N packets, no gaps`. If that line is missing, or
  reports a gap, the build failed even though an mp4 exists.
- **Loudness, once, over the whole video.** Levelling is not done per scene:
  done that way, each scene is measured on its own and a quiet scene is pushed
  up to match a loud one, and the level jumps at every join. Instead the whole
  narration is measured first, and the measured figures are handed back to
  ffmpeg's `loudnorm` filter as one constant gain, to −16 LUFS integrated,
  −1.5 dB true peak — the level YouTube plays at. A single constant gain cannot
  pump between quiet and loud lines.
- **Encode.** AAC at 192 kbit/s, 48 kHz stereo. The opening frame is fixed so
  players show the poster at 0:00 rather than black.

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and
  `matplotlib`. On a Mac where the first `python3` on the `PATH` lacks them,
  `/usr/bin/python3` usually has them.

The video itself needs no cluster, no container runtime and no kind; only the
demo does.

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Leader Election with Kubernetes | Title card and the definition |
| 2 | The Scenario | Three copies, one nightly sales report |
| 3 | Three Copies, Nobody In Charge | Act one |
| 4 | Kubernetes' Words | Cluster, API server, Lease, holder, renewal, version, 409 Conflict, through a staff-room notice board |
| 5 | One Holds The Lease | Act two, and the refused write |
| 6 | The Elector's Settings | Fabric8's LeaderElector: four settings, three callbacks |
| 7 | The Leader Stops | Act three: a clean stop, then a kill |
| 8 | Who Reads The Clock | Three processes, one record, and where expiry is decided |
| 9 | Two Who Think They Lead | Act four: the frozen leader |
| 10 | The Lease's Own Record | The proof, from the lease's holder and renewal time |
| 11 | Fencing | Act five: the token |
| 12 | The Bill | Act six: the loser never rejoins, and the costs |
| 13 | What The Simulation Left Out | The contrast with the plain-Java project |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | Kubernetes 1.37.0 in kind, Fabric8 8.0.0, and when a lease is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 docs/make_narration.py --force leader-election-with-kubernetes` from
the `gradle-java` directory to refresh `narration.md`, then re-run
`./build_video.sh`.

Every narration line speaks its counts and outcomes in words, explains each
term Kubernetes introduces before using its name for it, and never points at a
picture the listener cannot see. Every number is the output of
`./gradlew run`.

## Publishing Notes

Upload `leader-election-with-kubernetes-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
