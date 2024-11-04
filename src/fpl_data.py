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

def get_team_abbreviation(team_id, teams):
    """Get team abbreviation from team ID."""
    for team in teams:
        if team['id'] == team_id:
            return team['short_name']
    return 'Unknown'

def main():
    # Fetch general player data and team data from the FPL API
    fpl_data = fetch_fpl_data()

    if fpl_data:
        players = fpl_data['elements']
        teams = fpl_data['teams']
        player_data = []

        for player in players:
            # Skip players who are unavailable or loaned out
            if player['status'] == 'u' or player.get('loaned_out', False):
                continue

            # Get the team abbreviation
            team_abbr = get_team_abbreviation(player['team'], teams)

            # Construct the player image URL and force .png extension
            photo_filename = player['photo'].replace('.jpg', '')  # Remove any .jpg extension if present
            image_url = f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{photo_filename}.png"

            # Add the player data, including new fields such as xG and xA
            player_info = {
                'web_name': player['web_name'],
                'price': player['now_cost'] / 10,  # Price in millions
                'position': {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}.get(player['element_type'], 'Unknown'),
                'team': team_abbr,
                'avg_points_per_game': player['points_per_game'],
                'expected_points': player.get('ep_this', 0),  # Expected points for current GW
                'xG': player.get('expected_goals', 0),  # Expected Goals (using placeholder, replace with real field if available)
                'xA': player.get('expected_assists', 0),  # Expected Assists (using placeholder, replace with real field if available)
                'fixture': 'N/A',  # Placeholder for fixture, this will be updated later
                'image_url': image_url
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

















