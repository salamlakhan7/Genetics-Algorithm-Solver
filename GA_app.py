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

def average_fitness(fitness_scores):
    return sum(fitness_scores) / len(fitness_scores)

# Helper to show the math
def format_equation(coeffs, variables):
    terms = []
    for c, v in zip(coeffs, variables):
        terms.append(f"{c}({v})")
    return " + ".join(terms).replace("+ -", "- ")

# --- Streamlit UI Setup ---
st.set_page_config(page_title="GA Solver", layout="wide")
st.title(" Genetic Algorithm Solver")

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
    try:
        coeffs = list(map(int, coeffs_str.split()))
    except ValueError:
        st.error("Coefficients must be whole numbers separated by spaces (e.g. `3 2 -1`).")
        st.stop()

    if len(coeffs) == 0:
        st.error("Enter at least one coefficient.")
        st.stop()

    population = generate_population(pop_size, len(coeffs))
    best_fit_history = []
    avg_fit_history = []

    # Elitism: track the best candidate ever found, across all generations
    best_ever_candidate = None
    best_ever_fit = None

    progress_bar = st.progress(0)
    status = st.empty()
    solved = False

    for gen in range(max_gen):
        fitness_scores = [fitness_function(c, coeffs, target_val) for c in population]

        gen_best_idx = fitness_scores.index(min(fitness_scores))
        gen_best_candidate = population[gen_best_idx]
        gen_best_fit = fitness_scores[gen_best_idx]

        # Update all-time best (elitism source of truth)
        if best_ever_fit is None or gen_best_fit < best_ever_fit:
            best_ever_fit = gen_best_fit
            best_ever_candidate = gen_best_candidate

        best_fit_history.append(best_ever_fit)
        avg_fit_history.append(average_fitness(fitness_scores))

        progress_bar.progress((gen + 1) / max_gen)
        status.write(
            f"**Generation {gen + 1}:** Best Fitness = `{best_ever_fit}` | "
            f"Average Fitness = `{avg_fit_history[-1]:.2f}`"
        )

        if best_ever_fit == 0:
            math_str = format_equation(coeffs, best_ever_candidate)
            st.success(f" **Solution Found at Gen {gen + 1}!**")
            st.code(f"{math_str} = {target_val}", language="python")
            solved = True
            break

        # Selection
        sorted_pop = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0])]
        parents = sorted_pop[:max(2, pop_size // 2)]

        # Crossover + mutation, with elitism: the all-time best always survives into the next generation
        new_pop = [best_ever_candidate]
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(parents, 2)
            new_pop.append(mutate(crossover(p1, p2), mut_rate))
        population = new_pop

    if not solved:
        math_str = format_equation(coeffs, best_ever_candidate)
        st.warning(f" **No exact solution found within {max_gen} generations.**")
        st.write(f"Closest result: `{math_str} = {sum(c * x for c, x in zip(coeffs, best_ever_candidate))}` "
                 f"(target was `{target_val}`, error `{best_ever_fit}`)")

    # Plotting Results
    fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(best_fit_history, label="Best Fitness (Error)")
    ax.plot(avg_fit_history, label="Average Fitness (Error)", linestyle="--")
    ax.set_title("Fitness Over Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Error")
    ax.legend()
    ax.grid(True)
   st.pyplot(fig, use_container_width=True)
