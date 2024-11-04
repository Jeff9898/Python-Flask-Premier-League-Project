import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('fpl_data.db')
cursor = conn.cursor()

# Fetch some data to verify the connection
cursor.execute('SELECT * FROM player_data LIMIT 5')
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
