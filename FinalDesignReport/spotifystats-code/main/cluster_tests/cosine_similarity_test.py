"""
DEPRECATED; Tool set created by Justin to make functions that took users from a json file and loaded them into vectors with their respective genre
representation; is not used in production, but was used with Noah's cluster_test.py file to help tune the hyperparameters for the clustering algorithm
Loads users from generated_users/
Builds three types of vectors:
	Flat Subgenre Vector (based on genres_flat.json)
	Dynamic Subgenre Vector (based on only seen genres)
	Hardcoded Supergenre Vector (15 fixed supergenres)
Computes cosine similarity for each
Saves:
	Similarity matrices to user_similarity.json
	Heatmaps to PNGs
	Timings to timings.json
"""
"""
# Default (uses generated_users/)
python analyze_user_similarity.py

# Custom input folder (e.g., data/users_set_b/)
python analyze_user_similarity.py data/users_set_b

"""
#SOME BOILER PLATE CODE WAS GENERATED WITH CHATGPT
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import time

# 15 fixed supergenre list
HARDCODED_SUPERGENRES = [
    "Pop", "Electronic", "Hip Hop", "R&B", "Latin",
    "Rock", "Metal", "Country", "Folk/Acoustic", "Classical",
    "Jazz", "Blues", "Easy listening", "New age", "World/Traditional"
]

# Load all user profiles
def load_users(user_dir):
    users = {}
    for file in os.listdir(user_dir):
        if file.endswith(".json"):
            with open(os.path.join(user_dir, file), "r") as f:
                data = json.load(f)
                users[data["user_id"]] = {
                    "subgenres": data.get("subgenres", {}),
                    "supergenres": data.get("supergenres", {})
                }
    return users

# Load genre list from genres_flat.json (assumed in script directory)
def load_flat_genres(path="../genres_flat.json"):
    with open(path, "r") as f:
        data = json.load(f)
        return sorted(set(data["genres"]))

# Vectorization using fixed genre list (flat or supergenres)
def build_fixed_vectors(users, genre_list, field="subgenres"):
    user_ids = list(users.keys())
    index = {genre: i for i, genre in enumerate(genre_list)}
    matrix = np.zeros((len(user_ids), len(genre_list)))

    for i, user_id in enumerate(user_ids):
        for genre, score in users[user_id][field].items():
            if genre in index:
                matrix[i][index[genre]] = score
    return matrix, user_ids

# Vectorization using only genres seen across users
def build_dynamic_vectors(users):
    all_genres = set()
    for u in users.values():
        all_genres.update(u["subgenres"].keys())
    genre_list = sorted(all_genres)
    return build_fixed_vectors(users, genre_list, field="subgenres")

# Compute cosine similarity dict from matrix
def compute_similarity(matrix, user_ids):
    sim = cosine_similarity(matrix)
    return {
        user_ids[i]: {
            user_ids[j]: float(sim[i][j]) for j in range(len(user_ids))
        }
        for i in range(len(user_ids))
    }, sim

# Plot similarity heatmap
def plot_heatmap(sim_matrix, labels, title, filename):
    fig, ax = plt.subplots(figsize=(10, 8))
    cax = ax.matshow(sim_matrix, cmap="viridis")
    plt.title(title, pad=20)
    plt.xticks(range(len(labels)), labels, rotation=90)
    plt.yticks(range(len(labels)), labels)
    fig.colorbar(cax)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Saved heatmap: {filename}")

if __name__ == "__main__":
    # Use optional CLI arg or fallback
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "generated_users"
    if not os.path.isdir(input_dir):
        print(f"Error: Directory '{input_dir}' does not exist.")
        sys.exit(1)

    output_subdir = os.path.join(input_dir, "similarity_outputs")
    os.makedirs(output_subdir, exist_ok=True)

    users = load_users(input_dir)
    flat_genres = load_flat_genres()

    results = {}
    timings = {}

    print("Computing Flat Subgenre Vector similarities...")
    t0 = time.perf_counter()
    flat_matrix, user_ids = build_fixed_vectors(users, flat_genres, field="subgenres")
    flat_sim_dict, flat_sim_matrix = compute_similarity(flat_matrix, user_ids)
    timings["flat_subgenre_vector"] = time.perf_counter() - t0
    results["flat_subgenre_similarity"] = flat_sim_dict
    plot_heatmap(
        flat_sim_matrix,
        user_ids,
        "Flat Subgenre Cosine Similarity",
        os.path.join(output_subdir, "flat_subgenre_similarity_heatmap.png")
    )

    print("Computing Dynamic Subgenre Vector similarities...")
    t0 = time.perf_counter()
    dynamic_matrix, user_ids = build_dynamic_vectors(users)
    dynamic_sim_dict, dynamic_sim_matrix = compute_similarity(dynamic_matrix, user_ids)
    timings["dynamic_subgenre_vector"] = time.perf_counter() - t0
    results["dynamic_subgenre_similarity"] = dynamic_sim_dict
    plot_heatmap(
        dynamic_sim_matrix,
        user_ids,
        "Dynamic Subgenre Cosine Similarity",
        os.path.join(output_subdir, "dynamic_subgenre_similarity_heatmap.png")
    )

    print("Computing Hardcoded Supergenre Vector similarities...")
    t0 = time.perf_counter()
    super_matrix, user_ids = build_fixed_vectors(users, HARDCODED_SUPERGENRES, field="supergenres")
    super_sim_dict, super_sim_matrix = compute_similarity(super_matrix, user_ids)
    timings["supergenre_vector"] = time.perf_counter() - t0
    results["supergenre_similarity"] = super_sim_dict
    plot_heatmap(
        super_sim_matrix,
        user_ids,
        "Supergenre Cosine Similarity",
        os.path.join(output_subdir, "supergenre_similarity_heatmap.png")
    )

    # Save results
    similarity_path = os.path.join(output_subdir, "user_similarity.json")
    with open(similarity_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved: {similarity_path}")

    timing_path = os.path.join(output_subdir, "timings.json")
    with open(timing_path, "w") as f:
        json.dump(timings, f, indent=2)
    print(f"Saved: {timing_path}")

    print("\nTiming summary:")
    for k, v in timings.items():
        print(f"{k}: {v:.4f} seconds")
