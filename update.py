import requests

USERNAME = "royce_the_ta"

url = f"https://data.typeracer.com/users?id=tr:{USERNAME}"

response = requests.get(url)
response.raise_for_status()

data = response.json()

print("Username:", USERNAME)
print("Recent Average WPM:", data["tstats"]["recentAvgWpm"])
