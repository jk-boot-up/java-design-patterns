# Layered Architecture Pattern — Teaching Video

A narrated, slide-based video that teaches Layered Architecture using this
project's code. This is the category's reference project, so the video also
sets the standard the other four architectures are measured against: how the
architecture test reads and how it fails, and how a forced change is counted
and printed.

## Output Files

| File | What it is |
| --- | --- |
| `layered-architecture-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `layered-architecture-pattern-explained.m4a` | Audio-only version, for listening on the move or for revision. |
| `layered-architecture-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. Upload alongside the video for accurate captions. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail — see the publishing notes below. |

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

The `.mp4`, `.m4a` and `.srt` are build output and are not committed — run
`./build_video.sh` to produce them. `poster.png` *is* committed, so the title
card is available without a build.

## Source Files

| File | Purpose |
| --- | --- |
| `narration.md` | The full spoken script, scene by scene — read this to review the wording. It is generated from `scenes.py` by `../../docs/make_narration.py`, so edit the scenes, not the script. |
| `scenes.py` | Slide content *and* narration text, kept together so they cannot drift apart. |
| `make_slides.py` | Renders one 1920×1080 PNG per scene. |
| `make_subtitles.py` | Generates the SRT, timed from the encoded scene clips. |
| `build_video.sh` | The whole pipeline: slides → narration → per-scene clips → final video → subtitles. |
| `build/` | Generated slide images (regenerated on every build). |

## Rebuilding

```bash
./build_video.sh
```

The pipeline, the audio chain and the reasons behind both — no denoiser, two-pass
loudness, lossless per-scene WAV joined to a single AAC encode, `+faststart` and
a dropped edit list — are identical across every project in this repository and
documented at length in the platform category's
[`externalised-configuration-pattern/video/README.md`](../../platform-design-patterns/externalised-configuration-pattern/video/README.md).
Nothing about this project changes that pipeline; only the scenes and the slide
renderer differ.

Set `KEEP_INTERMEDIATE=1` to retain the per-scene narration and clips for
inspection.

### Options

```bash
VOICE=Ava RATE=155 ./build_video.sh
```

| Variable | Default | Meaning |
| --- | --- | --- |
| `VOICE` | `Samantha` | Any voice from `say -v '?'` |
| `RATE` | `145` | Speaking rate in words per minute |

### Requirements

- **macOS** — the narration uses the built-in `say` command
- **ffmpeg** — `brew install ffmpeg`
- **Python 3** with `pillow` and `matplotlib`
  (`matplotlib` is used only for its bundled DejaVu fonts)

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Layered Architecture | Title card, author credit, the plain-language definition of a layered architecture, and then the same idea in the online store |
| 2 | The Scenario | Ada's £382.50 order — the same feature every project in this category places |
| 3 | Version One — No Layers At All | `EverythingOrderService`, and why its pricing cannot be tested without its storage |
| 4 | Four Layers, Stacked | Presentation, application, domain, infrastructure — what each one's job is and what it must not know |
| 5 | The One Call That Ruins Them | `OrderHistoryScreen`'s shortcut, and the line that names this project's whole lesson: nothing in the build objected |
| 6 | Why This Keeps Happening | Diagrams and adjectives versus a test that can fail — the category's anti-vagueness argument |
| 7 | The Rule, Written Where A Build Can Read It | `ArchitectureTest`'s ArchUnit rule, read almost as English |
| 8 | Watching It Go Red | The failure message naming `OrderHistoryScreen` and `InMemoryOrderTable` by name |
| 9 | The Forced Change | Swapping the storage layer, counted: 1 file added, 1 modified, 1 line, 16 of 17 classes never opened |
| 10 | And The One That Took The Shortcut | Why `OrderHistoryScreen` alone fails to compile after the swap |
| 11 | What This Project Does Not Fix | The application layer still names infrastructure by package — the one thing Hexagonal Architecture changes next |
| 12 | An Order That Is Not Obvious | Why the card is charged before anything is written down |
| 13 | The Bill | Indirection, pass-through layers, and the bottom layer still being the database |
| 14 | When This Is Too Much | The size of application at which four layers stop paying for themselves |
| 15 | Thanks for Watching | The widen-the-architecture-test exercise, like, subscribe, and where the source lives |

The first and last scenes carry the branding: scene 1 credits the author out
loud, scene 15 asks for the thumbs up and the subscribe. Scene 11 is a
`diagram` slide laid out by hand in `make_slides.py`; scenes 5, 8, 9 and 10
are `console` slides showing what the demo actually prints. If you change
`PlaceAnOrderDemo`, re-check all four against its real output.

Scene 15 deliberately does not name whichever pattern comes next. Publishing
order on YouTube is not the order these projects were built in, and a
rendered video cannot be corrected without re-uploading it.

## Related: the animation's narration

[`../docs/animation.html`](../docs/animation.html) has its own optional
narration, generated separately by
[`../docs/make_animation_audio.sh`](../docs/make_animation_audio.sh) into
`docs/audio/`. It uses the same voice and rate as this video so the two
sound consistent. Those clips are short per-step explanations, not the
video script.

## Editing the Script

Narration lives in `scenes.py`, next to the slide it belongs to. Edit the
`narration` field of a scene, re-run
`python3 ../../docs/make_narration.py --force layered-architecture` to
refresh `narration.md`, then re-run `./build_video.sh`.
`[[slnc NNN]]` markers insert a pause of NNN milliseconds; they are
instructions to `say`, not words, and `make_subtitles.py` strips them.

This is the hardest audio-only category in the course: architecture is
normally taught by pointing at a diagram, and a listener has no diagram. Every
narration line describes structure as rules and directions in words —
"the checkout names the application layer, and nothing else" — and the phrase
"as you can see" does not appear anywhere in `scenes.py`. If a scene needs the
picture to make sense, the scene is rewritten rather than the rule relaxed.

## Publishing Notes

The video is encoded to YouTube's recommended settings already. Upload
`layered-architecture-pattern-explained.mp4`, with `../docs/thumbnail.png` as
the thumbnail and the `.srt` as the captions. The title, description, chapters
and tags to paste at upload time live in [`../docs/youtube.md`](../docs/youtube.md).

`poster.png` is the video's opening frame, not the thumbnail: it is composed
for a full screen, whereas `thumbnail.png` is drawn at 1280×720 with only the
pattern name, one promise and one line of code, so it survives being shrunk to
search-result size.

Wait for HD processing before sharing the link — code and console slides are
unreadable at 360p — and set the custom thumbnail under **Details** →
**Thumbnail** rather than letting YouTube auto-pick a frame.
