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

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Genetic Solver", layout="wide")
st.title("🧬 Genetic Algorithm Solver")

# Sidebar for Inputs (replacing tkinter entry fields)
with st.sidebar:
    st.header("Parameters")
    coeffs_str = st.text_input("Coefficients (space-separated):", "3 2 -1")
    target_val = st.number_input("Target Value:", value=50)
    pop_size = st.slider("Population Size:", 10, 500, 100)
    mut_rate = st.slider("Mutation Rate:", 0.0, 1.0, 0.05)
    max_gen = st.number_input("Max Generations:", value=100)
    run_btn = st.button("Start Algorithm")

# --- Logic Execution ---
if run_btn:
    coeffs = list(map(int, coeffs_str.split()))
    population = generate_population(pop_size, len(coeffs))
    best_fit_history = []
    
    # Placeholder for live updates
    status = st.empty()
    
    for gen in range(max_gen):
        fitness_scores = [fitness_function(c, coeffs, target_val) for c in population]
        best_fit = min(fitness_scores)
        best_fit_history.append(best_fit)
        
        status.write(f"**Generation {gen+1}:** Best Fitness = `{best_fit}`")
        
        if best_fit == 0:
            st.success(f"🎯 Solution Found at Gen {gen+1}!")
            break

        # Standard GA Selection/Crossover/Mutation
        population = [x for _, x in sorted(zip(fitness_scores, population))][:pop_size // 2]
        new_pop = []
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(population, 2)
            new_pop.append(mutate(crossover(p1, p2), mut_rate))
        population = new_pop

    # Plotting (replacing FigureCanvasTkAgg)
    fig, ax = plt.subplots()
    ax.plot(best_fit_history, label="Best Fitness")
    ax.set_title("Fitness Over Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Error")
    st.pyplot(fig)