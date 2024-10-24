import requests
import pandas as pd
import os

def fetch_fpl_data():
    """Fetches general FPL data (players, teams, etc.)"""
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def main():
    # Fetch player data from the FPL API
    fpl_data = fetch_fpl_data()

    if fpl_data:
        players = fpl_data['elements']
        player_data = []

        for player in players:
            # Skip players who are unavailable or loaned out
            if player['status'] == 'u' or player.get('loaned_out', False):
                continue

            # Construct the player image URL and force .png extension
            photo_filename = player['photo'].replace('.jpg', '')  # Remove any .jpg extension if present
            image_url = f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{photo_filename}.png"

            # Add the player data
            player_info = {
                'second_name': player['second_name'],
                'price': player['now_cost'] / 10,  # Price in millions
                'position': player['element_type'],
                'avg_points_per_game': player['points_per_game'],
                'image_url': image_url  # Add image URL
            }
            player_data.append(player_info)

        # Create a DataFrame from the player data
        players_df = pd.DataFrame(player_data)

        # Save the DataFrame to CSV in the src folder
        output_path = os.path.join(os.path.dirname(__file__), 'players_data.csv')
        players_df.to_csv(output_path, index=False)
        print(f"Player data saved to {output_path}")

if __name__ == "__main__":
    main()
















