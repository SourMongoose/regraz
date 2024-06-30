from heapq import heappush, heappop

# a* algorithm to calculate shortest path between two layouts
def get_path(start, end):
    rows = len(start)
    cols = len(start[0])

    heap = []
    visited = set()
    parent = {}

    end_coords = {}
    for i in range(rows):
        for j in range(cols):
            end_coords[end[i][j]] = (i, j)

    # manhattan distance as heuristic
    def h(state):
        total_dist = 0
        for i in range(rows):
            for j in range(cols):
                num = state[i][j]
                if num != 0:
                    total_dist += abs(i - end_coords[num][0]) + abs(j - end_coords[num][1])
        return total_dist

    heappush(heap, (h(start), 0, start))
    visited.add(start)
    parent[start] = None

    while heap:
        _, dist, curr = heappop(heap)

        if curr == end:
            path = []
            while curr:
                path.append(curr)
                curr = parent[curr]
            return path[::-1]

        zeros = []
        for i in range(rows):
            for j in range(cols):
                if curr[i][j] == 0:
                    zeros.append((i,j))

        for zero in zeros:
            r, c = zero[0], zero[1]
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    new_state = [list(row) for row in curr]
                    new_state[nr][nc], new_state[r][c] = new_state[r][c], new_state[nr][nc]
                    new_state = tuple(tuple(row) for row in new_state)

                    if new_state not in visited:
                        visited.add(new_state)
                        parent[new_state] = curr
                        heappush(heap, (dist+1+h(new_state), dist+1, new_state))

    return -1

def get_path_steps(start, end, steps):
    path = get_path(start, end)
    if path == -1:
        return -1

    dist = len(path)-1
    if steps < dist or (steps - dist) % 2 == 1:
        return -1

    # repeat the last two steps until you reach desired length
    while len(path) - 1 < steps:
        path.extend(path[-2:])

    return path

if __name__ == '__main__':
    path = get_path(((2,3,0),(1,6,7),(5,4,8)), ((1,4,3),(2,0,6),(7,5,8)))
    print(path)
    if path != -1:
        print(len(path))
