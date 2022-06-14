if __name__ == "__main__":
    while True:
        query = input("Query: ")
        if len(query.split(" ")) != 2:
            print("Invalid query format")
            continue
        action, name = query.split(" ")
        if action == "line":
            stations = ["South Ruislip", "Northolt"]
            print(f"{name} line stations: {', '.join(stations)}")
        elif action == "station":
            lines = ["Piccadilly", "Metropolitan"]
            print(f"{name} station lines: {', '.join(lines)}")
        else:
            print(f"Invalid action: {action}")