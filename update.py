import json
import os
import requests

# Get usernames from Power Automate
with open(os.environ["GITHUB_EVENT_PATH"], "r") as f:
    event = json.load(f)

users = event["client_payload"]["users"]
refreshID = event["client_payload"]["refreshID"]

# Power Automate may send the array as a JSON string
if isinstance(users, str):
    users = json.loads(users)

usernames = [user["Username"] for user in users]

# Get Recent Average WPM from TypeRacer
players = []

for username in usernames:
    try:
        url = f"https://data.typeracer.com/users?id=tr:{username}"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        wpm = data["tstats"]["recentAvgWpm"]
        
        players.append({
            "username": username,
            "wpm": wpm
        })

    except Exception as e:
        print(f"Skipping {username}: {e}")

# Sort highest WPM first
players.sort(key=lambda player: player["wpm"], reverse=True)

# Save leaderboard results
with open("leaderboard.json", "w") as f:
    json.dump(players, f, indent=2)


# Display leaderboard in GitHub Actions
print("=== TYPE RACER LEADERBOARD ===")

for rank, player in enumerate(players, start=1):
    print(
        f"{rank}. {player['username']} - "
        f"{player['wpm']:.2f} WPM"
    )
print("refreshID: ")
print(refreshID)

# Send leaderboard to GitHub Issue #1
token = os.environ["GITHUB_TOKEN"]

issue_url = "https://api.github.com/repos/MrYoYo88/TypeRacer-Leaderboard-Update/issues/1"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

issue_body = "```json{\n" + '"refreshID: "' + str(refreshID) + '\n"userScores: "' + json.dumps(players, indent=2) + "\n}```"

response = requests.patch(
    issue_url,
    headers=headers,
    json={
        "body": issue_body
    }
)

response.raise_for_status()

print("Leaderboard successfully sent to GitHub Issue #1!")
