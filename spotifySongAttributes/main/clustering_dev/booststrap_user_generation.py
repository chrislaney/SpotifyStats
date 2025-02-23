# this script is used to generate the initial dataset till enough users have joind/.
# note: current noise functions assume users listen to genres closer together in the strucutre. We can enfore this manually or just remove and make noise random. 
# this file can be extended and modfied to generate any type opf artifical users for testing and added to pieline to generate best results. 
import os
from datetime import datetime
import json
import numpy as np
# SCRIPT PARAMS <adjust as needed> #####################################################################################################################

#
NUM_USERS = 5000  # Total artificial users to generate,  Changing this will give us a general idea how many real users we may need. 
NUM_GENRES = 13  # Number of supergenres, play with this later maybe? we can add dismensiatly to users this way with info we can scrape 

# User Type Distribution: Adjust <percentages> easily here
USER_DISTRIBUTION = {
    "genre_centric": 100,    # % genre-centric
    "generalist": 0,       # % generalists
    "2_genre_hybrid": 0,   # % 2-genre hybrids
    "3_genre_hybrid": 0,   # % 3-genre hybrids
    "outlier": 0           # % outliers
}

# weights for genre-hybrid users 
TWO_GENRE_WEIGHTS = [0.4, 0.3]
THREE_GENRE_WEIGHTS = [0.35, 0.25, 0.2]


# SCRIPT <adjust with care as to effect on output> #####################################################################################################################

# Define the output directory
OUTPUT_DIR = 'bootstrap_data'

# Create the directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
default_filename = datetime.now().strftime("artifical_user_data_%Y-%m-%d_%H-%M-%S") + '.json'


# Generate Genre-Centric Users =
def generate_genre_centric_users(num_users=0):
    users = []

    # Calculate number of users per genre
    users_per_genre = num_users // NUM_GENRES
    remainder = num_users % NUM_GENRES  # To handle cases where num_users isn't perfectly divisible

    # Loop through each genre
    for i in range(NUM_GENRES):
        # Calculate how many users for this genre
        num_genre_users = users_per_genre + (1 if i < remainder else 0)  # Distribute the remainder evenly

        # Generate users for this genre
        for j in range(num_genre_users):
            base = np.zeros(NUM_GENRES)
            base[i] = 0.7  # 70% preference for the primary genre

            # Use random noise instead of Gaussian noise
            noisy_distribution = add_random_noise(base)
            user_id = f"TestUser_Genre_{i}_{j}"
            users.append({"user_id": user_id, "distribution": noisy_distribution.tolist()})

    return users


# Generate Generalist Users - Dirichlet distribution for broad taste
def generate_generalist_users(num_users=0):
    users = []
    for i in range(num_users):
        distribution = np.random.dirichlet(np.ones(NUM_GENRES), size=1)[0]
        user_id = f"TestUser_Generalist_{i}"
        users.append({"user_id": user_id, "distribution": distribution.tolist()})
    return users

# Generate Hybrid Users -  for 2 or 3 genre focuses
def generate_hybrid_users(num_users=0, num_primary_genres=2):
 
    if num_primary_genres not in [2, 3]:
        raise ValueError("num_primary_genres must be either 2 or 3.")
    
    users = []

    # Define preference weights for 2 or 3 genres
    if num_primary_genres == 2:
        weights = TWO_GENRE_WEIGHTS 

    elif num_primary_genres == 3:
        weights = THREE_GENRE_WEIGHTS  

    # Generate users
    for i in range(num_users):
        # Randomly select primary genres without replacement
        primary_genres = np.random.choice(NUM_GENRES, num_primary_genres, replace=False)
        
        # Initialize distribution and assign weights
        base = np.zeros(NUM_GENRES)
        base[primary_genres] = weights
        
        # Add Gaussian noise and normalize
        noisy_distribution = add_gaussian_noise(base)
        
        # Create unique user ID
        
        user_id = f"TestUser_{num_primary_genres}-genre-hybrid_G_{i}"
        users.append({"user_id": user_id, "distribution": noisy_distribution.tolist()})
    
    return users


# Generate Outlier Users - completely random for 
def generate_outlier_users(num_users=0):
    users = []
    for i in range(num_users):
        distribution = np.random.rand(NUM_GENRES)
        distribution /= np.sum(distribution)  # Normalize to 1
        user_id = f"TestUser_Outlier_{i}"
        users.append({"user_id": user_id, "distribution": distribution.tolist()})
    return users


    
# Adds Gaussian Noise to Data
def add_gaussian_noise(center, std_dev=0.1, size=NUM_GENRES):
    noisy_distribution = np.random.normal(center, std_dev, size)
    noisy_distribution = np.maximum(0, noisy_distribution)  # No negative values
    return noisy_distribution / np.sum(noisy_distribution)  # Normalize to 1

# Adds Random Noise to Data
def add_random_noise(base, noise_level=0.3):
    
    # Add uniform random noise to each genre
    noise = np.random.uniform(-noise_level, noise_level, size=base.shape)
    noisy_distribution = base + noise
    
    # Ensure no negative values
    noisy_distribution = np.clip(noisy_distribution, 0, None)
    
    # Normalize the distribution so it sums to 1
    return noisy_distribution / noisy_distribution.sum()


# generate users based on dev SCRIPT PARAMS <adjust as needed> at top of file
def generate_artificial_users(output_filename):
    # Validate percentages sum to 100
    if sum(USER_DISTRIBUTION.values()) != 100:
        raise ValueError("USER_DISTRIBUTION percentages must sum to 100.")

    # Set user_counts for given distribution
    user_counts = {user_type: round((percentage / 100) * NUM_USERS)
                   for user_type, percentage in USER_DISTRIBUTION.items()}

    # Generate users with given parameters 
    users = []
    users += generate_genre_centric_users(user_counts["genre_centric"])
    users += generate_generalist_users(user_counts["generalist"])
    users += generate_hybrid_users(user_counts["2_genre_hybrid"], 2)
    users += generate_hybrid_users(user_counts["3_genre_hybrid"], 3)
    users += generate_outlier_users(user_counts["outlier"])

    # Construct the full path for the output files
    json_output_path = os.path.join(OUTPUT_DIR, output_filename)
    txt_output_path = os.path.join(OUTPUT_DIR, output_filename.replace('.json', '.txt'))

    # Save JSON for inspection
    with open(json_output_path, 'w') as f:
        json.dump(users, f, indent=4)
    print(f"Artificial users generated and saved to {json_output_path}")

    # Save Parameters Used in .txt
    with open(txt_output_path, 'w') as f:
        f.write("=== Parameters Used ===\n")
        f.write(f"Total Users to Generate: {NUM_USERS}\n")
        f.write(f"Number of Supergenres: {NUM_GENRES}\n")
        f.write("\nUser Type Distribution:\n")
        for user_type, percentage in USER_DISTRIBUTION.items():
            f.write(f"  - {user_type}: {percentage}%\n")
        f.write("\nWeights for Hybrid Users:\n")
        f.write(f"  - 2-Genre Hybrid Weights: {TWO_GENRE_WEIGHTS}\n")
        f.write(f"  - 3-Genre Hybrid Weights: {THREE_GENRE_WEIGHTS}\n")
    print(f"Parameters saved to {txt_output_path}")



def display_and_confirm():
    # Generate default filename with current date and time
    default_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.json'

    print("\n=== Configuration Summary ===")
    print(f"Total Users to Generate: {NUM_USERS}")
    print(f"Number of Supergenres: {NUM_GENRES}")
    print("\nUser Type Distribution:")
    for user_type, percentage in USER_DISTRIBUTION.items():
        print(f"  - {user_type}: {percentage}%")

    print("\nWeights for Hybrid Users:")
    print(f"  - 2-Genre Hybrid Weights: {TWO_GENRE_WEIGHTS}")
    print(f"  - 3-Genre Hybrid Weights: {THREE_GENRE_WEIGHTS}")
    
    print("\n==============================")
    print(f"Default output directory: {OUTPUT_DIR}")
    print(f"Default output file: {os.path.join(OUTPUT_DIR, default_filename)}")
    user_input = input("Proceed with these settings? (y/n) or enter <new filename>: ").strip()

    if user_input.lower() == 'n':
        print("Aborted by user.")
        exit(0)
    elif user_input.lower() == 'y' or user_input == '':
        output_file = default_filename
    else:
        output_file = user_input if user_input.endswith('.json') else user_input + '.json'

    return output_file

# Run the generation process with confirmation
if __name__ == "__main__":
    output_filename = display_and_confirm()
    generate_artificial_users(output_filename)
