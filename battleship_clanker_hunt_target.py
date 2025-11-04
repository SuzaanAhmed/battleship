import random

# Internal memory for the AI (persistent across turns)
memory = {
    "mode": "hunt",          # "hunt" or "target"
    "last_hits": [],         # List of cells where hits occurred
    "potential_targets": []  # Next coordinates to try
}

def get_clanker_move(guess_board, size):
    """
    Smart AI that alternates between:
    - HUNT mode: Randomly search for ships
    - TARGET mode: Once a hit is found, systematically target nearby cells
    """
    global memory

    # --- Utility functions ---
    def get_neighbors(x, y):
        """Return valid neighboring cells (up, down, left, right)."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and guess_board[nx][ny] == ' ':
                neighbors.append((nx, ny))
        return neighbors

    # --- Update mode if necessary ---
    # If we are in target mode but no more hits remain, go back to hunt
    if memory["mode"] == "target" and not memory["last_hits"]:
        memory["mode"] = "hunt"
        memory["potential_targets"] = []

    # --- Target Mode: systematically finish off a ship ---
    if memory["mode"] == "target" and memory["potential_targets"]:
        move = memory["potential_targets"].pop(0)
        return move

    # --- Check for new hits on the board to update AI memory ---
    for r in range(size):
        for c in range(size):
            if guess_board[r][c] == 'H' and (r, c) not in memory["last_hits"]:
                # Found a new hit on the board
                memory["last_hits"].append((r, c))
                memory["mode"] = "target"
                memory["potential_targets"].extend(get_neighbors(r, c))

    # --- If target mode has potential moves, use them first ---
    if memory["mode"] == "target" and memory["potential_targets"]:
        return memory["potential_targets"].pop(0)

    # --- Hunt Mode: pick random empty cell ---
    available_moves = [
        (r, c)
        for r in range(size)
        for c in range(size)
        if guess_board[r][c] == ' '
    ]

    if not available_moves:
        return (0, 0)  # Safety fallback

    move = random.choice(available_moves)
    return move
