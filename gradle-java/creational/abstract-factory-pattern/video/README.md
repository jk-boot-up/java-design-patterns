# Abstract Factory Pattern — Teaching Video

A narrated, slide-based video that teaches the Abstract Factory pattern using
this project's code. Aimed at beginners with no prior design-pattern
knowledge.

## Output Files

| File | What it is |
| --- | --- |
| `abstract-factory-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `abstract-factory-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `abstract-factory-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |

**Runtime:** approximately 9 minutes.
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
| 2 | The Scenario | Three markets, three sets of rules |
| 3 | Nine Classes, Three Legal Combinations | The 3×3 grid, and what a "family" means |
| 4 | The Problem | Three branches on the same string |
| 5 | Why That Hurts | Silent mismatches, three-way edits, a wrong invoice |
| 6 | The Abstract Factory | The GoF definition, then the plain-language one |
| 7 | The Set Menu | How to remember it forever |
| 8 | The Roles | Client, abstract factory, concrete factories, products |
| 9 | The Abstract Factory | The interface — and the parameter that is missing |
| 10 | A Concrete Factory | Three `new` calls, and zero validation |
| 11 | The Client | Four lines of setup, then no country anywhere |
| 12 | What You Gain | Impossible mismatches, additive markets, testable families |
| 13 | The Honest Cost | Rows are cheap, columns are expensive |
| 14 | Running It | The real program output, including the rejection |
| 15 | Wrap Up | When to use it, when not to, and the one sentence to remember |

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

Note that some words are spelled phonetically for the synthesiser — "V A T"
rather than "VAT", "à la carte" spoken as written. Keep that habit, or the
narration will mispronounce them.

## Publishing Notes

The video is encoded to YouTube's recommended settings already (1080p,
H.264, 30 fps, stereo AAC at 48 kHz), so it can be uploaded as-is.

**Upload only `abstract-factory-pattern-explained.mp4`.** The `.m4a` and the
build scripts have no role on YouTube.

### Adding the subtitles

YouTube auto-generates captions, but they mis-hear class names like
`MarketFactory`. Uploading `abstract-factory-pattern-explained.srt` gives
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
- **Set a thumbnail.** Auto-picked frames are often mid-transition. The
  3×3 grid slide (`build/03-grid.png` after a rebuild),
  `../docs/images/families.png` or the title slide all work well.

Suggested description:

> Learn the Abstract Factory pattern in Java 21 by building an online
> store's regional checkout. We start with the problem — three separate
> if/else chains that must all agree with each other, and silently produce a
> wrong invoice when they don't — and end with a design where a mismatched
> family is not caught but impossible. We also cover, honestly, why adding a
> new product kind is the expensive direction, and when the pattern is more
> machinery than the job needs. No prior design-pattern knowledge needed.
> Full source code and written notes are in the repository.
