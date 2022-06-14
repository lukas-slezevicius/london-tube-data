import psycopg2

DSN = "postgresql://vaticle:mypassword@localhost:5432/postgres"

def get_stations(cur, line):
    cur.execute("SELECT id FROM lines WHERE name = %s", (line,))
    rows = cur.fetchall()
    line_ids = [row[0] for row in rows]
    for line_id in line_ids:
        station_ids = []
        cur.execute("SELECT station_id FROM line_stations WHERE line_id = %s", (line_id,))
        rows = cur.fetchall()
        for station_id, *_ in rows:
            station_ids.append(station_id)
        yield station_ids

def get_lines(cur, station):
    cur.execute("SELECT id FROM stations WHERE name = %s", (station,))
    row = cur.fetchone()
    if row is None:
        return []
    station_id = row[0]
    cur.execute("SELECT line_id FROM line_stations WHERE station_id = %s", (station_id,))
    rows = cur.fetchall()
    line_names = []
    for line_id, *_ in rows:
        cur.execute("SELECT name FROM lines WHERE id = %s", (line_id,))
        row = cur.fetchone()
        line_names.append(row[0])
    return line_names

if __name__ == "__main__":
    conn = psycopg2.connect(DSN)
    try:
        cur = conn.cursor()
        while True:
            query = input("Query: ").strip()
            if len(query.split(" ")) < 2:
                print("Invalid query format")
                continue
            action, *name_tokens = query.split(" ")
            name = " ".join(name_tokens)
            if action == "line":
                for stations in get_stations(cur, name):
                    print(f"{name} line stations: {', '.join(stations)}")
            elif action == "station":
                lines = get_lines(cur, name)
                if len(lines) > 0:
                    print(f"{name} station lines: {', '.join(lines)}")
                else:
                    print(f"{name} station has no lines")
            else:
                print(f"Invalid action: {action}")
    finally:
        conn.close()