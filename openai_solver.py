"""
OpenAI API Integration for Tower of Hanoi Solver

This module provides the integration with OpenAI's API to solve the Tower of Hanoi
puzzle using tool-calling capabilities.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from hanoi import TowerOfHanoi

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the tools that can be used by the model
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "move_disk",
            "description": "Move a disk from one tower to another in the Tower of Hanoi puzzle",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "The source tower (A, B, or C)"
                    },
                    "target": {
                        "type": "string",
                        "description": "The target tower (A, B, or C)"
                    }
                },
                "required": ["source", "target"]
            }
        }
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "is_puzzle_solved",
    #         "description": "Check if the Tower of Hanoi puzzle is solved",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {}
    #         }
    #     }
    # }
]


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
                    Your task is to solve a {self.game.num_disks}-disk Tower of Hanoi puzzle by moving disks from Tower A to Tower C.

                    Remember the rules:
                    1. Only one disk can be moved at a time
                    2. Each move consists of taking the upper disk from one of the stacks and placing it on top of another stack or an empty rod
                    3. Bigger disk can't be placed on top of a smaller disk

                    You can use the following tools:
                    - move_disk: Move a disk from one tower to another
                    - is_puzzle_solved: Check if the puzzle is solved

                    Please solve the puzzle as quick as possible. If the minimum number of moves is already surpassed, proceed anyway.
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
        description.append(f"Moves so far: {state['moves']}")
        
        for tower in ['A', 'B', 'C']:
            disks = state[tower]
            if disks:
                disk_str = ", ".join(str(disk) for disk in disks)
                description.append(f"Tower {tower}: [{disk_str}] (top disk is {disks[0]})")
            else:
                description.append(f"Tower {tower}: [] (empty)")
                
        return "\n".join(description)
    
    def _handle_tool_call(self, tool_call):
        """Handle a tool call from the assistant.
        
        Args:
            tool_call (dict): The tool call from the assistant
            
        Returns:
            str: The result of the tool call
        """
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        if function_name == "move_disk":
            source = function_args.get("source")
            target = function_args.get("target")
            success = self.game.move(source, target)
            
            if success:
                result = f"Successfully moved disk from {source} to {target}"
                if self.verbose:
                    self.game.display()
            else:
                result = f"Invalid move: Cannot move disk from {source} to {target}"
                
            return result
        
            
        elif function_name == "is_puzzle_solved":
            solved = self.game.is_solved()
            return json.dumps({"solved": solved})
            
        return "Unknown function"
    
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
                "content": f"Current state of the towers:\n{state_description}\n\nPlease make the next move to solve the puzzle."
            })
                
            # Get response from OpenAI
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=TOOLS,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            self.messages.append(assistant_message)
            
            # Check if the assistant wants to use tools
            if not assistant_message.tool_calls:
                if self.verbose:
                    print(f"Assistant message: {assistant_message.content}")
                continue
                
            # Handle each tool call
            for tool_call in assistant_message.tool_calls:
                if self.verbose:
                    print(f"Tool call: {tool_call.function.name} with arguments {tool_call.function.arguments}")
                    
                result = self._handle_tool_call(tool_call)
                
                # Add the tool response to messages
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
                
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
