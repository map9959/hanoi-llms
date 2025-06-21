"""
OpenAI API Integration for Tower of Hanoi Solver

This module provides the integration with OpenAI's API to solve the Tower of Hanoi
puzzle using tool-calling capabilities.
"""

import os
import json
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
from openai import OpenAI
from hanoi import TowerOfHanoi

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TowerOfHanoiMove(BaseModel):
    """A move in the Tower of Hanoi puzzle"""
    
    #reasoning: str = Field(description="Think about what move to make next and whether it's valid")
    source: Literal["A", "B", "C"] = Field(description="Tower to move the top disk from (A, B, or C)")
    target: Literal["A", "B", "C"] = Field(description="Tower to move the top disk to (A, B, or C)")
    


class OpenAIHanoiSolver:
    def __init__(self, num_disks=3, model="gpt-4.1", verbose=True):
        """Initialize the OpenAI-powered Tower of Hanoi solver.
        
        Args:
            num_disks (int): Number of disks in the Tower of Hanoi puzzle
            model (str): The OpenAI model to use
            verbose (bool): Whether to display verbose output
        """
        self.game = TowerOfHanoi(num_disks)
        self.model = model
        self.verbose = verbose
        self.messages = []
        self._initialize_messages()
        
    def _initialize_messages(self):
        """Initialize the conversation with the AI."""
        
        self.messages = [
            {
                "role": "system",
                "content": f"""
                    You are an expert at solving the Tower of Hanoi puzzle. 
                    Your task is to solve a {self.game.num_disks}-disk Tower of Hanoi puzzle by moving all disks from Tower A to Tower C.

                    Remember the rules:
                    1. Only one disk can be moved at a time
                    2. Each move consists of taking the top disk from one of the stacks and placing it on top of another stack or an empty rod
                    3. Bigger disk can't be placed on top of a smaller disk
                """
            }
        ]
    
    def _format_state_description(self, state):
        """Format the state of the towers as a string.
        
        Args:
            state (dict): The current state of the towers
            
        Returns:
            str: A formatted string representation of the state
        """
        description = []
        
        for tower in ['A', 'B', 'C']:
            disks = state[tower]
            if disks:
                disk_str = ", ".join(str(disk) for disk in disks)
                description.append(f"Tower {tower}: [{disk_str}] (top disk is {disks[0]})")
            else:
                description.append(f"Tower {tower}: [] (empty)")
                
        return "\n".join(description)
    
    def _handle_move(self, move: TowerOfHanoiMove):
        """Handle a move parsed from the assistant's response.
        
        Args:
            move (TowerOfHanoiMove): The move to be executed
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        source = move.source
        target = move.target
        
        if self.verbose:
            print(f"Assistant suggests moving disk from {source} to {target}")
            
        success = self.game.move(source, target)
        
        if not success and self.verbose:
            print(f"Invalid move: Cannot move disk from {source} to {target}")

        if success:
            self.game.display()
            
        return success
    
    def solve(self, max_iterations=100):
        """Solve the Tower of Hanoi puzzle using the OpenAI API.
        
        Args:
            max_iterations (int): Maximum number of iterations to attempt
            
        Returns:
            bool: True if the puzzle was solved, False otherwise
        """
        if self.verbose:
            print("Starting Tower of Hanoi puzzle...")
            self.game.display()
            
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            if self.verbose:
                print(f"Iteration {iteration}...")
            
            # Update with current state before each iteration
            current_state = self.game.get_state()
            state_description = self._format_state_description(current_state)

            # if True:
            #     self._initialize_messages()
            
            # Add a user message with the current state
            self.messages.append({
                "role": "user",
                "content": f"Current state of the towers:\n\n{state_description}\n\nPlease make the next move to solve the puzzle."
            })
                
            # Get response from OpenAI
            response = client.responses.parse(
                model=self.model,
                input=self.messages,
                text_format=TowerOfHanoiMove,
            )
            
            move = response.output_parsed
            if move is None:
                continue

            self.messages.append({
                "role": "assistant",
                "content": f'Moving top disk of {move.source} to {move.target}'
            })
            if not self.game.is_valid_move(move.source, move.target):
                self.messages.append({
                    "role": "user",
                    "content": f'Invalid move: Cannot move disk from {move.source} to {move.target}. Please suggest a valid move.'
                })

            self._handle_move(move)
                
            # Check if the puzzle is solved
            if self.game.is_solved():
                if self.verbose:
                    print(f"Puzzle solved in {self.game.moves} moves!")
                return True
                
        if self.verbose:
            print(f"Failed to solve the puzzle in {max_iterations} iterations.")
        return False
        
    def reset(self):
        """Reset the game and conversation."""
        self.game.reset()
        self._initialize_messages()


if __name__ == "__main__":
    # Make sure OPENAI_API_KEY is set in .env file
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set in .env file")
        exit(1)
        
    # Solve the puzzle
    solver = OpenAIHanoiSolver(num_disks=3)
    solver.solve()
