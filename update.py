import json
import os
import requests

# Get usernames from Power Automate
with open(os.environ["GITHUB_EVENT_PATH"], "r") as f:
    event = json.load(f)

users = event["client_payload"]["users"]

# Power Automate may send the array as a JSON string
if isinstance(users, str):
    users = json.loads(users)

usernames = [user["Username"] for user in users]

# Get Recent Average WPM from TypeRacer
players = []

for username in usernames:
    url = f"https://data.typeracer.com/users?id=tr:{username}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    wpm = data["tstats"]["recentAvgWpm"]

    players.append({
        "username": username,
        "wpm": wpm
    })

# Sort highest WPM first
players.sort(key=lambda player: player["wpm"], reverse=True)

# Display leaderboard
print("=== TYPE RACER LEADERBOARD ===")

for rank, player in enumerate(players, start=1):
    print(
        f"{rank}. {player['username']} - "
        f"{player['wpm']:.2f} WPM"
    )
