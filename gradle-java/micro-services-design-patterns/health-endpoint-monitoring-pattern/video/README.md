# Health Endpoint Monitoring Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `health-endpoint-monitoring-pattern-explained.mp4` | the video, 1920×1080 |
| `health-endpoint-monitoring-pattern-explained.m4a` | audio only |
| `health-endpoint-monitoring-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Let each instance answer two questions for the platform: am I working at all (restart me if not), and can I take work right now (stop sending it if not). Health Endpoint Monitoring gives each instance two addresses: liveness, which says whether the process works and gets it restarted if not, and readiness, which says whether it can take work now and takes it out of rotation if not.
