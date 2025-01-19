import os
import json
import pandas as pd
from Levenshtein import distance
from tqdm import tqdm

def load_json(file_path):
    """
    Load a JSON file and return its content.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        dict or list: Parsed JSON data.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def save_progress(file_path, data):
    """
    Save progress or parameters into a JSON file.

    Parameters:
        file_path (str): The path to the JSON file.
        data (dict): The data to save.

    Returns:
        None
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Progress saved to {file_path}")
    except Exception as e:
        print(f"Failed to save progress: {e}")

def load_progress(file_path):
    """
    Load progress or parameters from a JSON file.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded data, or an empty dictionary if not found or failed.
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as json_file:
                return json.load(json_file)
        else:
            print(f"No previous progress found at {file_path}.")
    except Exception as e:
        print(f"Failed to load progress: {e}")
    return {}

def calculate_levenshtein_distances(test_values, train_values, progress_path, current_status):
    """
    Calculate the Levenshtein distances between two lists of strings.

    Parameters:
        test_values (iterable): Iterable containing test strings.
        train_values (iterable): Iterable containing train strings.
        progress_path (str): Path to save progress JSON file.
        current_status (dict): Current processing status.

    Returns:
        pd.DataFrame: DataFrame containing the distances.
    """
    distances = []
    for idx, test_value in enumerate(tqdm(test_values, desc="Calculating Distances")):
        row_distances = [distance(test_value, train_value) for train_value in train_values]
        distances.append(row_distances)

        # Update progress for each test_value
        current_status["last_processed_test_value"] = idx
        save_progress(progress_path, current_status)

    return pd.DataFrame(distances, columns=train_values)

# Define paths and folder structure
main_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\05.DATA_VALIDATION'
output_main_path = r'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\RESULT\06.EDIT_DISTANCE_VALIDATION'
progress_path = os.path.join(output_main_path, "progress.json")
folds = [f"fold_{i}" for i in range(1, 5)]
malware_variants = [f"MALWARE_{i}" for i in range(100, 400, 100)]
benign_variants = [f"BENIGN_{i}" for i in range(100, 400, 100)]

# Load previous progress
progress = load_progress(progress_path)

# Loop through each folder and process files
for fold in folds:
    for malware in malware_variants:
        for benign in benign_variants:
            folder_path = os.path.join(main_path, fold, f"{malware}_{benign}")

            if not os.path.exists(folder_path):
                continue

            validation_test_path = os.path.join(folder_path, "validation_test.json")
            validation_train_path = os.path.join(folder_path, "validation_train.json")

            # Process validation_test.json
            if os.path.isfile(validation_test_path):
                validation_test_data = load_json(validation_test_path)
                if validation_test_data:
                    try:
                        validation_test_df = pd.DataFrame(validation_test_data)
                    except Exception as e:
                        print(f"Failed to convert validation_test data to DataFrame: {e}")
            
            # Process validation_train.json
            if os.path.isfile(validation_train_path):
                validation_train_data = load_json(validation_train_path)
                if validation_train_data:
                    try:
                        validation_train_df = pd.DataFrame(validation_train_data)
                    except Exception as e:
                        print(f"Failed to convert validation_train data to DataFrame: {e}")

            # Calculate edit distances if both DataFrames are available
            if 'validation_test_df' in locals() and 'validation_train_df' in locals():
                if not validation_test_df.empty and not validation_train_df.empty:
                    try:
                        test_column = validation_test_df.columns[0]
                        train_column = validation_train_df.columns[0]

                        current_status = {
                            "current_fold": fold,
                            "current_malware_variant": malware,
                            "current_benign_variant": benign,
                            "last_processed_test_value": -1
                        }

                        distances_df = calculate_levenshtein_distances(
                            validation_test_df[test_column], 
                            validation_train_df[train_column], 
                            progress_path, 
                            current_status
                        )

                        # Save distances to CSV with descriptive filename
                        output_filename = f"levenshtein_distances_{fold}_{malware}_{benign}.csv"
                        output_path = os.path.join(output_main_path, fold, f"{malware}_{benign}", output_filename)
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        distances_df.to_csv(output_path, index=False)
                        print(f"Distances saved to {output_path}")

                    except Exception as e:
                        print(f"Failed to calculate edit distances: {e}")