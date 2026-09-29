# Distributed Tracing with Jaeger Pattern — Teaching Video

A narrated, slide-based video that teaches distributed tracing with
OpenTelemetry and a real Jaeger collector: a hop that forgets the trace
header, the header forwarded, spans that arrive later in batches, sampling at
the front door, a clock that is off, and the spans a crash loses.

| File | What it is |
| --- | --- |
| `distributed-tracing-with-jaeger-pattern-explained.mp4` | the video, 1920×1080 |
| `distributed-tracing-with-jaeger-pattern-explained.m4a` | audio only |
| `distributed-tracing-with-jaeger-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

The mp4, m4a and srt are not committed; `poster.png` is.

**Narration:** the amy-slow voice (Piper, `en_US-amy-medium`, slower, with
longer pauses), set in `videokit.toml` and built by the shared videokit
library. Scenes live in `scenes.py`.

## Rebuilding

```bash
../../../../tools/videokit/videokit.sh all distributed-tracing-with-jaeger
```

Suggested description:

> Distributed Tracing pattern in Java, explained with OpenTelemetry and a
> real Jaeger collector, using an online store product page built by two
> programs: the page and a recommendations service. One customer request
> gets one trace ID, every piece of work records a span with its parent, and
> Jaeger puts the spans back together into one story, like a hospital
> records office joining forms by wristband number. We watch a forgotten
> header split one page load into two healthy-looking traces, forward it
> and get one trace of eight spans, see spans arrive seconds later in
> batches, sample one trace in four at the front door, and meet a clock that
> makes an answer arrive before its question. We finish with the bill: a
> crash loses exactly the spans you would want to read.
