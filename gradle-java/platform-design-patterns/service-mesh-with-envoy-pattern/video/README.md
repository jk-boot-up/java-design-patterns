# Service Mesh with Envoy Pattern — Teaching Video

A narrated, slide-based video that shows what Envoy adds to the Service Mesh pattern,
and the failures that are its own.

## Output Files

| File | What it is |
| --- | --- |
| `service-mesh-with-envoy-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `service-mesh-with-envoy-pattern-explained.m4a` | Audio-only version. |
| `service-mesh-with-envoy-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Not the thumbnail. |

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

## Rebuilding

```bash
./build_video.sh
```

The audio chain is identical across every project in this repository; see
[`../../../architectural-design-patterns/layered-architecture-pattern/video/README.md`](../../../architectural-design-patterns/layered-architecture-pattern/video/README.md)
for the full explanation.

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Service Mesh with Envoy | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | Each Service Carries Its Own |  |
| 5 | A Proxy Beside The Service |  |
| 6 | Change The Policy Once |  |
| 7 | Who Is Calling |  |
| 8 | Numbers For Free |  |
| 9 | The Bill |  |
| 10 | The Verdict |  |
| 11 | How To Recognise It |  |
| 12 | Where You Have Met This |  |
| 13 | What Was Used |  |
| 14 | What Is Real Here |  |
| 15 | When This Is Too Much |  |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force service-mesh-with-envoy`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `service-mesh-with-envoy-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Service Mesh pattern in Java: the proxy in front of a service applies the
> retry, identity and counting policy from its configuration, and the service
> carries none of that code. Explained with Envoy, a real proxy. With an
> online store's payment service, we watch three callers retry three different
> ways, then let one real proxy retry for a caller that has no retry code,
> change the policy in one file, refuse an unknown caller before it reaches
> payments, and read the proxy's own counters. We finish with the bill.
