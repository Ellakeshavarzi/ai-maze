import queue    #for BFS

import heapq    #for A*
import math     #for A*

def read_maze(file_path):
    with open(file_path, 'r') as f:
        maze = [list(line.strip()) for line in f.readlines()]
    return maze

def find_start_goal(maze):
    start = goal = None
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == 'S':
                start = (r, c)
            elif val == 'G':
                goal = (r, c)
    return start, goal

def bfs(maze, start, goal):
    q = queue.Queue()
    q.put(start)
    visited = {start}
    parent = {start: None}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    nodes_expanded = 0
    max_depth = 0

    while not q.empty():
        current = q.get()
        nodes_expanded += 1

        if current == goal:
            break
        for d in directions:
            nr, nc = current[0] + d[0], current[1] + d[1]
            if (0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and
                    maze[nr][nc] != '%' and (nr, nc) not in visited):
                q.put((nr, nc))
                visited.add((nr, nc))
                parent[(nr, nc)] = current
                max_depth = max(max_depth, len(parent))

    path = []
    if goal in parent:
        step = goal
        while step:
            path.append(step)
            step = parent[step]
        path.reverse()
    
    solution_cost = len(path) - 1  # start در نظر نگرفتن نود 
    return path, solution_cost, nodes_expanded, max_depth

def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def a_star(maze, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    nodes_expanded = 0
    max_depth = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        nodes_expanded += 1
        current_depth = g_score[current]

        if current == goal:
            break

        for d in directions:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if (0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and
                    maze[neighbor[0]][neighbor[1]] != '%'):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    max_depth = max(max_depth, tentative_g_score)

    path = []
    if goal in came_from:
        step = goal
        while step:
            path.append(step)
            step = came_from[step]
        path.reverse()
    
    solution_cost = len(path) - 1  # start در نظر نگرفتن نود 
    return path, solution_cost, nodes_expanded, max_depth

def print_path(maze, path):
    for r, c in path:
        if maze[r][c] not in ('S', 'G'):
            maze[r][c] = '.'
    for row in maze:
        print(''.join(row))

if __name__ == "__main__":
    maze = read_maze('input1.txt')
    start, goal = find_start_goal(maze)
    
    # BFS اجرای 
    path, solution_cost, nodes_expanded, max_depth = bfs(maze, start, goal)
    print("Path found by BFS:")
    print_path(maze, path)
    print(f"Total solution cost: {solution_cost}")
    print(f"Number of nodes expanded: {nodes_expanded}")
    print(f"Maximum depth searched: {max_depth}")
    
    print("\n" + "#" * 40 + "\n")
    

    
    # A* لود کردن دوباره ماز برای الگوریتم 
    maze = read_maze('input1.txt')
    
    # A* اجرای 
    path, solution_cost, nodes_expanded, max_depth = a_star(maze, start, goal)
    print("Path found by A*:")
    print_path(maze, path)
    print(f"Total solution cost: {solution_cost}")
    print(f"Number of nodes expanded: {nodes_expanded}")
    print(f"Maximum depth searched: {max_depth}")
