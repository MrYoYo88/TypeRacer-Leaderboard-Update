import requests

usernames = [
    "royce_the_ta",
    # Add a couple more TypeRacer usernames here for testing
]

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

players.sort(key=lambda player: player["wpm"], reverse=True)

print("=== TYPE RACER LEADERBOARD ===")

for rank, player in enumerate(players, start=1):
    print(
        f"{rank}. {player['username']} - "
        f"{player['wpm']:.2f} WPM"
    )
