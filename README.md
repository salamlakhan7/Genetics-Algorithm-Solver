#  Genetic Algorithm Solver

A Streamlit app that uses a genetic algorithm to solve linear equations of the form:

```
a·x + b·y + c·z + ... = Target
```

Given a set of coefficients and a target value, the algorithm evolves a population of candidate solutions over generations - selecting, combining, and mutating them - until it finds integer values that satisfy the equation.

##  Live Demo

[Add your Streamlit Cloud URL here once deployed]

##  Features

- **Custom equations** - enter any number of coefficients
- **Adjustable parameters** - population size, mutation rate, max generations
- **Elitism** - the best candidate found is always carried into the next generation, so progress is never lost
- **Live convergence chart** - tracks both best and average population fitness over time
- **Real-time feedback** - progress bar and per-generation status updates

##  How It Works

1. **Initial population** - random integer candidates are generated
2. **Fitness function** - measures how far each candidate's result is from the target (lower is better, 0 = solved)
3. **Elitism** - the best candidate from the current generation is preserved into the next
4. **Selection** - the top-performing candidates are kept as parents
5. **Crossover** - parent values are combined to produce new candidates
6. **Mutation** - occasional random tweaks are introduced to maintain diversity and avoid getting stuck

The process repeats until either a candidate reaches zero error (an exact solution) or the maximum number of generations is reached, at which point the closest solution found is shown.

##  Installation & Local Setup

Clone the repository:
```bash
git clone https://github.com/salamlakhan7/Genetics-Algorithm-Solver.git
cd Genetics-Algorithm-Solver
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
streamlit run GA_app.py
```

##  Known Limitations

- Candidate values are currently sampled from a fixed integer range, so very large or negative-only solutions may not be reachable without adjusting the code
- Designed for linear equations; not currently built for quadratic or non-linear targets

##  Author

Built by [Abdul Salam](https://github.com/salamlakhan7) as a personal project exploring genetic algorithms with Python and Streamlit.
