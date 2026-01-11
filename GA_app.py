import streamlit as st
import random
import matplotlib.pyplot as plt

# --- Genetic Algorithm Core ---
def fitness_function(candidate, coeffs, target):
    return abs(sum(c * x for c, x in zip(coeffs, candidate)) - target)

def mutate(candidate, rate):
    return [x + random.choice([-1, 0, 1]) if random.random() < rate else x for x in candidate]

def crossover(p1, p2):
    return [random.choice([x, y]) for x, y in zip(p1, p2)]

def generate_population(size, length):
    return [[random.randint(0, 20) for _ in range(length)] for _ in range(size)]

# Helper to show the math
def format_equation(coeffs, variables):
    terms = []
    for c, v in zip(coeffs, variables):
        terms.append(f"{c}({v})")
    return " + ".join(terms).replace("+ -", "- ")

# --- Streamlit UI Setup ---
st.set_page_config(page_title="GA Solver", layout="wide")
st.title("🧬 Genetic Algorithm Solver")

with st.sidebar:
    st.header("Parameters")
    coeffs_str = st.text_input("Coefficients (space-separated):", "3 2 -1")
    target_val = st.number_input("Target Value:", value=50)
    pop_size = st.slider("Population Size:", 10, 500, 100)
    mut_rate = st.slider("Mutation Rate:", 0.0, 1.0, 0.05)
    max_gen = st.number_input("Max Generations:", value=100)
    run_btn = st.button("Start Algorithm")

# --- Execution ---
if run_btn:
    coeffs = list(map(int, coeffs_str.split()))
    population = generate_population(pop_size, len(coeffs))
    best_fit_history = []
    
    progress_bar = st.progress(0)
    status = st.empty()
    
    for gen in range(max_gen):
        fitness_scores = [fitness_function(c, coeffs, target_val) for c in population]
        best_idx = fitness_scores.index(min(fitness_scores))
        best_candidate = population[best_idx]
        best_fit = fitness_scores[best_idx]
        
        best_fit_history.append(best_fit)
        progress_bar.progress((gen + 1) / max_gen)
        status.write(f"**Generation {gen+1}:** Best Fitness = `{best_fit}`")
        
        if best_fit == 0:
            math_str = format_equation(coeffs, best_candidate)
            st.success(f"🎯 **Solution Found at Gen {gen+1}!**")
            st.code(f"{math_str} = {target_val}", language="python") # Displays equation clearly
            break

        # Selection/Crossover/Mutation logic
        sorted_pop = [x for _, x in sorted(zip(fitness_scores, population))]
        parents = sorted_pop[:pop_size // 2]
        new_pop = []
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(parents, 2)
            new_pop.append(mutate(crossover(p1, p2), mut_rate))
        population = new_pop

    # Plotting Results
    fig, ax = plt.subplots()
    ax.plot(best_fit_history, label="Error (Fitness)")
    ax.set_title("Fitness Over Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Error")
    ax.grid(True)
    st.pyplot(fig)