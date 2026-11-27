"""Optional AL08 starter: model Monday, traversals Tuesday, routes Thursday."""

from collections import deque
from network_support import validate_request, record_step
from app_runner import run

STAGE = 2  # Monday 1; Tuesday 2 when traversals work; Thursday 3 when routes work.
MY_RESTRICTION = "A"  # Set this to your instructor-issued case in your personal copy.


# MONDAY — Inspect the supplied model and test copies with a connection mistake.
# No traversal is required for STAGE 1; keep your brief personal model notes.


# TUESDAY — Complete each algorithm separately on the fresh common fixture.
def breadth_first(graph, start):
    """Return BFS order, independent snapshots, and adjacency entries examined."""
    validate_request(graph, start)
    # Queue the start and mark it discovered.
    queue = deque([start])
    discovered = {start}
    # Track visit order, snapshots, and examined adjacency entries.
    order = []
    trace = []
    edges_examined = 0

    # Process the queue and inspect neighbors in listed order.
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            edges_examined += 1
            if neighbor not in discovered:
                # Mark each neighbor before queueing it.
                discovered.add(neighbor)
                queue.append(neighbor)
        # Save state after handling this node's neighbors.
        record_step(trace, node, queue, discovered)

    return order, trace, edges_examined


def depth_first(graph, start):
    """Return iterative DFS order, independent snapshots, and adjacency count."""
    validate_request(graph, start)
    # Start with a stack and mark nodes when they are processed.
    stack = [start]
    visited = set()
    # Track visit order, snapshots, and examined adjacency entries.
    order = []
    trace = []
    edges_examined = 0

    # Process the stack, skipping nodes already visited.
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        # Reverse neighbors so the first listed available one is next.
        for neighbor in reversed(graph[node]):
            edges_examined += 1
            if neighbor not in visited:
                stack.append(neighbor)
        # Save state after handling this node's neighbors.
        record_step(trace, node, stack, visited)

    return order, trace, edges_examined


# THURSDAY — Save parents during BFS, then follow one chain backward.
def reconstruct_path(parents, goal):
    """Return start-to-goal order by following the BFS parent chain."""
    # Walk from goal to start by following the parent chain, collecting node names.
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parents.get(node)
    
    # Reverse to get start-to-goal order and preserve the input parents dictionary.
    path.reverse()
    return path


def shortest_hop_path(graph, start, goal, blocked=()):
    """Return a permitted fewest-hop path and parents, or None with parent state."""
    blocked_nodes = set(blocked)
    validate_request(graph, start, goal, blocked_nodes)
    
    # Return None immediately if start or goal is blocked.
    if start in blocked_nodes or goal in blocked_nodes:
        return None, {}
    
    # Initialize parents dictionary; start has no parent, and the BFS queue begins with the start node.
    parents = {start: None}
    queue = deque([start])
    
    # Perform BFS, tracking each node's parent and stopping when goal is found.
    while queue:
        node = queue.popleft()
        
        # Check if we have reached the goal; reconstruct and return the path.
        if node == goal:
            path = reconstruct_path(parents, goal)
            return path, parents
        
        # For each neighbor not yet visited (and not blocked), record parent and queue it.
        for neighbor in graph[node]:
            if neighbor not in parents and neighbor not in blocked_nodes:
                parents[neighbor] = node
                queue.append(neighbor)
    
    # If the queue is empty and the goal has not been found, return None and all discovered parents.
    return None, parents


def main():
    """Run only the selected completed stage using supplied presentation."""
    run(STAGE, breadth_first, depth_first, shortest_hop_path, MY_RESTRICTION)


if __name__ == "__main__":
    main()