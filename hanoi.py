"""
Tower of Hanoi Solver Module

This module contains the core functionality for:
- Representing the Tower of Hanoi state
- Validating and executing moves
- Displaying the current state in the console
"""

from typing import List, Tuple, Dict, Literal

Tower = Literal['A', 'B', 'C']

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
        
    def is_valid_move(self, source: Tower, target: Tower) -> bool:
        """Check if a move from source tower to target tower is valid.
        
        Args:
            source (Tower): The source tower ('A', 'B', or 'C')
            target (Tower): The target tower ('A', 'B', or 'C')
            
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
    
    def move(self, source: Tower, target: Tower) -> bool:
        """Move the top disk from source tower to target tower if valid.
        
        Args:
            source (Tower): The source tower ('A', 'B', or 'C')
            target (Tower): The target tower ('A', 'B', or 'C')
            
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
    
    def is_solved(self) -> bool:
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
    
    def get_valid_moves(self):
        """Get a list of all valid moves from the current state.
        
        Returns:
            list: A list of tuples representing valid moves in the format (source, target)
        """
        valid_moves = []
        for source in self.towers:
            for target in self.towers:
                if source != target and self.is_valid_move(source, target):
                    valid_moves.append(f'source: {source}, target: {target}')
        return valid_moves
    
    def display(self) -> None:
        """Display the current state of the towers in the console."""
        print(self.display_str())

    def display_str(self) -> str:
        """Get a string visual representation of the current state of the towers.
        
        Returns:
            str: A formatted string representing the current state
        """
        lines = []
        lines.append("\n" + "=" * 40)
        lines.append(f"Tower of Hanoi - {self.num_disks} disks - Moves: {self.moves}")
        lines.append("=" * 40)
        
        max_height = self.num_disks
        
        # Display the towers row by row, from top to bottom
        for height in range(max_height, 0, -1):
            row = []
            for tower in ['A', 'B', 'C']:
                if len(self.towers[tower]) >= height:
                    disk = self.towers[tower][-height]
                    disk_str = '█' * ((disk-1) * 2) + '█'
                    padding = self.num_disks - (disk-1)
                    row.append(' ' * padding + disk_str + ' ' * padding)
                else:
                    row.append(' ' * self.num_disks + '|' + ' ' * self.num_disks)
            lines.append("  ".join(row))
        
        # Display tower bases
        bases = []
        for _ in ['A', 'B', 'C']:
            base = '▀' * (self.num_disks * 2 + 1)
            bases.append(base)
        lines.append("  ".join(bases))
        
        # Display tower labels
        labels = []
        for tower in ['A', 'B', 'C']:
            label = ' ' * self.num_disks + tower + ' ' * self.num_disks
            labels.append(label)
        lines.append("  ".join(labels))
        lines.append("\n")
        return "\n".join(lines)
        
    
    def reset(self):
        """Reset the puzzle to its initial state."""
        self.__init__(self.num_disks)
        
    def solve_recursive(
            self,
            n: int | None = None,
            source: Tower = 'A',
            auxiliary: Tower = 'B',
            target: Tower = 'C'):
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


def get_optimal_moves(num_disks: int) -> List[Tuple[Tower, Tower]]:
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
