import math
import sys
import mysql.connector
from heapq import heappush, heappop

# City coordinates dictionary
coords = {
    "Ahmedabad": (23.0225, 72.5714),
    "Amritsar": (31.6340, 74.8723),
    "Bangalore": (12.9716, 77.5946),
    "Delhi": (28.7041, 77.1025),
    "Patna": (25.5941, 85.1376),
    "Bhubaneshwar": (20.2961, 85.8245),
    "Chennai": (13.0827, 80.2707),
    "Goa": (15.2993, 74.1240),
    "Varanasi": (25.3176, 82.9739),
    "Hyderabad": (17.3850, 78.4867),
    "Indore": (22.7196, 75.8577),
    "Jaipur": (26.9124, 75.7873),
    "Kolkata": (22.5726, 88.3639),
    "Lucknow": (26.8467, 80.9462),
    "Mumbai": (19.0760, 72.8777),
    "Nagpur": (21.1458, 79.0882),
    "Pune": (18.5204, 73.8567),
    "Raipur": (21.2514, 81.6296),
    "Dehradun": (30.3165, 78.0322)
}

# Connect to MySQL database
def get_flights_from_db():
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='srishtihello',
        database='SBPsystem'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT f_code, f_name, source, destination FROM flight")
    flights = cursor.fetchall()
    cursor.close()
    connection.close()
    return flights

# Define blocked routes (no-fly zones or bad weather)
def get_blocked_routes():
    # Format: list of (source, destination)
    return [
        ("Delhi", "Patna"),           # Example no-fly zone
        ("Mumbai", "Hyderabad")       # Example bad weather
    ]

# Haversine distance between coordinates
def haversine(c1, c2):
    R = 6371
    lat1, lon1 = c1
    lat2, lon2 = c2
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Build graph excluding blocked routes
def build_graph(flights):
    blocked = set(get_blocked_routes())
    graph = {}
    for f_id, f_num, src, dst in flights:
        if src in coords and dst in coords:
            if (src, dst) in blocked or (dst, src) in blocked:
                continue  # Skip blocked routes
            dist = haversine(coords[src], coords[dst])
            graph.setdefault(src, []).append((dst, dist))
            graph.setdefault(dst, []).append((src, dist))
    return graph

# Dijkstra's algorithm
def dijkstra(graph, start, goal):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        dist, city, path = heappop(queue)
        if city in visited:
            continue
        path = path + [city]
        if city == goal:
            return dist, path
        visited.add(city)
        for neighbor, weight in graph.get(city, []):
            if neighbor not in visited:
                heappush(queue, (dist + weight, neighbor, path))
    return float('inf'), []

# A* algorithm
def a_star(graph, start, goal):
    queue = [(0, 0, start, [])]
    visited = set()
    while queue:
        f_score, g_score, city, path = heappop(queue)
        if city in visited:
            continue
        path = path + [city]
        if city == goal:
            return g_score, path
        visited.add(city)
        for neighbor, dist in graph.get(city, []):
            if neighbor not in visited:
                h = haversine(coords[neighbor], coords[goal])
                heappush(queue, (g_score + dist + h, g_score + dist, neighbor, path))
    return float('inf'), []

# Mark and print flights in the shortest path
def mark_shortest_flights(flights, shortest_path):
    path_edges = set((shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path) - 1))
    blocked = set(get_blocked_routes())
    
    for flight_id, flight_num, src, dst in flights:
        if (src, dst) in blocked or (dst, src) in blocked:
            print(f"{flight_num} from {src} to {dst}  blocked (obstacle)")
        elif (src, dst) in path_edges or (dst, src) in path_edges:
            print(f"{flight_num} from {src} to {dst}  shortest")
        else:
            print(f"{flight_num} from {src} to {dst}")

# Main logic
def main():
    flights = get_flights_from_db()
    graph = build_graph(flights)

    src = input("Enter source city: ").strip()
    dest = input("Enter destination city: ").strip()

    if src not in coords or dest not in coords:
        print("Error: Source or destination city coordinates not found.")
        return

    dist, path = dijkstra(graph, src, dest)
    if dist == float('inf'):
        print(f"No path found from {src} to {dest} using Dijkstra.")
        return

    print(f"\nShortest distance by Dijkstra: {dist:.2f} km")
    print("Shortest path:", " -> ".join(path))
    print("\nFlights status:")
    mark_shortest_flights(flights, path)

    dist_a, path_a = a_star(graph, src, dest)
    print(f"\nShortest distance by A*: {dist_a:.2f} km")
    print("Shortest path:", " -> ".join(path_a))

# Support command-line usage
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        src = sys.argv[1]
        dest = sys.argv[2]
        flights = get_flights_from_db()
        graph = build_graph(flights)
        dist, path = dijkstra(graph, src, dest)
        if dist == float('inf'):
            print(f"No path from {src} to {dest}")
        else:
            print(f"Shortest distance: {dist:.2f} km")
            print(" -> ".join(path))
    else:
        main()
