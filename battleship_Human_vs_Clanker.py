import random
import time
import importlib
import os

'''
VERY IMPORTANT:
This code is the interface for moves from both Human and clanker and processeswhich is correct.
However, the algorithm for clanker is in a different file to be imported.
The reason for this design is to create multiple files of different algorithms to be able to alternate and pklay with each.
So the algorithm will be imported from other files.
'''

class BTS:
    def __init__(self,clanker_module,size=10):
        self.size=size

        self.ships={
            "Biggest Ship":5,
            "Sub-Big Ship":4,
            "Mid Ship":3,
            "Sub mid ship":2,
            "Tiny Ship":1
        }

        # self.MainShip=5
        # self.SubShip=3
        # self.TinyShip=1

        # self.MainShipTest=False
        # self.SubShipTest=False
        # self.TinyShipTest=False
        self.total_ship_cells = sum(self.ships.values())

        """Below is what either side sees their board as"""
        self.player_board = self.create_board()
        self.clanker_board = self.create_board()

        """Below is what either side sees the others board as"""
        self.player_guess_board = self.create_board()
        self.clanker_guess_board = self.create_board()
        self.clanker_move_function = None
        self.import_clanker(clanker_module)

    def import_clanker(self, clanker_module):
        """Dynamically imports the clanker module and gets its move function."""

        if clanker_module.endswith(".py"):
            clanker_module = clanker_module[:-3]
            
        print(f"Fecthing clanker algo from {clanker_module}.py")
        # Use importlib to load the module
        clanker_mod = importlib.import_module(clanker_module)
        
        # Get the required function from the loaded module
        self.clanker_move_function = getattr(clanker_mod, 'get_clanker_move')
        print("clanker algo imported.")

    def create_board(self):
        return [[' ' for _ in range(self.size)] for _ in range(self.size)]

    def print_boards(self):
        """Decided to print out both boards"""
        print("\n" + "="*53)
        print("     PLAYER'S GUESSES                  YOUR BOARD ")
        header = "   " + " ".join([f"{i}" for i in range(self.size)])
        print(header + "        " + header)
        print("   " + "-"*(self.size*2+1) + "        " + "   " + "-"*(self.size*2+1))
        
        for i in range(self.size):
            row_guess = " ".join(self.player_guess_board[i]) 
            row_own = " ".join(self.player_board[i])
            print(f"{i:1} | {row_guess} |      {i:1} | {row_own} |")
        
        print("   " + "-"*(self.size*2+1) + "        " + "  " + "-"*(self.size*2+1))
        print("Legend: 'S' = Your Ship, 'H' = Hit, 'M' = Miss, 'X' = Sunk Ship Part")

    def is_valid_placement(self, board, ship_size, x, y, orientation):
        """Just to clarify no placements are done here, only validity is checked
           Checks if a ship can be placed at the given location."""
        if orientation == 'h':
            if y + ship_size > self.size:
                return False
            for i in range(ship_size):
                if board[x][y+i] != ' ':
                    return False
        else: #'v'
            if x + ship_size > self.size:
                return False
            for i in range(ship_size):
                if board[x+i][y] != ' ':
                    return False
        return True

    def place_ship_on_board(self, board, ship_size, x, y, orientation, ship_char='S'):
        """Actually places ship as wanted by the person or a clanker
           Post validity checks"""
        if orientation == 'h':
            for i in range(ship_size):
                board[x][y+i] = ship_char
        else: # 'v'
            for i in range(ship_size):
                board[x+i][y] = ship_char

    def choose_Pos(self):
        """Allows the player to interactively place their ships."""
        print("\n--- Place Your Ships ---")
        for ship_name, ship_length in self.ships.items():
            while True:
                self.print_boards()
                print(f"Placing {ship_name} (length {ship_length})")
                
                try:
                    pos = input(f"Enter start coordinate (row,col) (e.g., 3,4): ")
                    x, y = map(int, pos.split(','))
                    
                    orientation = input("Enter orientation (h for horizontal, v for vertical): ").lower()
                    if orientation not in ['h', 'v']:
                        raise ValueError("Invalid orientation.")
                    
                    if self.is_valid_placement(self.player_board, ship_length, x, y, orientation):
                        self.place_ship_on_board(self.player_board, ship_length, x, y, orientation)
                        break
                    else:
                        print("Invalid placement. Ship is out of bounds or overlaps another ship. Try again.")
                
                except ValueError as e:
                    print(f"Invalid input ({e}). Please use the format 'row,col' and 'h' or 'v'.")
                except IndexError:
                     print("Invalid coordinates. Please enter numbers between 0 and 9.")
 
    def place_ships_clanker(self):
        """Clanker places ships"""
        print("\nClanker placing ships")
        #time.sleep(5)
        for _, ship_length in self.ships.items():
            while True:
                orientation = random.choice(['h', 'v'])
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                
                if self.is_valid_placement(self.clanker_board, ship_length, x, y, orientation):
                    self.place_ship_on_board(self.clanker_board, ship_length, x, y, orientation)
                    break # Move to the next ship

    def get_player_guess(self):
            """Validity of guess"""
            while True:
                try:
                    pos = input("Enter your guess (row,col): ")
                    x, y = map(int, pos.split(','))
                    
                    if not (0 <= x < self.size and 0 <= y < self.size):
                        print("Coordinates out of bounds. Try again.")
                    elif self.player_guess_board[x][y] != ' ':
                        print("You've already guessed that spot. Try again.")
                    else:
                        return x, y
                except ValueError:
                    print("Invalid input. Please use the format 'row,col'.")

    def process_player_guess(self, x, y):
        """Checks whether its correct guess i.e. 'Hit' or 'Miss'"""
        target = self.clanker_board[x][y]
        
        if target == 'S':
            print(">>> HIT!")
            self.player_guess_board[x][y] = 'H'
            self.clanker_board[x][y] = 'H' # Mark on clanker's board as hit
        else:
            print(">>> MISS!")
            self.player_guess_board[x][y] = 'M'

    def process_clanker_guess(self, x, y):
        """clanker moves processing"""
        print(f"clanker guesses: ({x}, {y})")
        target = self.player_board[x][y]
        
        self.clanker_guess_board[x][y] = 'M' 
        
        if target == 'S':
            print(">>> clanker HIT your ship!")
            self.player_board[x][y] = 'H'
            self.clanker_guess_board[x][y] = 'H' 
        else:
            print(">>> clanker missed.")

    def check_game_over(self):
        """whether either of their ships have been destroyed"""
        player_hits = sum(row.count('H') for row in self.player_guess_board)
        if player_hits == self.total_ship_cells:
            print("\n" + "="*30)
            print("Hooray! YOU WIN! All clanker ships sunk!")
            print("="*30)
            return True
            
        clanker_hits = sum(row.count('H') for row in self.player_board)
        if clanker_hits == self.total_ship_cells:
            print("\n" + "="*30)
            print("Oh no! The clanker sunk all your ships! clanker WINS!")
            print("="*30)
            return True
            
        return False

    def play_game(self):
        print("Battleship gameplay")
        self.choose_Pos()
        self.place_ships_clanker()

        while True:
            self.print_boards()
            
            # --- Player's Turn ---
            print("\n--- Your Turn ---")
            px, py = self.get_player_guess()
            self.process_player_guess(px, py)
            if self.check_game_over():
                break
        
            # --- clanker's Turn ---
            print("\n--- clanker's Turn ---")
            # This is the key part: call the imported function
            # We pass it the clanker's "memory" (guess board) and the board size
            try:
                ax, ay = self.clanker_move_function(self.clanker_guess_board, self.size)
                self.process_clanker_guess(ax, ay)
            except Exception as e:
                print(f"ERROR during clanker move: {e}")
                print("clanker forfeits turn.")

            if self.check_game_over():
                break
            
            input("Press Enter to continue to the next turn...")
                

if __name__=="__main__":
    clanker_file = "battleship_clanker_simple" 

    bts=BTS(clanker_module=clanker_file)
    bts.play_game()