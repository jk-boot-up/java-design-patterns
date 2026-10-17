# videokit

The shared library that builds every pattern project's narrated video, its
audio-only edition, its subtitles, its thumbnail and the narration of its
browser animation. Projects keep only their content (`video/scenes.py` and
`video/videokit.toml`); the pipeline lives here.

```bash
tools/videokit/videokit.sh all <project>   # everything, including the YouTube docs
tools/videokit/videokit.sh help            # every command
```

`<project>` is a project directory, its `video/` directory, or just its slug.
The Python environment and the `amy-slow` Piper voice model are created on the
first run in `$VIDEOKIT_HOME` (default `~/.cache/videokit`), outside the
repository. The rules the output must meet are in
[`AUDIO-VIDEO-SPEC.md`](../../AUDIO-VIDEO-SPEC.md).
