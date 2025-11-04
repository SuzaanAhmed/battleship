import random
from collections import deque

def neighbors4(x, y, size):
    for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
        nx, ny = x+dx, y+dy
        if 0 <= nx < size and 0 <= ny < size:
            yield nx, ny

def get_clanker_move(guess_board, size):
    """
    Flooding/hunt-target algorithm:
    - If there are any 'H' on guess_board, form clusters and try to extend them
      along detected orientation (horizontal/vertical). If orientation unknown,
      try orthogonal neighbors.
    - If no hits, choose a parity (checkerboard) cell for hunting (more efficient).
    """
    # list of all empty cells
    empties = [(r, c) for r in range(size) for c in range(size) if guess_board[r][c] == ' ']
    if not empties:
        return (0, 0)

    # collect hit coordinates
    hits = [(r, c) for r in range(size) for c in range(size) if guess_board[r][c] == 'H']

    # Helper to check if a cell is empty
    def is_empty(cell):
        r, c = cell
        return 0 <= r < size and 0 <= c < size and guess_board[r][c] == ' '

    # If there are hits, attempt targeted flooding
    if hits:
        visited = set()
        # Build clusters of adjacent hits (connected orthogonally)
        clusters = []
        for hit in hits:
            if hit in visited:
                continue
            # BFS/DFS to gather cluster
            q = deque([hit])
            cluster = []
            visited.add(hit)
            while q:
                cur = q.popleft()
                cluster.append(cur)
                cr, cc = cur
                for nr, nc in neighbors4(cr, cc, size):
                    if (nr, nc) in visited:
                        continue
                    if guess_board[nr][nc] == 'H':
                        visited.add((nr,nc))
                        q.append((nr,nc))
            clusters.append(cluster)

        # For each cluster, try to determine orientation and extend
        for cluster in clusters:
            if len(cluster) >= 2:
                # Determine if horizontal or vertical by comparing coords
                rows = {r for r, _ in cluster}
                cols = {c for _, c in cluster}
                if len(rows) == 1:
                    # horizontal line on row = single value
                    r = next(iter(rows))
                    ys = sorted(c for _, c in cluster)
                    left = (r, ys[0] - 1)
                    right = (r, ys[-1] + 1)
                    # prefer the side that is empty; randomize tie
                    candidates = []
                    if is_empty(left):
                        candidates.append(left)
                    if is_empty(right):
                        candidates.append(right)
                    if candidates:
                        return random.choice(candidates)
                elif len(cols) == 1:
                    # vertical line on column = single value
                    c = next(iter(cols))
                    xs = sorted(r for r, _ in cluster)
                    up = (xs[0] - 1, c)
                    down = (xs[-1] + 1, c)
                    candidates = []
                    if is_empty(up):
                        candidates.append(up)
                    if is_empty(down):
                        candidates.append(down)
                    if candidates:
                        return random.choice(candidates)
                else:
                    # Unlikely (bent cluster) — fall back to neighbor tries
                    pass

            # If cluster size == 1 or orientation unknown, try orthogonal neighbors
            for (hr, hc) in cluster:
                # try neighbors in an order: prefer continuing strategy but randomize between neighbors
                nbors = list(neighbors4(hr, hc, size))
                random.shuffle(nbors)
                for nbr in nbors:
                    if is_empty(nbr):
                        return nbr

        # If none of the clusters yielded an available extension (e.g., blocked),
        # fallback to next available empty cell (still better than pure random)
        return random.choice(empties)

    # HUNT mode (no hits): use checkerboard parity to improve odds
    # prefer cells where (r+c) % 2 == 0 (cover maximum without overlaps for ships >=2)
    parity_cells = [cell for cell in empties if (cell[0] + cell[1]) % 2 == 0]
    if parity_cells:
        return random.choice(parity_cells)
    else:
        return random.choice(empties)
