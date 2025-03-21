import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Configuration
query_user_directory =  "groups_plays"         # new/test users
reference_user_directory =  "top_artist_users"        # reference users
cache_file = "cached_reference_vectors_supergenres.npz"         # where matrix and metadata are stored
genre_field = "supergenres"
top_n = 2000
bottom_n = 2000

# Load users from JSON files
def load_users_from_directory(user_dir, genre_field="supergenres"):
    users = {}
    all_genres = set()

    for filename in os.listdir(user_dir):
        if filename.endswith(".json"):
            with open(os.path.join(user_dir, filename), "r") as f:
                data = json.load(f)
                user_id = data["user_id"]
                genre_distro = data.get(genre_field, {})
                users[user_id] = genre_distro
                all_genres.update(genre_distro.keys())

    genre_list = sorted(list(all_genres))
    return users, genre_list

# Build matrix from user dicts
def build_user_matrix(users, genre_list):
    matrix = []
    user_ids = []

    for user_id, genre_distro in users.items():
        row = [genre_distro.get(genre, 0.0) for genre in genre_list]
        matrix.append(row)
        user_ids.append(user_id)

    return np.array(matrix), user_ids

# Match top and bottom users
def find_similar_and_dissimilar_users(new_vector, existing_matrix, user_ids, top_n=5, bottom_n=5): 
    similarities = cosine_similarity([new_vector], existing_matrix)[0]
    sorted_indices = np.argsort(similarities)
    bottom_users = [(user_ids[i], similarities[i]) for i in sorted_indices[:bottom_n]]
    top_users = [(user_ids[i], similarities[i]) for i in sorted_indices[-top_n:][::-1]]
    return top_users, bottom_users

# Ask user whether to regenerate or load cached matrix
def should_regenerate_cache():
    if os.path.exists(cache_file):
        return False  # Use cache by default
    return True       # No cache exists, must generate

# Load or generate reference user matrix
def get_reference_data():
    if should_regenerate_cache():
        print("🔄 Generating reference matrix...")
        reference_users, reference_genres = load_users_from_directory(reference_user_directory, genre_field)
        matrix, user_ids = build_user_matrix(reference_users, reference_genres)
        np.savez(cache_file, matrix=matrix, user_ids=user_ids, genres=reference_genres)
    else:
        print("✅ Using cached reference matrix.")
        cached = np.load(cache_file, allow_pickle=True)
        matrix = cached["matrix"]
        user_ids = cached["user_ids"].tolist()
        reference_genres = cached["genres"].tolist()
    return matrix, user_ids, reference_genres

# Load query users
query_users, query_genres = load_users_from_directory(query_user_directory, genre_field)

# Load or regenerate reference matrix
reference_matrix, reference_user_ids, reference_genres = get_reference_data()

# Use consistent genre list
combined_genres = sorted(set(query_genres + reference_genres))

# Rebuild reference matrix with full genre space if needed
if len(combined_genres) != reference_matrix.shape[1]:
    print("⚠️ Genre mismatch detected. Rebuilding reference matrix with updated genres...")
    reference_users, _ = load_users_from_directory(reference_user_directory, genre_field)
    reference_matrix, reference_user_ids = build_user_matrix(reference_users, combined_genres)
    np.savez(cache_file, matrix=reference_matrix, user_ids=reference_user_ids, genres=combined_genres)

# Compare each query user
results_top, results_bottom = [], []

for user_id, genre_distro in query_users.items():
    query_vector = [genre_distro.get(g, 0.0) for g in combined_genres]
    top_matches, bottom_matches = find_similar_and_dissimilar_users(query_vector, reference_matrix, reference_user_ids, top_n=top_n, bottom_n=bottom_n)

    for match_id, sim in top_matches:
        results_top.append({"Query User": user_id, "Match Type": "Top", "Matched User": match_id, "Similarity": sim})

    for match_id, sim in bottom_matches:
        results_bottom.append({"Query User": user_id, "Match Type": "Bottom", "Matched User": match_id, "Similarity": sim})

# Display to user
top_df = pd.DataFrame(results_top)
bottom_df = pd.DataFrame(results_bottom)

print("\nTop Similar Users:")
print(top_df.to_string(index=False))

print("\nLeast Similar Users:")
print(bottom_df.to_string(index=False))

combined_df = pd.concat([top_df, bottom_df], ignore_index=True)
combined_df.to_csv("user_similarities_group_plays.csv", index=False)