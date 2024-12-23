import json
from collections import defaultdict

def load_flight_history(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def dfs_code(path, graph):
    
    visited = set()  
    dfs_result = []  

    def dfs(vertex):
        if vertex not in visited:
            visited.add(vertex)
            dfs_result.append(vertex)
            
            for neighbor in graph.get(vertex, []):
                if neighbor not in visited:
                    dfs(neighbor)

    for v in path:
        if v not in visited:
            dfs(v)

    return dfs_result


def frequent_path_mining(flight_history, theta):
    frequent_paths = set()
    dfs_codes = []
    
    for path in flight_history:
        sub_paths = extract_edge_disjoint_subpaths(path)
        for sub_path in sub_paths:
            code = dfs_code(sub_path)
            dfs_codes.append(code)
    
    dfs_codes.sort()  
    for code in dfs_codes:
        if dfs_search(code, flight_history, theta):
            frequent_paths.add(code)
    
    with open("frequent_paths.json", "w") as f:
        json.dump(list(frequent_paths), f)
    
    return frequent_paths

def extract_edge_disjoint_subpaths(path):
    
    if not path or len(path) < 2:
        return []
    
    sub_paths = []
    current_subpath = [path[0]]  
    
    for i in range(1, len(path)):
        current_subpath.append(path[i])
        
        if path[i] in current_subpath[:-1]:  
            sub_paths.append(current_subpath[:-1])  
            current_subpath = [path[i - 1], path[i]]
    
    if current_subpath:
        sub_paths.append(current_subpath)
    
    return sub_paths


def dfs_search(code, flight_history, theta):
    sup = sum(1 for path in flight_history if code in path) / len(flight_history)
    return sup >= theta

if __name__ == "__main__":
    flight_history = load_flight_history('flight_history.json')
    theta = 0.5  
    frequent_paths = frequent_path_mining(flight_history, theta)
    print(frequent_paths)
