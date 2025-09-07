import requests
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

players = pd.DataFrame(data['elements'])

players = players[['first_name', 'second_name', 'team', 'now_cost', 'total_points', 'minutes']]

players.to_csv("data/players.csv", index=False)

print(players.head())