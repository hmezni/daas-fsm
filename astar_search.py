
import heapq

def astar_search(graph, start, goal, heuristic):
    """
    Perform A* search algorithm to find the shortest path from start to goal.

    :param graph: Dictionary where keys are vertices and values are lists of tuples (neighbor, cost)
    :param start: The starting node
    :param goal: The goal node
    :param heuristic: A function that estimates the cost from a node to the goal
    :return: Tuple containing the shortest path and its cost
    """
    # Priority queue for A* frontier, stores (cost, node, path)
    frontier = [(0, start, [start])]
    heapq.heapify(frontier)

    # Dictionary to store the best cost to reach each node
    cost_so_far = {start: 0}

    while frontier:
        # Get the node with the lowest estimated cost
        current_cost, current_node, path = heapq.heappop(frontier)

        # If we reached the goal, return the path and the cost
        if current_node == goal:
            return path, current_cost

        # Explore neighbors
        for neighbor, edge_cost in graph[current_node]:
            new_cost = current_cost + edge_cost
            # If this path to the neighbor is better, update the cost and add to the frontier
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor, path + [neighbor]))

    return None, float('inf')  # No path found


# Example heuristic function (Manhattan distance for grid-like graphs)
def manhattan_heuristic(node, goal):
    (x1, y1) = node
    (x2, y2) = goal
    return abs(x1 - x2) + abs(y1 - y2)
