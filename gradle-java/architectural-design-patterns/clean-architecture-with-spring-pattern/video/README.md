# Clean Architecture with Spring — Teaching Video

A narrated, slide-based video owning one comparison: hand-wiring fails at
compile time, container wiring fails at startup — proven with this
project's own code, not narrated over a diagram.

## Output Files

| File | What it is |
| --- | --- |
| `clean-architecture-with-spring-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `clean-architecture-with-spring-pattern-explained.m4a` | Audio-only version. |
| `clean-architecture-with-spring-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Not the thumbnail. |

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

## Rebuilding

```bash
./build_video.sh
```

The audio chain is identical across every project in this repository; see
[`../../layered-architecture-pattern/video/README.md`](../../layered-architecture-pattern/video/README.md)
for the full explanation.

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Clean Architecture with Spring | Title card, and naming §66 as required watching first |
| 2 | What This Video Owns, And What It Does Not | Scope, stated precisely |
| 3 | What Spring Actually Does | The plain-language definition |
| 4 | What This Project Installs | Version pinned: Spring Boot 4.1.1 |
| 5 | Recognition: @Bean Is Those Twenty Lines | The hand-wired call next to the `@Bean` method |
| 6 | Seven Beans, The Same Seven Objects | The container's startup log |
| 7 | The Forced Change Still Costs Nothing Extra | One more `@Bean`, same as one more `new` |
| 8 | Hand-Wiring Fails At Compile Time | The deleted constructor argument |
| 9 | Container Wiring Fails At Startup | `UnsatisfiedDependencyException`, named |
| 10 | Why The Container Cannot See It Coming | The mechanism, stated plainly |
| 11 | The Cost, Honestly Priced | Three real costs |
| 12 | When This Is Worth The Extra Dependency | The honest boundary |
| 13 | What This Project Deliberately Skips | No re-teaching, no Spring tutorial, no web app |
| 14 | Thanks for Watching | The delete-a-different-bean exercise |

Scene 14 deliberately does not name whichever pattern comes next — there is
none; this is the category's fifth and final project.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force clean-architecture-with-spring`,
then re-run `./build_video.sh`.

## Publishing Notes

Upload `clean-architecture-with-spring-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
