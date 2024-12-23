if __name__ == "__main__":
    
    charging_history = load_charging_history('charging_history.json')
    threshold = 0.7
    station_states = predict_resource_usage(charging_history, threshold)
    
    flight_history = load_flight_history('flight_history.json')
    theta = 0.5
    frequent_paths = frequent_path_mining(flight_history, theta)
    
    best_path = tune_frequent_paths(frequent_paths, station_states, 'station_1', 'station_2')
    
    drones = load_drones('drones.json')
    packages = [{'item': 'item_1', 'weight': 5}, {'item': 'item_2', 'weight': 15}]
    best_drones = drone_selection(best_path, drones, packages)
    
    print(f"Best Delivery Path: {best_path}")
    print(f"Best Drone Composition: {best_drones}")
