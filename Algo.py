import math
import mysql.connector
from heapq import heappush, heappop
import tkinter as tk
from tkinter import ttk, messagebox

# --- Coordinates dictionary ---
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

# --- Database functions ---
def get_flights_from_db():
    connection = mysql.connector.connect(
        host='localhost',
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

def get_blocked_routes():
    return [("Delhi", "Patna"), ("Mumbai", "Hyderabad")]

# --- Graph and distance functions ---
def haversine(c1, c2):
    R = 6371
    lat1, lon1 = c1
    lat2, lon2 = c2
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def build_graph(flights):
    blocked = set(get_blocked_routes())
    graph = {}
    for f_id, f_num, src, dst in flights:
        if src in coords and dst in coords and (src, dst) not in blocked and (dst, src) not in blocked:
            dist = haversine(coords[src], coords[dst])
            graph.setdefault(src, []).append((dst, dist))
            graph.setdefault(dst, []).append((src, dist))
    return graph

# --- Dijkstra & A* ---
def dijkstra(graph, start, goal):
    queue, visited = [(0, start, [])], set()
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

def a_star(graph, start, goal):
    queue, visited = [(0, 0, start, [])], set()
    while queue:
        f, g, city, path = heappop(queue)
        if city in visited:
            continue
        path = path + [city]
        if city == goal:
            return g, path
        visited.add(city)
        for neighbor, dist in graph.get(city, []):
            if neighbor not in visited:
                h = haversine(coords[neighbor], coords[goal])
                heappush(queue, (g + dist + h, g + dist, neighbor, path))
    return float('inf'), []

# --- Mark flights ---
def mark_flights(flights, path):
    edges = set((path[i], path[i+1]) for i in range(len(path)-1))
    blocked = set(get_blocked_routes())
    status = []
    for f_id, f_num, src, dst in flights:
        if (src, dst) in blocked or (dst, src) in blocked:
            status.append(f"{f_num}: {src} → {dst}  ❌ BLOCKED")
        elif (src, dst) in edges or (dst, src) in edges:
            status.append(f"{f_num}: {src} → {dst}  ✅ SHORTEST")
        else:
            status.append(f"{f_num}: {src} → {dst}")
    return "\n".join(status)

# --- GUI Setup ---
def find_paths():
    src = source_var.get()
    dest = dest_var.get()
    if src == dest:
        messagebox.showerror("Error", "Source and destination cannot be the same.")
        return
    if src not in coords or dest not in coords:
        messagebox.showerror("Error", "Invalid cities selected.")
        return

    flights = get_flights_from_db()
    graph = build_graph(flights)

    d_dist, d_path = dijkstra(graph, src, dest)
    a_dist, a_path = a_star(graph, src, dest)

    if d_dist == float('inf'):
        messagebox.showinfo("No Path", f"No route found from {src} to {dest}")
        return

    dijkstra_result.set(f"Dijkstra:\n{d_dist:.2f} km\nPath: {' → '.join(d_path)}")
    a_star_result.set(f"A*:\n{a_dist:.2f} km\nPath: {' → '.join(a_path)}")
    flight_output.delete(1.0, tk.END)
    flight_output.insert(tk.END, mark_flights(flights, d_path))

# GUI Window
root = tk.Tk()
root.title("Shortest Flight Path Finder")

source_var = tk.StringVar()
dest_var = tk.StringVar()
dijkstra_result = tk.StringVar()
a_star_result = tk.StringVar()

# --- Layout ---
tk.Label(root, text="Select Source City:").grid(row=0, column=0, padx=5, pady=5)
ttk.Combobox(root, textvariable=source_var, values=list(coords.keys())).grid(row=0, column=1)

tk.Label(root, text="Select Destination City:").grid(row=1, column=0, padx=5, pady=5)
ttk.Combobox(root, textvariable=dest_var, values=list(coords.keys())).grid(row=1, column=1)

tk.Button(root, text="Find Shortest Path", command=find_paths).grid(row=2, column=0, columnspan=2, pady=10)

tk.Label(root, textvariable=dijkstra_result, justify="left", fg="blue").grid(row=3, column=0, columnspan=2, sticky="w", padx=5)
tk.Label(root, textvariable=a_star_result, justify="left", fg="green").grid(row=4, column=0, columnspan=2, sticky="w", padx=5)

tk.Label(root, text="Flights Status:").grid(row=5, column=0, columnspan=2)
flight_output = tk.Text(root, width=70, height=15)
flight_output.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
