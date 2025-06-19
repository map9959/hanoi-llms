# Tower of Hanoi LLM Solver

This project uses Python, OpenAI's API, and tool-calling to solve the Tower of Hanoi problem. It demonstrates how large language models (LLMs) can be used to solve logical puzzles through tool-calling capabilities.

## Features

- **Core Tower of Hanoi Implementation**: A backend state machine representing the towers as lists of numbers.
- **OpenAI API Integration**: Uses OpenAI's tool-calling API to enable an LLM to solve the puzzle.
- **Multiple Interfaces**:
  - Console-based visualization with ASCII art representation
  - Command-line interface (CLI) for interactive play
- **Multiple Solving Methods**:
  - Manual solving
  - AI solving using OpenAI's API
  - Algorithmic solving using the recursive solution
- **Comparison Tools**: Compare the efficiency of different solving methods

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/hanoi-llms.git
   cd hanoi-llms
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key.

## Usage

### Command Line Interface

```bash
# Play manually with 3 disks
python cli.py --mode manual --disks 3

# Let the AI solve a 4-disk puzzle
python cli.py --mode ai --disks 4

# Watch the algorithmic solution for a 5-disk puzzle
python cli.py --mode algorithm --disks 5

# Compare different solving methods
python cli.py --mode compare --disks 3
```

## How It Works

### Tower of Hanoi Problem

The Tower of Hanoi is a mathematical puzzle that consists of three rods and a number of disks of different sizes. The puzzle starts with all disks stacked on one rod in ascending order of size (the smallest at the top). The objective is to move the entire stack to another rod, following these rules:

1. Only one disk can be moved at a time.
2. Each move consists of taking the upper disk from one of the stacks and placing it on top of another stack or an empty rod.
3. No disk may be placed on top of a smaller disk.

### LLM Tool-Calling Solution

This project demonstrates how an LLM can solve the Tower of Hanoi puzzle by:

1. Representing the state of the towers in a way the LLM can understand
2. Providing tools that allow the LLM to inspect the state and make moves
3. Giving the LLM clear instructions on the rules and objective
4. Allowing the LLM to iteratively solve the puzzle by making a sequence of moves

The OpenAI API is used with tool-calling capabilities, where the LLM can make function calls to:
- Get the current state of the towers
- Move disks between towers
- Check if the puzzle is solved

## Project Structure

- `hanoi.py`: Core implementation of the Tower of Hanoi puzzle
- `openai_solver.py`: Integration with the OpenAI API for LLM-based solving
- `cli.py`: Command-line interface for different modes of interaction
- `requirements.txt`: Required Python packages
- `.env.example`: Example environment variable file

## License

This project is licensed under the MIT License - see the LICENSE file for details.