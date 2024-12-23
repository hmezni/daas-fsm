import json
import itertools

class Drone:
    def __init__(self, id, payload, speed, cost, range_capacity, reliability):
        self.id = id
        self.payload = payload
        self.speed = speed
        self.cost = cost
        self.range_capacity = range_capacity
        self.reliability = reliability

class Package:
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight

def load_drones(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        drones = [Drone(d['id'], d['payload'], d['speed'], d['cost'], d['range_capacity'], d['reliability']) for d in data['drones']]
    return drones

def max_distance(path):
    return max(path)

def filter_drones_by_range(drones, seg):
    return [d for d in drones if d.range_capacity >= seg]

def sort_drones(drones):
    return sorted(drones, key=lambda d: (-d.payload, d.speed, d.cost))

def sort_packages(packages):
    return sorted(packages, key=lambda p: p.weight)

def assign_packages(packages, drone, remaining_payload):
    if not packages:
        return []
    
    assigned_packages = []
    for pkg in packages[:]:
        if pkg.weight <= remaining_payload:
            assigned_packages.append(pkg)
            remaining_payload -= pkg.weight
            packages.remove(pkg)
    
    return assigned_packages, packages

def drone_selection(drones, packages, formation):
    if not packages:
        return formation

    drone = drones[0]
    remaining_payload = drone.payload
    assigned_packages, remaining_packages = assign_packages(packages, drone, remaining_payload)

    formation.append(drone)
    drones = drones[1:]

    return drone_selection(drones, remaining_packages, formation)

def evaluate_score(formation, path_segment, w1, w2, w3, w4):
    total_time = sum(drone.speed for drone in formation)
    total_cost = sum(drone.cost for drone in formation) * path_segment
    availability = sum(drone.reliability for drone in formation) / len(formation)
    drone_count_penalty = 1 / len(formation)

    score = (w1 * total_time) + (w2 * total_cost) + (w3 * availability) + (w4 * drone_count_penalty)
    return score

def drone_formation_selection(drones, path, packages):
    seg = max_distance(path)
    drones = filter_drones_by_range(drones, seg)
    drones = sort_drones(drones)
    packages = sort_packages(packages)

    total_drone_capacity = sum(drone.payload for drone in drones)
    total_package_weight = sum(pkg.weight for pkg in packages)

    if total_drone_capacity >= total_package_weight:
        formations = []
        for i in range(1, len(drones) + 1):
            for combination in itertools.combinations(drones, i):
                formation = []
                remaining_packages = packages.copy()
                formation = drone_selection(list(combination), remaining_packages, formation)
                formations.append(formation)

        best_score = float('inf')
        best_formation = None
        for formation in formations:
            score = evaluate_score(formation, seg)
            if score < best_score:
                best_score = score
                best_formation = formation
        
        return best_formation
    else:
        return None  


if __name__ == "__main__":
    drones = load_drones("drones.json")

    packages = [
        Package("P1", 5),
        Package("P2", 8),
        Package("P3", 3),
        Package("P4", 7)
    ]

    path = [100, 200, 150]

    best_formation = drone_formation_selection(drones, path, packages)
    if best_formation:
        print("Best Drone Formation:")
        for drone in best_formation:
            print(f"Drone {drone.id} - Payload: {drone.payload}, Speed: {drone.speed}, Cost: {drone.cost}")
    else:
        print("No valid formation found.")
