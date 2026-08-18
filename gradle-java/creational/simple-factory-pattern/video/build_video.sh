#!/usr/bin/env bash
#
# Builds the Simple Factory pattern teaching video.
#
#   1. renders one 1920x1080 slide per scene          (make_slides.py)
#   2. narrates each scene with a female voice        (macOS `say`)
#   3. joins each slide to its narration              (ffmpeg)
#   4. concatenates every scene into the final video  (ffmpeg)
#
# Outputs:
#   simple-factory-pattern-explained.mp4   1080p H.264 + AAC, ready for YouTube
#   simple-factory-pattern-explained.m4a   audio-only version (podcast / revision)
#
# Requirements: macOS (for `say`), ffmpeg, python3 with pillow + matplotlib.
#
set -euo pipefail

cd "$(dirname "$0")"

BUILD=build
VOICE="${VOICE:-Samantha}"     # female US English voice
RATE="${RATE:-170}"            # words per minute
OUT_VIDEO=simple-factory-pattern-explained.mp4
OUT_AUDIO=simple-factory-pattern-explained.m4a
OUT_SUBS=simple-factory-pattern-explained.srt

command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }
command -v say    >/dev/null || { echo "macOS 'say' is required"; exit 1; }

mkdir -p "$BUILD"
rm -f "$BUILD"/*.aiff "$BUILD"/*.m4a "$BUILD"/scene-*.mp4 "$BUILD"/concat.txt

echo "==> 1/4  rendering slides"
python3 make_slides.py "$BUILD"

echo "==> 2/4  writing narration text"
python3 - "$BUILD" <<'PY'
import sys, os
from scenes import SCENES
out = sys.argv[1]
for s in SCENES:
    with open(os.path.join(out, s["key"] + ".txt"), "w") as fh:
        fh.write(s["narration"])
    print("text   ->", s["key"] + ".txt")
PY

echo "==> 3/4  narrating with voice '$VOICE' and building scene clips"
for txt in "$BUILD"/*.txt; do
    key=$(basename "$txt" .txt)
    png="$BUILD/$key.png"
    aiff="$BUILD/$key.aiff"

    say -v "$VOICE" -r "$RATE" -o "$aiff" -f "$txt"

    # a beat of silence at the end of each scene so slides do not snap past
    ffmpeg -y -loglevel error \
        -loop 1 -i "$png" \
        -i "$aiff" \
        -filter_complex "[1:a]apad=pad_dur=0.9[a]" \
        -map 0:v -map "[a]" \
        -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 \
        -c:a aac -b:a 192k -ar 48000 -ac 2 \
        -shortest "$BUILD/scene-$key.mp4"

    echo "scene  -> scene-$key.mp4"
done

echo "==> 4/5  concatenating"
for f in "$BUILD"/scene-*.mp4; do
    echo "file '$(basename "$f")'" >> "$BUILD/concat.txt"
done

ffmpeg -y -loglevel error -f concat -safe 0 -i "$BUILD/concat.txt" \
    -c copy "$OUT_VIDEO"

ffmpeg -y -loglevel error -i "$OUT_VIDEO" -vn -c:a aac -b:a 192k -ac 2 "$OUT_AUDIO"

# Subtitles are timed from the narration audio, so this must run before the
# intermediates are cleaned up.
echo "==> 5/5  generating subtitles"
python3 make_subtitles.py "$BUILD" "$OUT_SUBS"

# Keep only the slides; drop the narration/clip intermediates.
if [ -z "${KEEP_INTERMEDIATE:-}" ]; then
    rm -f "$BUILD"/*.aiff "$BUILD"/*.txt "$BUILD"/scene-*.mp4 "$BUILD"/concat.txt
fi

echo
echo "Done."
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT_VIDEO"
echo "  video:     $OUT_VIDEO"
echo "  audio:     $OUT_AUDIO"
echo "  subtitles: $OUT_SUBS"
