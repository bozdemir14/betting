import pandas as pd
import numpy as np
import time

# --- Helper Functions for Binning ---

def bin_goal_difference(diff_series: pd.Series) -> pd.Series:
    """Bins goal differences into specified categories."""
    conditions = [
        diff_series >= 3,
        diff_series == 2,
        diff_series == 1,
        diff_series == 0,
        diff_series == -1,
        diff_series == -2,
        diff_series <= -3,
    ]
    choices = ['3+', '2', '1', '0', '-1', '-2', '-3-']
    return np.select(conditions, choices, default='other')

def bin_goal_count(goal_series: pd.Series, cap: int) -> pd.Series:
    """Bins goal counts into categories up to a specified cap (e.g., 5+)."""
    return np.where(goal_series >= cap, f"{cap}+", goal_series.astype(str))


def create_binned_feature_matrix(input_filename: str, output_filename: str):
    """
    Loads football data and creates a one-hot encoded feature matrix with
    binned categories as specified.
    """
    print(f"Starting binned feature matrix generation for '{input_filename}'...")
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
    venue_suffix = np.where(is_home_fav, '_home', '_away')
    
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

    # --- 4. Generate Binned Category Columns ---
    print("Generating binned one-hot encoded columns...")
    
    category_dfs = []
    base_df = df[['Season', 'Lig', 'Hafta', 'Tarih', 'Kod', 'EvSahibi', 'Deplasman', 'Skor', 'IY_Skor', 'Favorite_Odds', 'Favorite_Team']].copy()

    # A. Static Boolean Categories (including specific scores)
    static_cats = {
        'ht_score_2-2': (df['ht_fav'] == 2) & (df['ht_opp'] == 2),
        'ft_score_0-0': (df['ft_fav'] == 0) & (df['ft_opp'] == 0),
    }
    for name, mask in static_cats.items():
        base_df[f'{name}_home'] = (mask & is_home_fav).astype(int)
        base_df[f'{name}_away'] = (mask & ~is_home_fav).astype(int)

    # B. Binned Dynamic Categories
    # Goal Differences
    binned_ft_diff = 'ft_goal_diff_' + bin_goal_difference(df['ft_diff']) + venue_suffix
    category_dfs.append(pd.get_dummies(binned_ft_diff, prefix='', prefix_sep=''))
    
    binned_ht_diff = 'ht_goal_diff_' + bin_goal_difference(df['ht_diff']) + venue_suffix
    category_dfs.append(pd.get_dummies(binned_ht_diff, prefix='', prefix_sep=''))

    # Goal Counts
    goal_configs = {
        'ft_fav_goals': (df['ft_fav'], 5), 'ft_opp_goals': (df['ft_opp'], 5),
        'ht_fav_goals': (df['ht_fav'], 3), 'ht_opp_goals': (df['ht_opp'], 3),
        'sh_fav_goals': (df['sh_fav'], 3), 'sh_opp_goals': (df['sh_opp'], 3),
        'ft_total_goals': (df['ft_total'], 6),
        'ht_total_goals': (df['ht_total'], 3),
        'sh_total_goals': (df['sh_total'], 3),
    }
    for name, (series, cap) in goal_configs.items():
        binned_series = name + '_' + bin_goal_count(series, cap) + venue_suffix
        category_dfs.append(pd.get_dummies(binned_series, prefix='', prefix_sep=''))

    # --- 5. Combine and Save ---
    print("Combining all features...")
    final_df = pd.concat([base_df] + category_dfs, axis=1)

    final_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    
    end_time = time.time()
    print("\n--- Processing Complete ---")
    print(f"Generated file: '{output_filename}' with {len(final_df)} rows and {len(final_df.columns)} columns.")
    print(f"Total time: {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    INPUT_FILE = 'fikstur_favorites_only.csv'
    OUTPUT_FILE = 'fikstur_feature_matrix_binned.csv'
    
    create_binned_feature_matrix(INPUT_FILE, OUTPUT_FILE)