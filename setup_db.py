import psycopg2
import json

def create_tables(cur):
    commands = (
        """
        CREATE TABLE IF NOT EXISTS lines (
            id SERIAL PRIMARY KEY,
            name VARCHAR
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS stations (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            latitude NUMERIC,
            longitude NUMERIC
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS line_stations (
            line_id INTEGER REFERENCES lines(id),
            station_id VARCHAR REFERENCES stations(id),
            PRIMARY KEY (line_id, station_id)
        )
        """
    )
    for command in commands:
        cur.execute(command)

def load_lines(cur, data):
    command = "INSERT INTO lines(name) VALUES(%s)"
    for line_obj in data["lines"]:
        cur.execute(command, (line_obj["name"],))

def load_stations(cur, data):
    command = "INSERT INTO stations(id, name, latitude, longitude) VALUES(%s, %s, %s, %s)"
    for station_obj in data["stations"]:
        keys = ["id", "name", "latitude", "longitude"]
        cur.execute(command, [station_obj[key] for key in keys])

def load_line_stations(cur, data):
    command = "INSERT INTO line_stations(line_id, station_id) VALUES(%s, %s)"
    for line_obj in data["lines"]:
        cur.execute("SELECT id FROM lines WHERE name = %s", (line_obj["name"],))
        row = cur.fetchone()
        line_id = row[0]
        for station in line_obj["stations"]:
            cur.execute(command, (line_id, station))

if __name__ == "__main__":
    conn = psycopg2.connect("postgresql://vaticle:mypassword@localhost:5432/postgres")
    try:
        cur = conn.cursor()
        create_tables(cur)
        with open("train-network.json", "r") as f:
            data = json.load(f)
        load_lines(cur, data)
        load_stations(cur, data)
        load_line_stations(cur, data)
        cur.close()
        conn.commit()
    finally:
        conn.close()