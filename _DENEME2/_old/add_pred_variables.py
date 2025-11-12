import pandas as pd
import numpy as np
import time

def process_football_data(input_filename: str, output_filename: str):
    """
    Loads football fixture data, generates outcome categories, and saves to a new CSV.

    Args:
        input_filename (str): The name of the source CSV file.
        output_filename (str): The name of the destination CSV file.
    """
    print(f"Starting processing for '{input_filename}'...")
    start_time = time.time()

    # --- 1. Load Data with Error Handling ---
    try:
        df = pd.read_csv(input_filename)
        print(f"Successfully loaded {len(df)} rows.")
    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found in the current directory.")
        return

    # --- 2. Vectorized Data Parsing and Cleaning ---
    # Split score strings into separate columns. Use 'coerce' to handle potential errors.
    scores_ft = df['Skor'].str.split('-', expand=True)
    df['home_ft'] = pd.to_numeric(scores_ft[0], errors='coerce')
    df['away_ft'] = pd.to_numeric(scores_ft[1], errors='coerce')

    scores_ht = df['IY_Skor'].str.split('-', expand=True)
    df['home_ht'] = pd.to_numeric(scores_ht[0], errors='coerce')
    df['away_ht'] = pd.to_numeric(scores_ht[1], errors='coerce')

    # Drop rows where scores could not be parsed to ensure data integrity
    original_rows = len(df)
    df.dropna(subset=['home_ft', 'away_ft', 'home_ht', 'away_ht'], inplace=True)
    df[['home_ft', 'away_ft', 'home_ht', 'away_ht']] = df[['home_ft', 'away_ft', 'home_ht', 'away_ht']].astype(int)
    
    if len(df) < original_rows:
        print(f"Warning: Dropped {original_rows - len(df)} rows due to malformed scores.")

    # --- 3. Vectorized Metric Calculation ---
    is_home_fav = (df['Favorite_Team'] == 'Home')
    
    df['ft_fav'] = np.where(is_home_fav, df['home_ft'], df['away_ft'])
    df['ft_opp'] = np.where(is_home_fav, df['away_ft'], df['home_ft'])
    df['ht_fav'] = np.where(is_home_fav, df['home_ht'], df['away_ht'])
    df['ht_opp'] = np.where(is_home_fav, df['away_ht'], df['home_ht'])

    df['sh_fav'] = df['ft_fav'] - df['ht_fav']
    df['sh_opp'] = df['ft_opp'] - df['ht_opp']
    df['ft_diff'] = df['ft_fav'] - df['ft_opp']
    df['ht_diff'] = df['ht_fav'] - df['ht_opp']
    df['ft_total'] = df['ft_fav'] + df['ft_opp']
    df['ht_total'] = df['ht_fav'] + df['ht_opp']
    df['sh_total'] = df['sh_fav'] + df['sh_opp']
    
    # --- 4. Define Category Conditions (Boolean Masks) ---
    conditions = {
        'fav_win': (df['ft_diff'] > 0),
        'draw': (df['ft_diff'] == 0),
        'fav_loss': (df['ft_diff'] < 0),
        'fav_double_chance': (df['ft_diff'] >= 0),
        'btts_yes': (df['ft_fav'] > 0) & (df['ft_opp'] > 0),
        'btts_no': (df['ft_fav'] == 0) | (df['ft_opp'] == 0),
        'fav_win_to_nil': (df['ft_diff'] > 0) & (df['ft_opp'] == 0),
        'fav_failed_to_score': (df['ft_fav'] == 0),
        'match_goals_over_2.5': (df['ft_total'] > 2.5),
        'match_goals_under_2.5': (df['ft_total'] < 2.5),
        'ht_match_goals_over_1.5': (df['ht_total'] > 1.5),
        'ht_match_goals_under_1.5': (df['ht_total'] < 1.5),
        'fav_scored_both_halves': (df['ht_fav'] > 0) & (df['sh_fav'] > 0),
        'ht_fav_win': (df['ht_diff'] > 0),
        'ht_draw': (df['ht_diff'] == 0),
        'ht_fav_loss': (df['ht_diff'] < 0),
        'fav_comeback_win': (df['ht_diff'] < 0) & (df['ft_diff'] > 0),
        'fav_threw_lead_loss': (df['ht_diff'] > 0) & (df['ft_diff'] < 0),
        'most_goals_2h': (df['sh_total'] > df['ht_total']),
        'most_goals_1h': (df['ht_total'] > df['sh_total']),
        'most_goals_equal': (df['ht_total'] == df['sh_total']),
        'fav_scored_first': ((df['home_ht'] > 0) & (df['away_ht'] == 0) & is_home_fav) | \
                            ((df['away_ht'] > 0) & (df['home_ht'] == 0) & ~is_home_fav) | \
                            ((df['ht_total'] == 0) & (df['sh_fav'] > 0) & (df['sh_opp'] == 0)),
    }

    # --- 5. Assemble Categories ---
    print("Generating categories...")
    categories_list = [[] for _ in range(len(df))]
    venue_map = np.where(is_home_fav, '_home', '_away')

    for cat_name, mask in conditions.items():
        # Apply the venue suffix and add the category where the condition is true
        cat_with_venue = cat_name + venue_map
        np.add.at(categories_list, np.where(mask)[0], cat_with_venue[mask].tolist())

    df['categories'] = [sorted(cats) for cats in categories_list]

    # --- 6. Clean Up and Save ---
    # Drop intermediate calculation columns
    df.drop(columns=[
        'home_ft', 'away_ft', 'home_ht', 'away_ht', 'ft_fav', 'ft_opp', 'ht_fav',
        'ht_opp', 'sh_fav', 'sh_opp', 'ft_diff', 'ht_diff', 'ft_total',
        'ht_total', 'sh_total'
    ], inplace=True)

    # Save to new CSV file
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    
    end_time = time.time()
    print("\n--- Processing Complete ---")
    print(f"Generated file: '{output_filename}' with {len(df)} rows.")
    print(f"Total time: {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    # Define the input and output filenames
    INPUT_FILE = 'fikstur_favorites_only.csv'
    OUTPUT_FILE = 'fikstur_with_categories.csv'
    
    process_football_data(INPUT_FILE, OUTPUT_FILE)