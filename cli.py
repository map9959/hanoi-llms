"""
Command Line Interface for Tower of Hanoi Solver

This module provides a CLI for the Tower of Hanoi solver, allowing users to:
- Play the game manually
- Watch the AI solve the puzzle
- Compare different solving approaches
"""

import argparse
import time
from hanoi import TowerOfHanoi, get_optimal_moves
from openai_solver import OpenAIHanoiSolver

def manual_play(num_disks):
    """Allow the user to manually solve the Tower of Hanoi puzzle.
    
    Args:
        num_disks (int): Number of disks in the puzzle
    """
    game = TowerOfHanoi(num_disks)
    game.display()
    
    while not game.is_solved():
        print("Enter your move (e.g., 'A C' to move from A to C, or 'q' to quit):")
        user_input = input("> ").strip().upper()
        
        if user_input == 'Q':
            print("Exiting game.")
            return
        
        try:
            source, target = user_input.split()
            if source not in ['A', 'B', 'C'] or target not in ['A', 'B', 'C']:
                print("Invalid towers. Please use A, B, or C.")
                continue
                
            if game.move(source, target):
                game.display()
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter source and target towers separated by a space.")
    
    print(f"Congratulations! You solved the puzzle in {game.moves} moves.")
    print(f"The minimum possible moves for {num_disks} disks is {2**num_disks - 1}.")

def ai_solve(num_disks, model="gpt-4.1-mini", max_iterations=100):
    """Have the AI solve the Tower of Hanoi puzzle.
    
    Args:
        num_disks (int): Number of disks in the puzzle
        model (str): The OpenAI model to use
        max_iterations (int): Maximum number of iterations to attempt
    """
    solver = OpenAIHanoiSolver(num_disks=num_disks, model=model)
    print(f"AI attempting to solve {num_disks}-disk Tower of Hanoi puzzle...")
    
    start_time = time.time()
    solved = solver.solve(max_iterations=max_iterations)
    elapsed_time = time.time() - start_time
    
    if solved:
        print(f"AI solved the puzzle in {solver.game.moves} moves and {elapsed_time:.2f} seconds.")
        print(f"The optimal solution requires {2**num_disks - 1} moves.")
    else:
        print(f"AI failed to solve the puzzle in {max_iterations} iterations.")

def algorithm_solve(num_disks):
    """Solve the Tower of Hanoi puzzle using the recursive algorithm.
    
    Args:
        num_disks (int): Number of disks in the puzzle
    """
    game = TowerOfHanoi(num_disks)
    print(f"Solving {num_disks}-disk Tower of Hanoi puzzle with recursive algorithm...")
    game.display()
    
    # Get the optimal sequence of moves
    moves = get_optimal_moves(num_disks)
    
    for i, (source, target) in enumerate(moves):
        print(f"Move {i+1}: {source} → {target}")
        game.move(source, target)
        game.display()
        time.sleep(0.5)  # Slow down to make it visible
    
    print(f"Puzzle solved in {len(moves)} moves (optimal).")

def compare_methods(num_disks, model="gpt-4.1-mini", max_iterations=100):
    """Compare different methods for solving the Tower of Hanoi puzzle.
    
    Args:
        num_disks (int): Number of disks in the puzzle
        model (str): The OpenAI model to use
        max_iterations (int): Maximum number of iterations to attempt
    """
    # Optimal number of moves
    optimal_moves = 2**num_disks - 1
    print(f"Comparing methods for solving {num_disks}-disk Tower of Hanoi puzzle...")
    print(f"Optimal solution requires {optimal_moves} moves.\n")
    
    # Algorithm solution
    moves = get_optimal_moves(num_disks)
    algorithm_moves = len(moves)
    print(f"Algorithm solution: {algorithm_moves} moves (optimal)\n")
    
    # OpenAI API solution
    print("OpenAI API solution:")
    solver = OpenAIHanoiSolver(num_disks=num_disks, model=model, verbose=False)
    start_time = time.time()
    solved = solver.solve(max_iterations=max_iterations)
    elapsed_time = time.time() - start_time
    
    if solved:
        openai_moves = solver.game.moves
        efficiency = optimal_moves / openai_moves if openai_moves > 0 else 0
        print(f"  - Moves: {openai_moves} (Efficiency: {efficiency:.2%})")
        print(f"  - Time taken: {elapsed_time:.2f} seconds")
    else:
        print("  - Failed to solve the puzzle")
    
    print("\nComparison complete.")

def main():
    """Main function for the CLI."""
    parser = argparse.ArgumentParser(description="Tower of Hanoi Solver")
    parser.add_argument("--mode", type=str, choices=["manual", "ai", "algorithm", "compare"], 
                      default="manual", help="Mode of operation")
    parser.add_argument("--disks", type=int, default=3, 
                      help="Number of disks (default: 3)")
    parser.add_argument("--model", type=str, default="gpt-4.1-mini", 
                      help="OpenAI model to use (default: gpt-4.1-mini)")
    parser.add_argument("--iterations", type=int, default=100, 
                      help="Maximum iterations for AI solver (default: 100)")
    
    args = parser.parse_args()
    
    # Validate number of disks
    if args.disks < 1:
        print("Number of disks must be at least 1.")
        return
    
    # Run the selected mode
    if args.mode == "manual":
        manual_play(args.disks)
    elif args.mode == "ai":
        ai_solve(args.disks, args.model, args.iterations)
    elif args.mode == "algorithm":
        algorithm_solve(args.disks)
    elif args.mode == "compare":
        compare_methods(args.disks, args.model, args.iterations)


if __name__ == "__main__":
    main()
