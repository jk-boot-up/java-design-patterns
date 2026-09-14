# Build Specification — Toolchain, File Shapes And Known Traps

How a project in this category is actually built: the exact commands, the exact shape each
generated file has to have, and the mistakes that have cost real time. It is written for a
session resuming work with no memory of how any of this was produced.

[`spec.md`](spec.md) says *what* each project teaches. This document says *how* the artefacts
are made. [`ai-session.md`](ai-session.md) holds the standing instructions and the current
state of the work.

---

## 1. Environment

| | |
| --- | --- |
| Java | 21, via each project's own Gradle wrapper |
| Gradle | 9.2.1, wrapper committed per project |
| Tests | JUnit 5 |
| Runtime dependencies | none, in any project |
| Python | 3, standard library plus Pillow for the slide generators |
| Audio and video | macOS `say`, and `ffmpeg` |
| Diagrams | `mmdc`, the Mermaid CLI |

Everything runs offline once the Gradle wrapper has downloaded itself once. There is no
broker, no database and no container anywhere in the category — that is a deliberate rule from
[`spec.md`](spec.md) §2.1, not a shortcut.

---

## 2. The shared generators

The four generators live in `gradle-java/docs/` and are shared by all thirty-seven projects.

> **They must be run from the `gradle-java` directory, and they take a slug with the
> `-pattern` suffix removed.** `cqrs`, not `cqrs-pattern`.

```bash
cd gradle-java

python3 docs/make_specs.py <slug>          # docs/spec.md + docs/spec.html
python3 docs/make_youtube_docs.py <slug>   # docs/youtube.md
python3 docs/make_thumbnails.py <slug>     # docs/thumbnail.png
python3 docs/make_narration.py --force <slug>   # video/narration.md
```

With no arguments, each processes every project it knows about. `make_specs.py` also accepts
`--no-measure` to skip the loudness measurement, which is the slow part.

### Registration

`make_narration.py` discovers projects by walking the category directories for anything ending
in `-pattern`, so a new project needs nothing from you. Note that it **keeps an existing
`narration.md` unless you pass `--force`**, and prints `kept (already written)` when it does —
easy to mistake for success after editing `scenes.py`.

The other three are different. **`make_specs.py`, `make_thumbnails.py` and
`make_youtube_docs.py` each carry their own table of slugs**, holding per-project content such
as the thumbnail's wording and the video title. Adding the directory is not enough; a project
missing from those tables is silently skipped.

### make_specs.py reads the rendered video

`make_specs.py` measures the mp4 to fill in the runtime, the subtitle count and the integrated
loudness. **If the video is not on disk when you run it, the spec silently degrades** to
`~not yet built over 0 scenes, 0 subtitle cues` rather than failing.

This has already produced one real defect: `service-discovery-pattern/docs/spec.md` sat in the
repository claiming zero scenes because it had been generated before its video was rendered.
Always regenerate the spec *after* the build, and check the line it prints.

A good run prints one line, and every field in it should look plausible:

```
cqrs   spec.md + spec.html  (16 scenes, 17:26, 18 tests, -16.02 LUFS)
```

---

## 3. `video/scenes.py`

The script for the video. One `SCENES` list of dictionaries, 14 to 16 entries.

> **Use `dict(key=..., kind=..., title=..., body=..., narration=...)` keyword form, never a
> dict literal with `"title":` string keys.** `make_specs.py` counts scenes with a regular
> expression looking for `title=`. A literal-style file reports **0 scenes** and the spec is
> quietly wrong.

### Body types

The body's Python type depends on the `kind`, and getting it wrong is a crash or a silent
mess:

| `kind` | `body` must be | Notes |
| --- | --- | --- |
| `poster` | `None` or `""` | |
| `diagram` | `None` or `""` | |
| `bullets` | a **list** of lines | |
| `quote` | a **list** of lines | `kind_quote` raises `TypeError` on a bare string |
| `outro` | a **list** of lines | |
| `code` | a **single string** | split internally on `\n` |
| `console` | a **single string** | split internally on `\n` |

Passing a list where a string is expected fails with
`AttributeError: 'list' object has no attribute 'split'`.

### Layout limits — nothing warns you

Text that overflows a slide is simply drawn past the bottom edge or off the right. Validate
before rendering.

| | Limit |
| --- | --- |
| `bullets`, `quote`, `outro` | **12 lines**, each **≤ 62 characters** |
| `console` | lines **≤ 62 characters** |
| `code` | lines **≤ 52 characters** — tighter, the font is wider |

The 12-line figure comes from the geometry: the body starts at y=260 and steps 60 pixels a
line, and the footer sits at about y=1022.

A validation pass before every render:

```python
import scenes
for s in scenes.SCENES:
    b = s["body"]
    if b is None or b == "": continue
    lines = b if isinstance(b, list) else b.split("\n")
    cap = 52 if s["kind"] == "code" else 62
    if s["kind"] in ("bullets", "quote", "outro") and len(lines) > 12:
        print("TOO TALL", s["key"], len(lines))
    for ln in lines:
        if len(ln) > cap:
            print("TOO WIDE", s["key"], len(ln), ln)
```

---

## 4. `video/make_slides.py`

Renders one PNG per scene into `video/build/`.

Three things carry the *source* project's identity when this file is copied, and all three
must be changed:

1. **The line-2 docstring**, which names the pattern.
2. **`footer(d, label)`**, which hard-codes the pattern name on the right-hand side.
3. **The poster and diagram content**, which is entirely per-project.

### Patching the poster and diagram safely

Both functions are replaced by slicing between markers. **Use these exact boundaries:**

| Function | From | To |
| --- | --- | --- |
| `kind_poster` | `s.index("def kind_poster(scene, img, d):")` | `s.index("\n\ndef kind_outro")` |
| `kind_diagram` | `s.index("def kind_diagram(scene, img, d):")` | `s.index("\n\nAUTHOR = ")` |

A generic `"\n\ndef "` boundary looks equivalent and is not: it swallows the module-level
constants `AUTHOR`, `POSTER_TOP`, `POSTER_BOTTOM`, `GOLD` and `RULE`, and the next render
fails with a `NameError`.

### The poster

The poster is lifted out as `video/poster.png` and used as the YouTube thumbnail, so it is the
first and often only thing a viewer judges the video by. It carries a large pattern word, a
short accent line, a *before* pill and an *after* pill each with a one-line result, and two
taglines.

**The before pill is never struck through.** This was an explicit instruction: strikethrough
is unreadable at search-result size and makes the poster look negative. Use colour and the
label to carry the contrast.

### The diagram slide

A right-hand spine of four `(title, subtitle, colour)` rows and a single bottom line. The
bottom line is where the pattern's real lesson goes.

**Check the rendered PNG at full width.** Header lines that look fine in the source run close
to the right edge at 1920 pixels; two have had to be shortened after visual inspection.

---

## 5. `video/build_video.sh` and `make_subtitles.py`

```bash
cd <project>/video
python3 make_slides.py      # one PNG per scene into build/
./build_video.sh            # narrate, clean, level, assemble
python3 make_subtitles.py   # .srt alongside the mp4
```

The output filename is `<slug>-pattern-explained.mp4`, written to `video/`, **not** to
`video/build/`.

> **Both scripts hard-code the source project's output filename when copied.** This has been
> missed more than once — one project inherited `cqrs-pattern-explained`, another inherited
> `strategy-pattern-explained` from a different category entirely. Fix immediately after
> copying:
>
> ```bash
> sed -i '' 's/<old>-pattern-explained/<new>-pattern-explained/g' build_video.sh make_subtitles.py
> ```

### The audio chain, and why it is shaped this way

| | |
| --- | --- |
| Voice | `Samantha`, macOS `say` |
| Rate | 145 words per minute — the pace educational YouTube settles on |
| Cleanup | `highpass=f=75` plus a gentle 3 kHz presence lift |
| Levelling | `loudnorm=I=-16:TP=-1.5:LRA=11`, **two-pass, measured once over the whole timeline** |
| Encode | AAC, 192 kbit/s, 48 kHz stereo |
| Frame rate | 30 |

Two decisions in that chain are load-bearing and should not be "simplified" by a later
session:

**There is deliberately no denoiser.** An earlier version ran one and it made the voice sound
underwater. `say` output has no noise floor worth removing.

**Levelling is not part of the per-scene cleanup.** Run per scene, `loudnorm` re-measures each
clip independently and pushes a quiet scene up to match a loud one, which audibly pumps across
a cut. It runs once, in two-pass mode, over the assembled timeline.

**Per-scene AAC concatenation needs care**, because AAC is a lapped format and every separately
encoded clip carries priming samples. The script handles this; the check at the end exists to
prove it worked.

### The continuity check

A successful build prints:

```
audio timeline continuous: NNNNN packets, no gaps
```

**If that line is missing or reports a gap, the build failed even if an mp4 was produced.** A
gap means a scene join or the concatenation dropped samples, and the video will have an
audible click or a silence.

### A render takes eight to ten minutes

Run it in the background and wait on the output file rather than blocking:

```bash
until [ -f <slug>-pattern-explained.mp4 ]; do sleep 20; done
```

**Delete `video/.build.log` afterwards.** It is not covered by `.gitignore` and will otherwise
be committed.

---

## 6. `docs/animation.html`

A single self-contained HTML file — no network, no dependencies — holding a stepped animation
with narration, a console, and play / step / reset / audio controls.

### Assembling one from the reference

The file is built in three pieces, taking the head and the engine from `cqrs-pattern`:

```python
REF = ".../cqrs-pattern/docs/animation.html"
lines = open(REF).readlines()
head   = "".join(lines[:166])   # through </head>
engine = "".join(lines[385:])   # from the line after the STEPS array closes
```

**The `385` is exact.** Line 385 is the `];` that closes `STEPS`, and line 386 is
`const BOXES = ["b-naive", "b-client"];`. Slicing a line either side breaks the script.

Between the two pieces go the new body markup and a new `const STEPS = [...]`.

### Element ids the engine requires

The copied engine addresses these by id, and every one must exist in the new body markup:

```
b-naive  b-client
r-s1 r-s2 r-s3 r-s4      r-c1 r-c2 r-c3
n-s1 n-s2 n-s3 n-s4      n-c1 n-c2 n-c3
naive-state  holding  clock  gate-label  family-label  bridge-rail
narration  console-lines  progress
play  step  reset  audio  audio-icon  audio-note
```

### Row and console classes

| Class | Meaning |
| --- | --- |
| `.row.dim` | opacity .38 |
| `.row.absent` | opacity .22, dashed border |
| `.row.wrong` | red |
| `.row.ok` | green |
| `.row.wait` | amber |
| `.c-context` / `.c-strategy` | green / purple console text |
| `.c-pick` / `.c-out` | a decision / ordinary output |
| `.c-bad` / `.c-good` | red / green |

### Validate before considering it done

Four checks, all of which have caught real breakage:

```bash
# 1. the script parses
python3 - <<'EOF'
h = open("docs/animation.html").read()
open("docs/.chk.js","w").write(h.split("<script>",1)[1].rsplit("</script>",1)[0])
EOF
node --check docs/.chk.js && rm docs/.chk.js
```

2. Every `r-*` and `b-*` id referenced in `STEPS` exists as an element id.
3. Every caption key — matched with `(?:^|,)\s*(\w+):` — has a matching `n-*` element.
4. Every `cls:` value used in `STEPS` has a CSS rule.

Delete any scratch file afterwards.

> **`str.replace` is global.** Replacing a line that appears in both `render()` and `reset()`
> collapses the pair and leaves `reset()` referring to an undefined variable. This has happened.
> Either include enough surrounding context to make the match unique, or order the replacements
> so the more specific one runs first.

---

## 7. `docs/make_animation_audio.sh`

Generates one short clip per animation step into `docs/audio/`, which is **ignored by git** —
the script is the source, the clips are output.

The narration lives in a `cat <<'EOF'` heredoc, one line per step. To replace it, slice between
`s.index("cat <<'EOF'\n")` and `s.index("\nEOF\n", start)`.

| | |
| --- | --- |
| Voice and rate | `Samantha` at 145 wpm, matching the video |
| Filter | `highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11` |
| Encode | AAC 128 kbit/s → `docs/audio/step-N.m4a` |

> **The loop reads on file descriptor 3**, not stdin: `done 3< <(narrate)`. `say` consumes
> stdin, and an earlier version using a plain `while read` loop had `say` eat the remaining
> narration lines so only the first clip was produced. Do not "tidy" the fd-3 redirection away.

---

## 8. Rendering the Mermaid diagrams

Extract the **first** Mermaid block from the markdown — that is the one the `![...]` image tag
at the top of the file refers to — and render it:

```bash
cat > /tmp/mmdc-config.json <<'EOF'
{ "theme": "dark", "themeVariables": { "fontSize": "16px" } }
EOF

mmdc -i /tmp/x.mmd -o docs/images/class-diagram.png \
     -b "#0f172a" -s 4 -c /tmp/mmdc-config.json
```

`-s 4` is the scale factor that makes the PNG legible on a high-density display. The
background matches the slide palette.

`uml-diagram.md` holds one sequence diagram per act, and the first block is rendered, so put
the act you most want shown at the top rather than in chronological order.

---

## 9. Environment quirks that have wasted time

- **The shell's working directory can reset between commands.** Prefer absolute paths. A `cd`
  into the directory you are already in fails, and if it is part of an `&&` chain it silently
  short-circuits everything after it.
- **Writing to `/tmp` with the file-writing tool is blocked.** Write scratch files inside the
  project, dot-prefixed, and delete them. Shell heredocs to `/tmp` are fine.
- **`sleep N` chained with another command is blocked.** Use a background run, or an
  `until [ -f ... ]; do sleep 20; done` loop.
- **`ls *.mp4` fails with `no matches found` under zsh**, not an empty result. During a render
  that looks like a build failure and is not.

---

## 10. Checklist for a new or revised project

- [ ] Registered with all four generators in `gradle-java/docs/`.
- [ ] `./gradlew test` passes; no `Thread.sleep` under `src/test`.
- [ ] `./gradlew run` prints a timeline showing both the failure and the pattern's answer.
- [ ] Every number in every document, slide and narration line matches that output.
- [ ] `scenes.py` uses `title=` keyword form; scene count is as expected in the spec output.
- [ ] Body types match their kinds; no slide overflows the 12-line / 62- / 52-character limits.
- [ ] `make_slides.py` docstring, footer, poster and diagram all name *this* pattern.
- [ ] `build_video.sh` and `make_subtitles.py` name *this* project's output file.
- [ ] The build printed `audio timeline continuous`; loudness is within 0.02 LU of −16 LUFS.
- [ ] `animation.html` passes all four validation checks.
- [ ] Both diagrams rendered; the poster and thumbnail looked at, not just generated.
- [ ] `video/.build.log` and any scratch files deleted.
- [ ] Spec regenerated **after** the video existed, and its printed line checked.
- [ ] `git status` shows no mp4, m4a, srt, wav, log, `docs/audio/` or `video/build/`.
