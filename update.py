import json
import os

# Read the GitHub repository_dispatch event
with open(os.environ["GITHUB_EVENT_PATH"], "r") as f:
    event = json.load(f)

users = event["client_payload"]["users"]

# If Power Automate sent the array as a JSON string, convert it back to a list
if isinstance(users, str):
    users = json.loads(users)

usernames = [user["Username"] for user in users]

print("=== USERNAMES RECEIVED ===")

for username in usernames:
    print(username)
