"""Voice auditions: one text rendered through several voices, level-matched.

    videokit.sh samples script.txt out/ kokoro:af_bella kokoro:af_heart@1.0 say:Samantha@130

A voice is engine:voice, optionally @speed (kokoro) or @rate (say). The
text uses the same narration markup as scenes.py, pauses included.
"""

from pathlib import Path

import soundfile as sf

from . import audio, narrate, tts


def parse_voice(spec):
    engine, _, rest = spec.partition(":")
    voice, _, pace = rest.partition("@")
    if engine == "say":
        return engine, voice, 1.0, int(pace or 145)
    return engine, voice, float(pace or 0.9), 145


def render(text, out_dir, voices):
    """Write <n>-<engine>-<voice>.m4a per voice into out_dir; return paths."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for n, spec in enumerate(voices, start=1):
        engine_name, voice, speed, rate = parse_voice(spec)
        engine = tts.get(engine_name, voice, speed, rate)
        samples, _ = narrate.speak(engine, text)
        stem = out_dir / ("%02d-%s-%s" % (n, engine_name, voice))
        wav = stem.with_suffix(".wav")
        sf.write(wav, samples, engine.sample_rate)
        # Same loudness for all, so the louder voice does not win by default.
        audio.encode(wav, stem.with_suffix(".m4a"),
                     "aresample=48000,highpass=f=75," + audio.loudnorm_filter(wav))
        wav.unlink()
        paths.append(stem.with_suffix(".m4a"))
    return paths
