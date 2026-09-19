import time
import uuid

# This runs once, when the platform starts a new copy of the function: the cold start.
INSTANCE = str(uuid.uuid4())[:8]
calls = 0


def handler(event, context):
    global calls
    calls += 1
    if event.get("sleep"):
        time.sleep(event["sleep"])
    if event.get("hold"):
        time.sleep(event["hold"])
    return {"receipt": "sent for " + event.get("orderId", "?"), "instance": INSTANCE, "callsOnThisInstance": calls}
