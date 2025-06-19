"""
Tower of Hanoi Solver Module

This module contains the core functionality for:
- Representing the Tower of Hanoi state
- Validating and executing moves
- Displaying the current state in the console
"""

class TowerOfHanoi:
    def __init__(self, num_disks=3):
        """Initialize the Tower of Hanoi with a given number of disks.
        
        Args:
            num_disks (int): The number of disks to use (default: 3)
        """
        self.num_disks = num_disks
        # Initialize towers - tower A has all disks stacked in ascending order (smallest on top)
        # Towers list disks from top to bottom
        self.towers = {
            'A': list(range(1, num_disks+1)),  # [1, 2, ..., num_disks]
            'B': [],
            'C': []
        }
        self.moves = 0
        
    def is_valid_move(self, source, target):
        """Check if a move from source tower to target tower is valid.
        
        Args:
            source (str): The source tower ('A', 'B', or 'C')
            target (str): The target tower ('A', 'B', or 'C')
            
        Returns:
            bool: True if the move is valid, False otherwise
        """

        # Check if source and target are valid tower names
        if source not in self.towers or target not in self.towers:
            return False
        
        # Check if source tower has disks to move
        if not self.towers[source]:
            return False
        
        # Check if the move obeys the rule: can't place a larger disk on a smaller one
        if self.towers[target] and self.towers[source][0] > self.towers[target][0]:
            return False
            
        return True
    
    def move(self, source, target):
        """Move the top disk from source tower to target tower if valid.
        
        Args:
            source (str): The source tower ('A', 'B', or 'C')
            target (str): The target tower ('A', 'B', or 'C')
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        if self.is_valid_move(source, target):
            disk = self.towers[source][0]  # Get the top disk from source
            self.towers[target] = [disk] + self.towers[target]
            self.towers[source] = self.towers[source][1:]  # Remove the disk from source
            self.moves += 1
            print(self.towers)
            return True
            
        return False
    
    def is_solved(self):
        """Check if the puzzle is solved (all disks are on tower C).
        
        Returns:
            bool: True if solved, False otherwise
        """
        return len(self.towers['C']) == self.num_disks
    
    def get_state(self):
        """Get the current state of the towers.
        
        Returns:
            dict: A dictionary with the current state of each tower
        """
        return {
            'A': self.towers['A'].copy(),
            'B': self.towers['B'].copy(),
            'C': self.towers['C'].copy(),
            'moves': self.moves
        }
    
    def display(self):
        """Display the current state of the towers in the console."""
        print("\n" + "=" * 40)
        print(f"Tower of Hanoi - {self.num_disks} disks - Moves: {self.moves}")
        print("=" * 40)
        
        # Find the maximum height of any tower
        max_height = self.num_disks
        
        # Display the towers row by row, from top to bottom
        for height in range(max_height, 0, -1):
            row = []
            for tower in ['A', 'B', 'C']:
                if len(self.towers[tower]) >= height:
                    disk = self.towers[tower][-height]
                    disk_str = '█' * ((disk-1) * 2) + '█'
                    # Pad with spaces to ensure alignment
                    padding = self.num_disks - (disk-1)
                    row.append(' ' * padding + disk_str + ' ' * padding)
                else:
                    # Empty space with pole indicator
                    row.append(' ' * self.num_disks + '|' + ' ' * self.num_disks)
            print("  ".join(row))
            
        # Display tower bases
        bases = []
        for _ in ['A', 'B', 'C']:
            base = '▀' * (self.num_disks * 2 + 1)
            bases.append(base)
        print("  ".join(bases))
        
        # Display tower labels
        labels = []
        for tower in ['A', 'B', 'C']:
            label = ' ' * self.num_disks + tower + ' ' * self.num_disks
            labels.append(label)
        print("  ".join(labels))
        print("\n")
    
    def reset(self):
        """Reset the puzzle to its initial state."""
        self.__init__(self.num_disks)
        
    def solve_recursive(self, n=None, source='A', auxiliary='B', target='C'):
        """Recursive solution for Tower of Hanoi puzzle.
        
        Args:
            n (int): Number of disks to move (default: all disks)
            source (str): Source tower (default: 'A')
            auxiliary (str): Auxiliary tower (default: 'B')
            target (str): Target tower (default: 'C')
            
        Returns:
            list: List of moves in the format ('source', 'target')
        """
        if n is None:
            n = self.num_disks
            
        moves = []
        if n == 1:
            moves.append((source, target))
        else:
            # Move n-1 disks from source to auxiliary using target as auxiliary
            moves.extend(self.solve_recursive(n-1, source, target, auxiliary))
            # Move the largest disk from source to target
            moves.append((source, target))
            # Move n-1 disks from auxiliary to target using source as auxiliary
            moves.extend(self.solve_recursive(n-1, auxiliary, source, target))
        return moves


def get_optimal_moves(num_disks):
    """Get the optimal sequence of moves for solving Tower of Hanoi.
    
    Args:
        num_disks (int): Number of disks in the puzzle
        
    Returns:
        list: List of moves in the format [('source', 'target'), ...]
    """
    hanoi = TowerOfHanoi(num_disks)
    return hanoi.solve_recursive()


if __name__ == "__main__":
    # Simple demo of the Tower of Hanoi
    game = TowerOfHanoi(3)
    game.display()
    
    # Manual moves example
    moves = [('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')]
    
    for source, target in moves:
        if game.move(source, target):
            print(f"Moved disk from {source} to {target}")
            game.display()
        else:
            print(f"Invalid move: {source} to {target}")
    
    if game.is_solved():
        print("Puzzle solved!")
    else:
        print("Puzzle not yet solved.")
