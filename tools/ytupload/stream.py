"""Upload every rebuilt video, one by one, each only after verify.py passes it.

    tools/ytupload/.venv/bin/python tools/ytupload/stream.py [state-dir]

State lives in ~/.ytupload-chrome/stream/ by default: done.txt (one "ok <project>"
line per rebuilt video), verified.txt (PASS/FAIL per video) and logs/ (each
video's rebuild log, which verify.py reads). Stops uploading while YouTube
refuses custom thumbnails and carries on once it accepts them again; retries
after Studio timeouts. See docs/youtube-upload-plan.md, "Resuming".
"""
import os, sys, time
S = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.ytupload-chrome/stream")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO + "/tools/ytupload")
os.chdir(REPO)
import ytupload as Y
ORDER = ["concurrency-design-patterns", "creational", "domain-driven-design-patterns",
         "enterprise-design-patterns", "foundational-design-patterns", "functional-design-patterns",
         "messaging-integration-patterns", "platform-design-patterns", "security-design-patterns",
         "structural", "testing-design-patterns", "micro-services-design-patterns",
         "architectural-design-patterns", "behavioural"]
tries = {}
VERIFY = [os.path.expanduser("~/.cache/videocheck/bin/python"),
          os.path.join(REPO, "tools", "ytupload", "verify.py"), S]


def verdict(rel):
    """PASS/FAIL from verified.txt; verify the video first if it has not been checked."""
    for line in reversed(open(S + "/verified.txt").read().splitlines()):
        if line.split(":")[0].split()[-1] == rel:
            return line.split()[0]
    import subprocess
    r = subprocess.run(VERIFY + [rel], capture_output=True, text=True)
    print(r.stdout.strip(), flush=True)
    return "PASS" if r.returncode == 0 else "FAIL"


while True:
    if Y.thumbnail_limited():                   # no thumbnail, no upload: wait for the next day
        print("thumbnail limit reached; uploads paused until YouTube accepts thumbnails", flush=True)
        while Y.thumbnail_limited():
            time.sleep(600)
        print("thumbnail limit cleared; resuming", flush=True)
    lines = open(S + "/done.txt").read().split("\n")
    built = [l.split()[1].split("gradle-java/")[1] for l in lines if l.startswith("ok ")]
    reg = Y.load_registry()
    ready = [r for r in built if tries.get(r, 0) < 2 and (r not in reg or
             (reg[r].get("visibility") == "Draft" and reg[r].get("tries", 0) < 2))]
    ready.sort(key=lambda r: (ORDER.index(r.split("/")[0]), r))
    rel = next((r for r in ready if verdict(r) == "PASS"), None)   # never upload an unverified video
    if rel:
        tries[rel] = tries.get(rel, 0) + 1
        try:
            Y.batch(["gradle-java/" + rel])     # one video; waits by itself at the daily limit
            crashes = 0
        except (Exception, SystemExit) as e:    # Studio timeouts, lost browser: pause, retry
            crashes = globals().get("crashes", 0) + 1
            tries[rel] -= 1
            print("crash %d on %s: %s" % (crashes, rel, (str(e) or repr(e)).splitlines()[0]), flush=True)
            if crashes >= 5:
                print("stopped after 5 crashes in a row"); break
            time.sleep(120)
            continue
        if Y.thumbnail_limited():               # stopped for the day: the loop waits, then resumes
            tries[rel] -= 1
            continue
        if "STOPPED" in open(Y.STATUS).read():
            print("stopped:", open(Y.STATUS).read().strip()); break
    elif len([l for l in lines if l.strip()]) >= 272:
        break
    else:
        time.sleep(120)
print("upload stream finished")
