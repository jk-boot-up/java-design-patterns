# Teaching Video Specification

This is the specification the video in [`../video/`](../video/) is built to. It
describes *what the video must be*, not how to run the build — for the build
steps see [`../video/README.md`](../video/README.md).

It is written to be portable. Every other teaching video in these repositories
is a port of this one, so if you are building a new project's video, this file
is the contract to satisfy.

---

## 1. What gets produced

One build produces exactly four artefacts, all in `video/`:

| File | Format | Purpose |
| --- | --- | --- |
| `<project>-explained.mp4` | 1920×1080, H.264 High, 30 fps, yuv420p, AAC-LC 192 kbps stereo @ 48 kHz, `+faststart` | The video. Uploaded to YouTube as-is. |
| `<project>-explained.m4a` | AAC 192 kbps stereo | Audio-only, for revision on the move. |
| `<project>-explained.srt` | SubRip | Captions. Uploaded alongside the video. |
| `poster.png` | 1920×1080 PNG | The opening frame, used as the custom thumbnail. |

None of the four are committed. They are build output; the scripts that produce
them are what lives in git. Every project's `.gitignore` therefore carries:

```
/video/*.mp4
/video/*.m4a
/video/*.srt
/video/poster.png
/video/build/
```

**Target runtime: 10–13 minutes.** Long enough to teach the idea from nothing,
short enough that a student finishes it. That works out at roughly 15–19
scenes.

---

## 2. Source layout

Six files, all in `video/`, and no others:

| File | Responsibility |
| --- | --- |
| `scenes.py` | The single source of truth: slide content *and* the narration spoken over it, in one `SCENES` list. |
| `make_slides.py` | Renders one 1920×1080 PNG per scene into `build/`. |
| `make_subtitles.py` | Writes the SRT, timed from the encoded scene clips. |
| `build_video.sh` | The whole pipeline, one command, no arguments. |
| `narration.md` | The full spoken script, generated from `scenes.py`, for human review. |
| `README.md` | How to rebuild, what the options are, and how to publish. |

The rule behind this layout is that **slide and narration never live apart**. A
scene is a `dict` holding `key`, `kind`, `title`, `body` and `narration`
together, so it is impossible to reword the narration and forget the slide, or
the other way round.

---

## 3. The pipeline

`build_video.sh` runs five stages and nothing else:

1. **Slides.** `make_slides.py` renders `build/<key>.png` per scene.
2. **Narration text.** Each scene's `narration` string is written to
   `build/<key>.txt`.
3. **Speech and per-scene clips.** macOS `say` speaks each `.txt` to AIFF; the
   AIFF is cleaned (§6), padded with a 0.9 s tail, and married to its PNG as
   `build/scene-<key>.mp4`.
4. **Concatenation.** The concat demuxer joins the clips with `-c copy`, then a
   second lossless remux applies the two opening-frame fixes (§7). The audio
   track and `poster.png` are lifted out here.
5. **Subtitles.** `make_subtitles.py` measures the encoded clips and writes the
   SRT.

Intermediates are deleted afterwards unless `KEEP_INTERMEDIATE=1` is set. The
slide PNGs are kept.

**Requirements:** macOS (for `say`), `ffmpeg`, and Python 3 with `pillow` and
`matplotlib`. `matplotlib` is a dependency only for the DejaVu TTFs it bundles,
which is what makes the slides render identically on any machine without a
font install.

---

## 4. The slide system

Canvas is 1920×1080 throughout. Background `#0F172A`, with an accent rule
across the top eight pixels.

### Palette

| Role | Hex | Used for |
| --- | --- | --- |
| `BG` | `#0F172A` | Slide background |
| `PANEL` | `#1E293B` | Code and diagram panels |
| `TEXT` | `#E2E8F0` | Body text |
| `MUTED` | `#94A3B8` | Footers, secondary lines |
| `ACCENT` | `#A78BFA` | Top rule, headings, structure |
| `CLIENT` | `#38BDF8` | The caller's side of a diagram; the byline pill |
| `HIDDEN` | `#FBBF24` | What the pattern conceals; the poster eyebrow |
| `PINK` | `#F472B6` | Emphasis and callout notes |
| `RED` | `#F87171` | The wrong way, struck through |
| `GREEN` | `#34D399` | The right way, and finished work |
| `LINE` | `#475569` | Rules and outlines |

Colour carries meaning and must stay consistent: red is always the approach
being rejected, green is always the one being taught.

### Scene kinds

A scene declares a `kind`, and `make_slides.py` dispatches on it. The set is
deliberately small — a new kind should only be added when an existing one
genuinely cannot carry the idea.

| `kind` | Renders |
| --- | --- |
| `poster` | The title card and thumbnail (§5) |
| `outro` | The sign-off card (§5) |
| `title` | Centred statement, for the closing takeaway |
| `bullets` | A list, with `✓`/`✗` lines auto-coloured green/red |
| `quote` | A definition, against a vertical accent bar |
| `code` | A monospaced panel, auto-fitted, with syntax colouring by line prefix |
| `console` | Real terminal output in a darker panel |
| `diagram` | A hand-laid structural drawing for that project |

Two hard rules for `code` and `console` scenes:

- **Code on a slide must match the real source file.** Condensing is allowed —
  dropping Javadoc, eliding a body with `...` — but not paraphrasing. If the
  source says `Node<T> sliceTail = beforeSlice.next;`, the slide does not say
  `sliceTail = beforeSlice.next;`.
- **Console output must be real.** Run the demo, paste what it printed. Never
  invent plausible output.

Text must be legible at 360p, because YouTube serves a low-resolution version
first: body text no smaller than 40 px, and code auto-fitted rather than
allowed to overflow. `title`, `poster` and `outro` carry no page footer; every
other kind shows `<n> / <total>` bottom-left and `<Topic>  ·  Java 21`
bottom-right.

---

## 5. Branding

Every video opens and closes with the same two cards.

**The poster (scene 1)** is the title card and the YouTube thumbnail in one, so
it is designed to survive being shrunk to about 320 px wide in a search result:
a vertical gradient wash, an eyebrow line in amber, the topic set in 120–128 px
across two lines, and one visual comparison — the rejected approach in a red
pill with a strike through it, an arrow, and the taught approach in a green
pill — wrapped in a single outlined box with the tagline, so the tagline reads
as part of the idea rather than as a floating caption.

The author credit sits in a pill at **bottom left**, at (110, 896). That
position is not arbitrary: it aligns with the eyebrow, title and rule above it,
and it stays clear of YouTube's own furniture — the duration badge sits bottom
right, and the watched-progress bar covers the last forty pixels of height.

The narration of scene 1 credits the author out loud: *"This one is written and
presented by Jayasekhar Konduru."*

**The outro (final scene)** is the same gradient reversed, the title, three
outlined buttons reading LIKE / SUBSCRIBE / SHARE, two short lines pointing at
the repository, and the byline pill centred at the foot. Its narration asks for
the like and the subscribe explicitly, and signs off by name.

---

## 6. Narration

**Voice: `Samantha`, US English, female. Rate: 165 wpm.** Both are
`build_video.sh` environment variables (`VOICE`, `RATE`) but the defaults are
the spec; a different voice is for experimenting, not for shipping.

The register is *spoken, not read*. Contractions, short sentences, the odd
aside, and a willingness to say the same thing twice in different words. It
must not sound auto-generated, which in practice means writing sentences a
person would actually say out loud and then reading them back.

Three conventions the script must follow:

- **Pauses are explicit.** `[[slnc NNN]]` inserts NNN milliseconds of silence
  where a person would draw breath — typically 300–500 ms between thoughts.
  These are instructions to `say`, not words, and `make_subtitles.py` strips
  them before writing captions.
- **Maths and symbols are spelled out.** "O of n", not "O(n)". "one and a half
  n", not "~1.5n". "next hop", not "nextHop". The synthesiser mispronounces
  the written forms.
- **No references the video cannot show.** No line numbers, no "as we saw in
  chapter three", no pointing at anything off-screen. The audience is a student
  meeting the topic for the first time.

`narration.md` is regenerated from `scenes.py` whenever the wording changes
substantially. It is the review copy, never the source.

---

## 7. Audio and container correctness

These are the two things that go silently wrong, so both are specified and both
are verified after every build.

### The narration is cleaned before encoding

Every voice macOS ships by default is the compact 22 kHz tier, and resampling
that straight to the 48 kHz the AAC track needs leaves an audible hiss. The
filter chain is:

```
aresample=48000:filter_size=256:cutoff=0.98,
highpass=f=85,
afftdn=nr=14:nf=-45,
equalizer=f=3000:t=q:w=1.2:g=2.5,
lowpass=f=10500,
loudnorm=I=-16:TP=-1.5:LRA=11
```

A long resampler so the upsampling adds no grit; a high-pass below the voice; a
spectral denoise, which is what actually removes the hiss; a small lift at
3 kHz where consonants live; a low-pass hiding the empty band a 22 kHz source
cannot fill; and normalisation to YouTube's −16 LUFS target. Measured against
the unfiltered encode this drops the noise floor by about 15 dB.

An Enhanced or Premium voice samples at 44.1 kHz and would sound better still,
but it is a manual download (**System Settings → Accessibility → Spoken Content
→ System Voice → Manage Voices**). The chain stays regardless.

### The first frame must be the poster

Three settings, all necessary:

| Setting | Why |
| --- | --- |
| `-bf 0` | B-frames save nothing on a static slide and push the video track's first timestamp past the audio's, so players show black at 0:00. |
| `-ignore_editlist 1` on the remux | Drops the edit list created by the AAC encoder's priming delay, which otherwise starts video 21 ms after audio. |
| `-movflags +faststart` | Moves the `moov` atom to the front. Without it the index sits behind twenty-odd megabytes of video and the player has nothing to draw until it has read the lot. |

---

## 8. Subtitles

Cues are timed from the **encoded scene clips**, not from the raw narration
audio. The clips run marginally longer than the speech they contain because of
encoder frame alignment, and timing against the raw audio lets that difference
accumulate into tens of seconds of caption drift by the end.

Each scene's narration is stripped of `[[slnc]]` markers, split at sentence
boundaries into cues of at most **84 characters**, and spread across that
scene's measured duration less a **0.9 s** tail that matches the `apad` in the
build. `make_subtitles.py` therefore has to run while the per-scene clips still
exist, which is why it is stage 5 and not a separate script.

---

## 9. Verification

A build is not finished until it has been measured. Assertions about the output
do not count; these commands do.

```bash
F=<project>-explained.mp4

# Both streams must start at 0.000000
ffprobe -v error -show_entries stream=codec_type,start_time -of csv=p=0 "$F"

# moov must be near the front — expect an offset of 36
head -c 300000 "$F" | grep -abo moov | head -1

# Noise floor should read -inf; peak should sit a few dB below full scale
ffmpeg -v info -i "$F" -af astats -f null - 2>&1 | grep -iE "noise floor|peak level"

# No speech commands may leak into the captions — expect 0
grep -c '\[\[' <project>-explained.srt

# Look at the first and last frames. Actually look at them.
ffmpeg -v error -ss 0      -i "$F" -frames:v 1 build/f0.png    -y
ffmpeg -v error -sseof -2  -i "$F" -frames:v 1 build/flast.png -y
```

Reference figures for this project: 690.10 s runtime, 24,939,131 bytes, 171
cues, both streams at 0.000000, `moov` at 36.

Slides should also be rendered and looked at *before* committing to a
ten-minute encode — `python3 make_slides.py build` on its own is cheap, and
multi-row diagram slides in particular tend to collide in ways only the eye
catches.

---

## 10. Publishing

The encode already matches YouTube's recommended settings, so the mp4 uploads
unchanged. Upload `poster.png` as the custom thumbnail rather than letting
YouTube auto-pick a frame, and upload the `.srt` as captions — the
auto-generated ones mis-hear method names. Set the video language to English
first, or the subtitle option may not appear. Wait for 1080p processing to
finish before sharing the link; code slides are unreadable at 360p.

`video/README.md` carries the click-by-click instructions and a ready-made
video description.

---

## 11. This project's scenes

Nineteen scenes, 11 minutes 30 seconds.

| # | Kind | Scene |
| --- | --- | --- |
| 1 | poster | Static Factory Method |
| 2 | bullets | The Job |
| 3 | code | The First Attempt Does Not Compile |
| 4 | code | So Everyone Writes This Instead |
| 5 | bullets | Why That Hurts |
| 6 | quote | The Static Factory Method |
| 7 | bullets | A Vending Machine |
| 8 | diagram | The Shape of It |
| 9 | code | The Type Is Its Own Factory |
| 10 | code | Freedom Two: Not to Allocate |
| 11 | code | Freedom Three: to Choose the Class |
| 12 | code | What the Client Looks Like |
| 13 | code | The Same Trick on a Value Type |
| 14 | bullets | You Already Use This Every Day |
| 15 | console | Running It |
| 16 | bullets | Where It Stops |
| 17 | bullets | The Rest of the Family |
| 18 | title | One Sentence to Keep |
| 19 | outro | Thanks for Watching |

The shape is worth copying, because it is what makes the video teachable:
**pose the problem → show the obvious answer failing → name the technique →
give it a physical analogy → draw the structure → walk the real code → run it
→ say where it stops → one sentence to keep.** A student who stops halfway has
still learned something useful at every point along that line.

---

## 12. Porting this to a new project

1. Copy `make_slides.py`, `make_subtitles.py` and `build_video.sh` into the new
   project's `video/`.
2. Rename the three `OUT_*` values in `build_video.sh` and the default output
   name in `make_subtitles.py`.
3. Change the footer label in `make_slides.py`, the poster's two title lines,
   its two pills and its tagline, and the syntax-colouring rules for the
   identifiers the new topic actually uses.
4. Read the real source. Run the real demo and keep its output.
5. Write `scenes.py` — 15–19 scenes following the shape in §11.
6. `python3 make_slides.py build`, and look at every slide.
7. `./build_video.sh`, then run every check in §9.
8. Generate `narration.md`, write `video/README.md`, and update the project's
   own README with the video link and a timestamp table read off the finished
   SRT.
9. Add the `/video/*` block from §1 to `.gitignore`.
