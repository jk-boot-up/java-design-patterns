"""Verify one rebuilt project video before it may go to YouTube.

    ~/.cache/videocheck/bin/python tools/ytupload/verify.py <state-dir> <project path relative to gradle-java>

<state-dir> is ~/.ytupload-chrome/stream (see stream.py). The speech check needs
faster-whisper, installed outside the repository:
    python3 -m venv ~/.cache/videocheck && ~/.cache/videocheck/bin/pip install faster-whisper

Prints PASS or FAIL with the reasons, appends the same line to verified.txt,
and exits 0 only on PASS.
"""
import json, os, re, subprocess, sys

S, REL = sys.argv[1], sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRADLE = REPO + "/gradle-java"
sys.path.insert(0, REPO + "/tools/ytupload")
proj = os.path.join(GRADLE, REL)
slug = os.path.basename(proj)
vdir = os.path.join(proj, "video")
NEW = ["kindly subscribe to the channel", "it helps the channel grow and bring you more content",
       "thanks for watching!"]
OLD = ["rest of the series", "a like really does help"]
bad = []


def check(ok, why):
    if not ok:
        bad.append(why)
    return ok


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


# 1. the voice: amy-slow only
amy_toml = os.path.join(vdir, "videokit-amy-slow.toml")
toml = amy_toml if os.path.exists(amy_toml) else os.path.join(vdir, "videokit.toml")
t = open(toml).read()
check('"piper"' in t and "en_US-amy-medium" in t and re.search(r"speed\s*=\s*0\.8\b", t),
      "voice config is not amy-slow: " + os.path.basename(toml))
log = os.path.join(S, "logs", slug + ".log")
lt = open(log).read() if os.path.exists(log) else ""
check("piper en_US-amy-medium" in lt, "rebuild log does not show the amy-slow voice")
check("audio continuous" in lt and "Traceback" not in lt, "rebuild log shows a problem")
check("kokoro" not in lt.lower(), "rebuild log mentions Kokoro")

# 2. the files: fresh, and built from the current script
base = os.path.join(vdir, slug + "-explained" + ("-amy-slow" if toml == amy_toml else ""))
mp4, srt = base + ".mp4", base + ".srt"
scenes_t = os.path.getmtime(os.path.join(vdir, "scenes.py"))
if check(os.path.exists(mp4) and os.path.exists(srt), "video or captions missing"):
    check(os.path.getmtime(mp4) > scenes_t and os.path.getmtime(srt) > scenes_t,
          "video or captions older than scenes.py")
    st = open(srt).read()
    flat = re.sub(r"\s+", " ", st).lower()
    check(all(n in flat for n in NEW), "captions lack the new subscribe lines")
    check(not any(o in flat for o in OLD), "captions still have the old subscribe lines")
    ends = re.findall(r"--> (\d+):(\d+):(\d+),(\d+)", st)
    srt_end = (lambda h, m, s, ms: int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000)(*ends[-1])

    # 3. picture and sound
    p = json.loads(run("ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", mp4).stdout)
    vs = [s for s in p["streams"] if s["codec_type"] == "video"]
    au = [s for s in p["streams"] if s["codec_type"] == "audio"]
    check(vs and vs[0]["codec_name"] == "h264" and (vs[0]["width"], vs[0]["height"]) == (1920, 1080),
          "video stream is not 1920x1080 H.264")
    check(au and au[0]["codec_name"] == "aac", "no AAC audio stream")
    dur = float(p["format"]["duration"])
    check(srt_end <= dur + 0.5 and dur - srt_end < 15, "duration %.1fs does not fit captions ending %.1fs" % (dur, srt_end))
    e = run("ffmpeg", "-nostats", "-i", mp4, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", e)
    pk = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)
    check(i and -17.5 <= float(i[-1]) <= -14.5, "loudness %s LUFS is off the -16 target" % (i[-1] if i else "?"))
    check(pk and float(pk[-1]) <= -0.5, "true peak %s dBFS above -0.5" % (pk[-1] if pk else "?"))

    # 4. what the outro actually says, heard from the video's own audio
    import numpy as np
    from faster_whisper import WhisperModel
    raw = subprocess.run(["ffmpeg", "-v", "error", "-sseof", "-50", "-i", mp4, "-vn", "-ac", "1",
                          "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    segs, _ = WhisperModel("base.en", device="cpu", compute_type="int8").transcribe(audio)
    heard = re.sub(r"\s+", " ", re.sub(r"[^a-z ]", "", " ".join(s.text for s in segs).lower()))
    for phrase in ("found this useful", "subscribe to the channel", "channel grow", "thanks for watching"):
        check(phrase in heard, "outro audio does not say %r (heard: ...%s)" % (phrase, heard[-160:]))
    check("rest of the series" not in heard, "outro audio still says the old lines")

# 5. thumbnail and the YouTube fields
thumb = os.path.join(proj, "docs", "thumbnail.png")
if check(os.path.exists(thumb), "thumbnail missing"):
    s = json.loads(run("ffprobe", "-v", "error", "-show_streams", "-of", "json", thumb).stdout)["streams"][0]
    check((s["width"], s["height"]) == (1280, 720), "thumbnail is not 1280x720")
try:
    import ytupload as Y
    sh = Y.sheet(proj)
    check(sh["video"] == mp4, "uploader would pick %s" % os.path.basename(sh["video"]))
    check("http://" not in sh["description"] and "https://" not in sh["description"], "description has a URL scheme")
    check("00:00" in sh["description"], "description chapters do not start at 00:00")
except SystemExit as e:
    bad.append("YouTube sheet: %s" % e)

line = ("PASS " + REL) if not bad else ("FAIL %s: %s" % (REL, "; ".join(bad)))
print(line)
with open(os.path.join(S, "verified.txt"), "a") as f:
    f.write(line + "\n")
sys.exit(0 if not bad else 1)
