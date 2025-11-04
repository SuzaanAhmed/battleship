import random

def get_clanker_move(guess_board, size):
    available_moves = []
    for r in range(size):
        for c in range(size):
            if guess_board[r][c] == ' ':
                available_moves.append((r, c))

    if not available_moves:
        # No moves left, though game should have ended
        return (0, 0) 

    # Pick a random move from the available list
    return random.choice(available_moves)
