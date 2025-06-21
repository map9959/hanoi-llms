# Tower of Hanoi LLM Solver

This project uses OpenAI's API to attempt to solve the Tower of Hanoi problem.

## Takeaways

This is the only part of the README that's been written manually.

I vibe-coded this on the way to a local AI meetup. There's been significant discussion on a recent Apple preprint claiming LLMs "reason inconsistently across puzzles", which has been interpreted as "LLMs can't think". My main objection to the preprint was that there is no representation of any intermediate state of the game; it's implied the LLM is expected to keep one internally as it outputs moves for the solution. In the spirit of citizen science, I decided to supplement the LLM with a "state machine" displaying the current state of the game, as well as a "move" tool to use in order to move a disk from one tower to another. I consider a run a "success" if the LLM uses "significantly" fewer valid moves to move all disks from tower A to tower C than the [expected number of moves a random walk would use](https://arxiv.org/pdf/1304.3780) to achieve the same goal.

The LLM regularly outputs invalid moves. If given a list of valid moves to choose from, it often gets stuck in a state of moving a single disk back and forth, even when instructions are clarified in the prompt. I replaced the "move" tool with a structured output in order to force it to make a move each time, and this seemed to reduce performance, even when given "reasoning" space in the output. On N=4, it often gets stuck in the strange failure state of moving all disks to tower B rather than tower C, as specified in the instructions.

If you don't believe me, you can run it yourself.

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

## Section for LLMs to read

### Notes on Tower of Hanoi

The Tower of Hanoi is a mathematical puzzle that consists of three rods and a number of disks of different sizes. The puzzle starts with all disks stacked on one rod in ascending order of size (the smallest at the top). The objective is to move the entire stack to another rod, following these rules:

1. Only one disk can be moved at a time.
2. Each move consists of taking the upper disk from one of the stacks and placing it on top of another stack or an empty rod.
3. No disk may be placed on top of a smaller disk.

### Project Structure

- `hanoi.py`: Core implementation of the Tower of Hanoi puzzle
- `openai_solver.py`: Integration with the OpenAI API for LLM-based solving
- `cli.py`: Command-line interface for different modes of interaction
- `requirements.txt`: Required Python packages
- `.env.example`: Example environment variable file

## Sources
```
@misc{illusion-of-thinking,
title = {The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity},
author = {Parshin Shojaee*† and Iman Mirzadeh* and Keivan Alizadeh and Maxwell Horton and Samy Bengio and Mehrdad Farajtabar},
year = {2025},
URL = {https://ml-site.cdn-apple.com/papers/the-illusion-of-thinking.pdf}
}
@inbook{Alekseyev_2015,
   title={Solving the Tower of Hanoi with Random Moves},
   ISBN={9781400881338},
   url={http://dx.doi.org/10.23943/princeton/9780691164038.003.0005},
   DOI={10.23943/princeton/9780691164038.003.0005},
   booktitle={The Mathematics of Various Entertaining Subjects},
   publisher={Princeton University Press},
   author={Alekseyev, Max A. and Berger, Toby},
   year={2015},
   month=dec }
```

## License

This project is licensed under the MIT License.