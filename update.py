import os
import json

payload = os.environ.get("GITHUB_EVENT_PATH")

with open(payload, "r") as f:
    event = json.load(f)

print("=== PAYLOAD RECEIVED ===")
print(json.dumps(event.get("client_payload"), indent=2))
