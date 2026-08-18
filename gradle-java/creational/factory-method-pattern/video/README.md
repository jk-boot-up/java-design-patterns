# Factory Method Pattern — Teaching Video

A narrated, slide-based video that teaches the Factory Method pattern using
this project's code. Aimed at beginners with no prior design-pattern
knowledge.

## Output Files

| File | What it is |
| --- | --- |
| `factory-method-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `factory-method-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `factory-method-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |

**Runtime:** approximately 7 minutes.
**Narration:** female voice (macOS `Samantha`, US English).

## Source Files

| File | Purpose |
| --- | --- |
| `narration.md` | The full spoken script, scene by scene — read this to review or edit the wording. |
| `scenes.py` | Slide content *and* narration text, kept together so they cannot drift apart. |
| `make_slides.py` | Renders one 1920×1080 PNG per scene. |
| `make_subtitles.py` | Generates the SRT, timed from the encoded scene clips. |
| `build_video.sh` | The whole pipeline: slides → narration → per-scene clips → final video → subtitles. |
| `build/` | Generated slide images (regenerated on every build). |

## Rebuilding

```bash
./build_video.sh
```

The script will:

1. render the slides,
2. narrate each scene with the `say` command,
3. pair every slide with its narration into a clip,
4. concatenate the clips and export the audio-only version,
5. generate the SRT subtitles, then clean up the intermediates.

Set `KEEP_INTERMEDIATE=1` to retain the per-scene narration and clips for
inspection.

### Options

Both are environment variables:

```bash
VOICE=Ava RATE=160 ./build_video.sh
```

| Variable | Default | Meaning |
| --- | --- | --- |
| `VOICE` | `Samantha` | Any voice from `say -v '?'` |
| `RATE` | `170` | Speaking rate in words per minute |

### Requirements

- **macOS** — the narration uses the built-in `say` command
- **ffmpeg** — `brew install ffmpeg`
- **Python 3** with `pillow` and `matplotlib`
  (`matplotlib` is used only for its bundled DejaVu fonts)

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Title | What the video will teach |
| 2 | The Scenario | Four delivery tiers, four carriers |
| 3 | The Workflow Is Always the Same | Three shared steps, one that varies |
| 4 | The Problem | One class doing the workflow *and* the choosing |
| 5 | Why That Hurts | Editing working code, tangled branches, closed extension |
| 6 | The Factory Method | The GoF definition, then the plain-language one |
| 7 | The Coffee Chain Analogy | How to remember it forever |
| 8 | The Four Roles | Product, products, creator, concrete creators |
| 9 | A Product | `AirCourier` — small and unaware |
| 10 | The Creator | The abstract method, and the `final` workflow |
| 11 | A Concrete Creator | Six lines, and no `switch` anywhere |
| 12 | What You Gain | Open/Closed, shared behaviour, external extension |
| 13 | Running It | The real program output |
| 14 | Wrap Up | When to use it, when not to, and the one sentence to remember |

## Related: the animation's narration

[`../docs/animation.html`](../docs/animation.html) has its own optional
narration, generated separately by
[`../docs/make_animation_audio.sh`](../docs/make_animation_audio.sh) into
`docs/audio/`. It uses the same voice and rate as this video so the two
sound consistent. Those clips are short per-step explanations, not the
video script.

## Editing the Script

Narration lives in `scenes.py`, next to the slide it belongs to. Edit the
`narration` field of a scene, then re-run `./build_video.sh`. Keep
`narration.md` in sync if you change the wording substantially — it is the
human-readable copy used for review.

Note that some words are spelled phonetically for the synthesiser — "sky
link air" rather than "SkyLink Air". Keep that habit, or the narration will
mispronounce them.

## Publishing Notes

The video is encoded to YouTube's recommended settings already (1080p,
H.264, 30 fps, stereo AAC at 48 kHz), so it can be uploaded as-is.

**Upload only `factory-method-pattern-explained.mp4`.** The `.m4a` and the
build scripts have no role on YouTube.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`DeliveryService`. Uploading `factory-method-pattern-explained.srt` gives
exact wording and makes the video searchable.

**During upload** — on the *Video elements* step, choose **Add subtitles**
→ **Upload file** → **With timing**, pick the `.srt`, then **Save**.

**After publishing** — YouTube Studio → **Subtitles** → select the video →
next to your language click **Add** → **Upload file** → **With timing** →
choose the `.srt` → **Publish**.

Set the video language (Details → *Show more* → Video language) to English
first, or the subtitle option may not appear.

Two further things that affect how well it plays for viewers:

- **Wait for HD processing.** YouTube serves a low-resolution version
  first; 1080p can take several extra minutes to appear. Code slides are
  unreadable at 360p, so do not share the link until 1080p is available in
  the quality menu.
- **Set a thumbnail.** Auto-picked frames are often mid-transition.
  `../docs/images/class-diagram.png` or the title slide works well.

Suggested description:

> Learn the Factory Method pattern in Java 21 by building an online store's
> delivery tiers. We start with the problem — a shipping method with an
> if/else chain buried in the middle of it — and end with an abstract
> creator whose subclasses answer one question each, and no `switch`
> anywhere. We also cover, honestly, when the pattern is more machinery
> than the job needs. No prior design-pattern knowledge needed. Full source
> code and written notes are in the repository.
