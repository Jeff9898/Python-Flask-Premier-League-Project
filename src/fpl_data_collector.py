import requests
import sqlite3
import os
import datetime

def log_message(message):
    """Log a message to a log file to track runs"""
    log_path = os.path.join(os.path.dirname(__file__), 'fpl_data_collection.log')
    # Open the log file in 'a' (append) mode and explicitly set encoding to 'utf-8'
    with open(log_path, 'a', encoding='utf-8') as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")

def fetch_fpl_data():
    """Fetches general FPL data (players, teams, etc.)"""
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    try:
        log_message("Attempting to fetch data from FPL API")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            log_message("Successfully fetched data from FPL API")
            return response.json()
        else:
            log_message(f"Failed to fetch data from FPL API: Status code {response.status_code}")
            return None
    except Exception as e:
        log_message(f"Error fetching data from FPL API: {e}")
        return None

def create_database(db_path):
    """Create the player data table if it doesn't exist"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                web_name TEXT,
                team_id INTEGER,
                position INTEGER,
                price REAL,
                transfers_in INTEGER,
                transfers_out INTEGER,
                ownership_percent REAL,
                avg_points_per_game REAL,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()
        log_message("Database and table created (if not existing)")
    except Exception as e:
        log_message(f"Error creating database: {e}")

def insert_player_data(db_path, players):
    """Insert the player data into the database with a unique timestamp for each run"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for player in players:
            # Insert the new player data including a full timestamp to ensure uniqueness
            cursor.execute('''
                INSERT INTO player_data (
                    player_id, web_name, team_id, position, price, transfers_in, transfers_out,
                    ownership_percent, avg_points_per_game, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                player['id'],
                player['web_name'],
                player['team'],
                player['element_type'],
                player['now_cost'] / 10,  # Price in millions
                player['transfers_in'],
                player['transfers_out'],
                player['selected_by_percent'],
                player['points_per_game'],
                timestamp
            ))
            log_message(f"Inserted data for player {player['web_name']} with timestamp {timestamp}")

        conn.commit()
        conn.close()
        log_message(f"Inserted data for {len(players)} players into the database")
    except Exception as e:
        log_message(f"Error inserting data into the database: {e}")

def main():
    """Main function to run the data collection process"""
    db_path = os.path.join(os.path.dirname(__file__), 'fpl_data.db')
    log_message("Starting data collection script")

    # Fetch FPL data
    fpl_data = fetch_fpl_data()
    if fpl_data:
        # Create database and tables if they do not exist
        create_database(db_path)

        # Extract player data from the API response
        players = fpl_data['elements']

        # Insert player data into the database (append, do not overwrite)
        insert_player_data(db_path, players)
        log_message("Data collection completed successfully")
    else:
        log_message("Data collection failed due to fetch error")

if __name__ == "__main__":
    main()



