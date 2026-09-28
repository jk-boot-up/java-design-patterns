"""Runs inside the Coqui venv ($VIDEOKIT_HOME/coqui): one model, many phrases.

stdin:  one JSON line per phrase {"text": ..., "out": "/path.wav"}
stdout: one line per phrase, "ok" or "error: ..."
The first line printed is the sample rate, once the model is loaded.
"""

import json
import sys
import warnings

warnings.filterwarnings("ignore")
from TTS.api import TTS  # noqa: E402

model, speaker, speed = sys.argv[1], sys.argv[2] or None, float(sys.argv[3])
tts = TTS(model, progress_bar=False)
print(tts.synthesizer.output_sample_rate, flush=True)
for line in sys.stdin:
    job = json.loads(line)
    try:
        kw = {"speaker": speaker} if speaker else {}
        tts.tts_to_file(text=job["text"], file_path=job["out"], speed=speed, **kw)
        print("ok", flush=True)
    except Exception as e:  # keep serving; report the failure
        print("error: %s" % e, flush=True)
