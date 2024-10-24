import requests

def fetch_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    print("Fetching data...")  # Debugging print
    response = requests.get(url)
    if response.status_code == 200:
        print("Data fetched successfully!")  # Debugging print
        data = response.json()
        players = data['elements']
        for player in players[:5]:  # Print the first 5 players as an example
            image_url = f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{player['photo']}"
            print(player['second_name'], player['photo'], image_url)  # Display name, photo, and image URL
    else:
        print(f"Failed to fetch data: {response.status_code}")

fetch_fpl_data()
