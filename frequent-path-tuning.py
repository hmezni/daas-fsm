import json
from astar import astar_search

def load_frequent_paths(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def score_path(path):
    dist=path.total_distance
    
    if not P or len(P) < 2:
        return 0

    total_distance = sum(dist(P[i], P[i + 1]) for i in range(len(P) - 1))

    total_waiting_time = sum(t_w(rs_i) for rs_i in P)

    total_cost = sum(cost(rs_i) for rs_i in P)

    score = (1 / len(P)) * (total_distance + total_waiting_time + total_cost)

    return score


def tune_frequent_paths(frequent_paths, rs_s, rs_t):
    tuned_paths = []
    for path in frequent_paths:
        for i, station in enumerate(path):
            if station_states[station] == 'overloaded':
                path[i] = astar_search(path[i-1], path[i+1])  
        if path[0] != rs_s:
            path = astar_search(rs_s, path[0]) + path
        if path[-1] != rs_t:
            path = path + astar_search(path[-1], rs_t)

        tuned_paths.append(path)

    tuned_paths = sorted(tuned_paths, key=score_path)
    return tuned_paths[0]

if __name__ == "__main__":
    frequent_paths = load_frequent_paths('frequent_paths.json')
    best_path = tune_frequent_paths(frequent_paths, 'rs_1', 'rs_7')
    print(best_path)
