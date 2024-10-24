from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Load player data from src/players_data.csv
    csv_path = os.path.join(os.path.dirname(__file__), 'players_data.csv')
    players_df = pd.read_csv(csv_path)

    # Get sorting parameters from the URL query
    sort_column = request.args.get('sort', 'second_name')  # Default column to sort by
    sort_order = request.args.get('order', 'asc')  # Default order is ascending

    # Check if the column exists in the DataFrame
    if sort_column in players_df.columns:
        # Sort the DataFrame based on the column and order
        players_df = players_df.sort_values(by=sort_column, ascending=(sort_order == 'asc'))

    # Convert the DataFrame to a list of dictionaries for rendering in HTML
    players = players_df.to_dict(orient='records')

    return render_template('index.html', players=players, sort_column=sort_column, sort_order=sort_order)

@app.route('/player/<second_name>', methods=['GET'])
def player_detail(second_name):
    # Load player data from src/players_data.csv
    csv_path = os.path.join(os.path.dirname(__file__), 'players_data.csv')
    players_df = pd.read_csv(csv_path)

    # Find the player by their second name
    player_data = players_df[players_df['second_name'].str.lower() == second_name.lower()]

    # If player data is found, convert to dictionary
    if not player_data.empty:
        player = player_data.to_dict(orient='records')[0]  # Get the first (and only) record
        return render_template('player_detail.html', player=player)

    # If no player is found, display a 404 page
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)



