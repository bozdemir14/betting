import pandas as pd
import numpy as np
import time

def create_feature_matrix(input_filename: str, output_filename: str):
    """
    Loads football data and creates a one-hot encoded feature matrix where each
    possible outcome category is a separate column.
    """
    print(f"Starting feature matrix generation for '{input_filename}'...")
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

    # --- 4. Generate Category Columns ---
    print("Generating one-hot encoded columns...")
    
    # This list will hold all the new category DataFrames
    category_dfs = []

    # A. Static Boolean Categories
    static_cats = {
        'fav_win': (df['ft_diff'] > 0),
        'draw': (df['ft_diff'] == 0),
        'fav_loss': (df['ft_diff'] < 0),
        'fav_double_chance': (df['ft_diff'] >= 0),
        'fav_win_by_2+': (df['ft_diff'] >= 2),
        'fav_win_to_nil': (df['ft_diff'] > 0) & (df['ft_opp'] == 0),
        'btts_yes_ft': (df['ft_fav'] > 0) & (df['ft_opp'] > 0),
        'btts_yes_ht': (df['ht_fav'] > 0) & (df['ht_opp'] > 0),
        'btts_yes_sh': (df['sh_fav'] > 0) & (df['sh_opp'] > 0),
        'most_goals_1h': (df['ht_total'] > df['sh_total']),
        'most_goals_2h': (df['sh_total'] > df['ht_total']),
        'most_goals_equal': (df['ht_total'] == df['sh_total']),
        'fav_scored_more_1h': (df['ht_fav'] > df['sh_fav']),
        'fav_scored_more_2h': (df['sh_fav'] > df['ht_fav']),
        'fav_scored_equal': (df['ht_fav'] == df['sh_fav']),
    }

    for name, mask in static_cats.items():
        # Create home/away versions for each static category
        df[f'{name}_home'] = (mask & is_home_fav).astype(int)
        df[f'{name}_away'] = (mask & ~is_home_fav).astype(int)

    # B. Dynamic Categories using pd.get_dummies
    # Goal Differences
    category_dfs.append(pd.get_dummies('ft_goal_diff_' + df['ft_diff'].astype(str) + venue_suffix, prefix='', prefix_sep=''))
    category_dfs.append(pd.get_dummies('ht_goal_diff_' + df['ht_diff'].astype(str) + venue_suffix, prefix='', prefix_sep=''))

    # Exact Goal Counts (0-6+)
    def format_goal_count(goals, cap=6):
        return np.where(goals >= cap, f"{cap}+", goals.astype(str))

    for period in ['ft', 'ht', 'sh']:
        for team in ['fav', 'opp', 'total']:
            goals = df[f"{period}_{team}"]
            temp_series = f"{period}_{team}_goals_" + format_goal_count(goals) + venue_suffix
            category_dfs.append(pd.get_dummies(temp_series, prefix='', prefix_sep=''))

    # HT/FT Result
    ht_res = np.select([df['ht_diff'] > 0, df['ht_diff'] == 0], ['W', 'D'], default='L')
    ft_res = np.select([df['ft_diff'] > 0, df['ft_diff'] == 0], ['W', 'D'], default='L')
    temp_series = 'ht_ft_' + ht_res + '/' + ft_res + venue_suffix
    category_dfs.append(pd.get_dummies(temp_series, prefix='', prefix_sep=''))

    # Specific Scorelines
    temp_series_ft = 'ft_score_' + df['ft_fav'].astype(str) + '-' + df['ft_opp'].astype(str) + venue_suffix
    category_dfs.append(pd.get_dummies(temp_series_ft, prefix='', prefix_sep=''))
    temp_series_ht = 'ht_score_' + df['ht_fav'].astype(str) + '-' + df['ht_opp'].astype(str) + venue_suffix
    category_dfs.append(pd.get_dummies(temp_series_ht, prefix='', prefix_sep=''))

    # --- 5. Combine and Save ---
    print("Combining all features...")
    # Concatenate original data with all new dummy variable dataframes
    final_df = pd.concat([df] + category_dfs, axis=1)

    # Drop intermediate calculation columns
    final_df.drop(columns=[
        'home_ft', 'away_ft', 'home_ht', 'away_ht', 'ft_fav', 'ft_opp', 'ht_fav',
        'ht_opp', 'sh_fav', 'sh_opp', 'ft_diff', 'ht_diff', 'ft_total',
        'ht_total', 'sh_total'
    ], inplace=True)

    final_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    
    end_time = time.time()
    print("\n--- Processing Complete ---")
    print(f"Generated file: '{output_filename}' with {len(final_df)} rows and {len(final_df.columns)} columns.")
    print(f"Total time: {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    INPUT_FILE = 'fikstur_favorites_only.csv'
    OUTPUT_FILE = 'fikstur_feature_matrix.csv'
    
    create_feature_matrix(INPUT_FILE, OUTPUT_FILE)