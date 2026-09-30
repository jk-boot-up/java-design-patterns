# Acyclic Visitor Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `acyclic-visitor-pattern-explained.mp4` | the video, 1920×1080 |
| `acyclic-visitor-pattern-explained.m4a` | audio only |
| `acyclic-visitor-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Acyclic Visitor pattern in Java: a visitor is an operation kept outside the
> classes it works on; in the acyclic version each type gets its own tiny
> visitor interface, so a new type changes nothing that already exists, like
> hotel staff wearing one badge per language they speak. Explained with an
> online store catalogue of books, food and electronics, and later gift cards,
> where visitors work out VAT and customs forms. We see what goes wrong with
> the classic visitor, fix it, add a product type without touching old code,
> and write a visitor for just one type. We finish with the bill.
