import random
from collections import Counter

P_A = {"yes": 0.8, "no": 0.2}
P_C = {"yes": 0.5, "no": 0.5}

P_G_given_A_C = {
    ("yes", "yes"): {"Good": 0.9, "OK": 0.1},
    ("yes", "no"): {"Good": 0.7, "OK": 0.3},
    ("no", "yes"): {"Good": 0.6, "OK": 0.4},
    ("no", "no"): {"Good": 0.3, "OK": 0.7},
}

P_J_given_G = {
    "Good": {"yes": 0.8, "no": 0.2},
    "OK": {"yes": 0.2, "no": 0.8},
}

P_S_given_G = {
    "Good": {"yes": 0.7, "no": 0.3},
    "OK": {"yes": 0.3, "no": 0.7},
}


def sample_from_distribution(prob_table):
    rnd = random.random()
    cumulative = 0
    for key, prob in prob_table.items():
        cumulative += prob
        if rnd <= cumulative:
            return key


def generate_sample():

    A = sample_from_distribution(P_A)

    C = sample_from_distribution(P_C)

    G = sample_from_distribution(P_G_given_A_C[(A, C)])

    J = sample_from_distribution(P_J_given_G[G])

    S = sample_from_distribution(P_S_given_G[G])

    return {"A": A, "C": C, "G": G, "J": J, "S": S}


def monte_carlo_inference(query_node, evidence, num_samples=10000):
    matching_samples = []

    for _ in range(num_samples):
        sample = generate_sample()
        if all(sample[var] == val for var, val in evidence.items()): 
            matching_samples.append(sample[query_node])

    if matching_samples:
        counts = Counter(matching_samples)
        total = len(matching_samples)
        return {key: counts[key] / total for key in counts}
    else:
        return None 

evidence = {"A": "yes", "C": "yes"}
query_node = "J" 

num_samples = 10000
result = monte_carlo_inference(query_node, evidence, num_samples)
print("Estimated probabilities for ")
print(
    f"{query_node} given evidence {evidence}: {result}")
