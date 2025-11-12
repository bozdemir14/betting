import pandas as pd
import numpy as np
import time

def process_football_data_complete(input_filename: str, output_filename: str):
    """
    Loads football data, generates a comprehensive list of all requested 
    outcome categories, and saves to a new CSV.
    """
    print(f"Starting comprehensive processing for '{input_filename}'...")
    start_time = time.time()

    # --- 1. Load and Prepare Data ---
    try:
        df = pd.read_csv(input_filename)
        print(f"Successfully loaded {len(df)} rows.")
    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
        return

    # --- 2. Vectorized Data Parsing and Cleaning ---
    scores_ft = df['Skor'].str.split('-', expand=True)
    df['home_ft'] = pd.to_numeric(scores_ft[0], errors='coerce')
    df['away_ft'] = pd.to_numeric(scores_ft[1], errors='coerce')

    scores_ht = df['IY_Skor'].str.split('-', expand=True)
    df['home_ht'] = pd.to_numeric(scores_ht[0], errors='coerce')
    df['away_ht'] = pd.to_numeric(scores_ht[1], errors='coerce')

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
    df['sh_diff'] = df['sh_fav'] - df['sh_opp']
    df['ft_total'] = df['ft_fav'] + df['ft_opp']
    df['ht_total'] = df['ht_fav'] + df['ht_opp']
    df['sh_total'] = df['sh_fav'] + df['sh_opp']

    # --- 4. Generate Categories (Comprehensive Loop) ---
    print("Generating all requested categories...")
    categories_list = []
    
    # Helper to format goal counts (e.g., 0, 1, ..., 6+)
    def format_goal_count(goals, cap=6):
        return f"{cap}+" if goals >= cap else str(goals)

    # Use itertuples for efficient row-wise iteration
    for row in df.itertuples():
        cats = set()
        venue = 'home' if row.Favorite_Team == 'Home' else 'away'

        # Primary outcomes
        if row.ft_diff > 0: cats.add(f"fav_win_{venue}")
        elif row.ft_diff == 0: cats.add(f"draw_{venue}")
        else: cats.add(f"fav_loss_{venue}")
        if row.ft_diff >= 0: cats.add(f"fav_double_chance_{venue}")
        if row.ft_diff >= 2: cats.add(f"fav_win_by_2+_{venue}")

        # Goal differences
        cats.add(f"ft_goal_diff_{row.ft_diff}_{venue}")
        cats.add(f"ht_goal_diff_{row.ht_diff}_{venue}")

        # Exact goal counts (0-6+)
        for period in ['ft', 'ht', 'sh']:
            for team in ['fav', 'opp', 'total']:
                goals = getattr(row, f"{period}_{team}")
                cats.add(f"{period}_{team}_goals_{format_goal_count(goals)}_{venue}")

        # Win to Nil & BTTS
        if row.ft_diff > 0 and row.ft_opp == 0: cats.add(f"fav_win_to_nil_{venue}")
        if row.ft_fav > 0 and row.ft_opp > 0: cats.add(f"btts_yes_ft_{venue}")
        if row.ht_fav > 0 and row.ht_opp > 0: cats.add(f"btts_yes_ht_{venue}")
        if row.sh_fav > 0 and row.sh_opp > 0: cats.add(f"btts_yes_sh_{venue}")

        # Half-time results
        if row.ht_diff > 0: ht_res = 'W'
        elif row.ht_diff == 0: ht_res = 'D'
        else: ht_res = 'L'
        if row.ft_diff > 0: ft_res = 'W'
        elif row.ft_diff == 0: ft_res = 'D'
        else: ft_res = 'L'
        cats.add(f"ht_ft_{ht_res}/{ft_res}_{venue}")

        # Half with most goals
        if row.ht_total > row.sh_total: cats.add(f"most_goals_1h_{venue}")
        elif row.sh_total > row.ht_total: cats.add(f"most_goals_2h_{venue}")
        else: cats.add(f"most_goals_equal_{venue}")
        
        # Favorite team scoring pattern
        if row.ht_fav > row.sh_fav: cats.add(f"fav_scored_more_1h_{venue}")
        elif row.sh_fav > row.ht_fav: cats.add(f"fav_scored_more_2h_{venue}")
        else: cats.add(f"fav_scored_equal_{venue}")

        # Specific scorelines
        cats.add(f"ft_score_{row.ft_fav}-{row.ft_opp}_{venue}")
        cats.add(f"ht_score_{row.ht_fav}-{row.ht_opp}_{venue}")

        categories_list.append(sorted(list(cats)))

    df['categories'] = categories_list

    # --- 5. Clean Up and Save ---
    df.drop(columns=[
        'home_ft', 'away_ft', 'home_ht', 'away_ht', 'ft_fav', 'ft_opp', 'ht_fav',
        'ht_opp', 'sh_fav', 'sh_opp', 'ft_diff', 'ht_diff', 'sh_diff', 'ft_total',
        'ht_total', 'sh_total'
    ], inplace=True)

    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    
    end_time = time.time()
    print("\n--- Processing Complete ---")
    print(f"Generated file: '{output_filename}' with {len(df)} rows.")
    print(f"Total time: {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    INPUT_FILE = 'fikstur_favorites_only.csv'
    OUTPUT_FILE = 'fikstur_with_all_categories.csv'
    
    process_football_data_complete(INPUT_FILE, OUTPUT_FILE)