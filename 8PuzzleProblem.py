import copy
import heapq

class Puzzle8:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def heuristic(self, state):
        """
        Calculate the heuristic (Manhattan distance) for the state.
        """
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:  # Ignore empty tile
                    x, y = divmod(self.goal.index(state[i][j]), 3)
                    distance += abs(x - i) + abs(y - j)
        return distance

    def find_zero(self, state):
        """
        Find the position of the empty tile (0).
        """
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j

    def get_neighbors(self, state):
        """
        Generate all possible states from the current state.
        """
        neighbors = []
        x, y = self.find_zero(state)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(new_state)
        return neighbors

    def hill_climbing(self):
        """
        Perform the Hill Climbing algorithm to solve the puzzle.
        """
        current_state = self.initial
        current_heuristic = self.heuristic(current_state)
        path = [current_state]
        
        while True:
            neighbors = self.get_neighbors(current_state)
            best_neighbor = None
            best_heuristic = float('inf')

            for neighbor in neighbors:
                h = self.heuristic(neighbor)
                if h < best_heuristic:
                    best_heuristic = h
                    best_neighbor = neighbor
            
            # If no better neighbor is found, return current state (local maximum/minimum)
            if best_heuristic >= current_heuristic:
                break

            # Move to the best neighbor
            current_state = best_neighbor
            current_heuristic = best_heuristic
            path.append(current_state)

        return path, current_heuristic

    def print_state(self, state):
        for row in state:
            print(" ".join(map(str, row)))
        print()

# Example initial and goal states
initial_state = [[1, 2, 3],
                 [4, 0, 5],
                 [7, 8, 6]]

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

# Flatten goal state for heuristic calculation
goal_flat = [item for row in goal_state for item in row]

# Initialize and solve
puzzle = Puzzle8(initial_state, goal_flat)
path, heuristic = puzzle.hill_climbing()

# Output the steps
print("Steps to solve the puzzle:")
for step in path:
    puzzle.print_state(step)

print(f"Final Heuristic Value: {heuristic}")
