"""Coqui TTS (open source, MPL 2.0) through a helper process.

Coqui needs PyTorch and Python <= 3.13, so it lives in its own venv at
$VIDEOKIT_HOME/coqui (python3.13 -m venv ...; pip install "coqui-tts[codec]"
torch torchaudio "transformers>=4.57,<4.58"). This engine keeps one helper
process alive and sends it one phrase at a time.

Voice names: "jenny" (tts_models/en/jenny/jenny), "vctk-p225" and similar for
the multi-speaker VCTK model, or a full Coqui model name.
"""

import json
import subprocess
import tempfile
from pathlib import Path

import soundfile as sf

from .kokoro import models_dir

BRIDGE = Path(__file__).with_name("coqui_bridge.py")


def _model(voice):
    if voice.startswith("tts_models/"):
        return voice, ""
    if voice.startswith("vctk-"):
        return "tts_models/en/vctk/vits", voice[5:]
    return "tts_models/en/%s/%s" % (voice, voice), ""


class CoquiEngine:
    def __init__(self, voice="jenny", speed=0.9, rate=None):
        python = models_dir().parent / "coqui" / "bin" / "python"
        if not python.exists():
            raise SystemExit("coqui: no venv at %s (see tts/coqui.py)" % python.parent.parent)
        model, speaker = _model(voice)
        self.proc = subprocess.Popen([str(python), str(BRIDGE), model, speaker, str(speed)],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        self.sample_rate = int(self.proc.stdout.readline())
        self.tmp = tempfile.mkdtemp(prefix="coqui-")

    def speak(self, text):
        out = Path(self.tmp) / "phrase.wav"
        self.proc.stdin.write(json.dumps({"text": text, "out": str(out)}) + "\n")
        self.proc.stdin.flush()
        reply = self.proc.stdout.readline().strip()
        if reply != "ok":
            raise RuntimeError("coqui: " + reply)
        samples, _ = sf.read(out, dtype="float32")
        return samples if samples.ndim == 1 else samples.mean(axis=1)
