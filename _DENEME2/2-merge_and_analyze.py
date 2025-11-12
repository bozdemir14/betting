import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import joblib

# --- 1. Merge Odds into Feature Matrix ---
print("Merging features with odds...")
features_df = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/data/fikstur_feature_matrix_final.csv')
odds_df = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/data/fikstur_tum_ligler_all_seasons.csv')
merge_keys = ['Season', 'Lig', 'Hafta', 'Tarih', 'Kod', 'EvSahibi', 'Deplasman', 'Skor', 'IY_Skor']
merged_df = pd.merge(features_df, odds_df[merge_keys + ['1', '0', '2', '1&0', '1&2', '2&0', 'Alt', 'Üst']], on=merge_keys, how='left')
merged_df.to_csv('/Users/batumbp/Files/betting/_DENEME2/data/fikstur_feature_matrix_with_odds.csv', index=False)
print("Merged file saved.")

# --- Configuration ---
DATA_FILE = '/Users/batumbp/Files/betting/_DENEME2/data/fikstur_feature_matrix_with_odds.csv'
RESULTS_FILE = '/Users/batumbp/Files/betting/_DENEME2/results/model_results.csv'

FEATURE_TO_ODDS_MAPPING = {
    'fav_win_home': '1',
    'fav_win_away': '2',
    'draw_home': '0',
    'draw_away': '0',
    'no_draw_home': '1&2',
    'no_draw_away': '1&2',
    'fav_double_chance_home': '1&0',
    'fav_double_chance_away': '2&0',
    'opp_double_chance_home': '2&0',
    'opp_double_chance_away': '1&0',
}

# --- 2. Load Data ---
model_results = pd.read_csv(RESULTS_FILE)
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"Error: Main data file '{DATA_FILE}' not found.")
    exit()

# Load test indices for consistent split
test_indices = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/results/test_indices.csv', header=None).squeeze()
test_df = df.loc[test_indices]

# Load the saved encoder and encode test features
encoder = joblib.load('/Users/batumbp/Files/betting/_DENEME2/results/encoder.pkl')
input_cols = ['Favorite_Odds', 'Favorite_Team', 'Lig', 'Season', 'Hafta']
for col in input_cols:
    test_df[col] = test_df[col].astype('category')
X_test_encoded = encoder.transform(test_df[input_cols])

all_features = model_results.sort_values('Precision', ascending=False)
profit_report = []

for _, row in all_features.iterrows():
    feature = row['Feature']
    precision = row['Precision']

    # Load the trained model
    model_path = f'/Users/batumbp/Files/betting/_DENEME2/results/models/{feature.replace("/", "_")}.pkl'
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        continue  # Skip if model not saved

    # Predict on test set
    y_pred = model.predict(X_test_encoded)
    y_test = test_df[feature]

    if feature in FEATURE_TO_ODDS_MAPPING:
        odds_col = FEATURE_TO_ODDS_MAPPING[feature]
        if odds_col not in test_df.columns:
            print(f"Warning: Odds column '{odds_col}' for feature '{feature}' not found. Skipping.")
            continue

        # Simulate bets based on predictions
        bets_indices = y_pred == 1
        if not bets_indices.any():
            continue

        odds_for_bets = pd.to_numeric(test_df.loc[bets_indices, odds_col], errors='coerce').dropna()
        if odds_for_bets.empty:
            continue

        # Actual outcomes for the bets
        actual_outcomes = test_df.loc[bets_indices, feature]
        wins = actual_outcomes == 1
        losses = actual_outcomes == 0

        num_bets = len(odds_for_bets)
        num_wins = wins.sum()
        num_losses = losses.sum()

        # Profit calculation: sum of (odds - 1) for wins minus losses
        win_odds = odds_for_bets[wins]
        total_profit = (win_odds - 1).sum() - num_losses
        roi = (total_profit / num_bets) * 100 if num_bets > 0 else 0
        avg_odds = odds_for_bets.mean()

        profit_report.append({
            'Feature': feature,
            'Precision': precision,
            'Simulated_Bets': num_bets,
            'Avg_Odds_On_Win': f"{avg_odds:.2f}",
            'Est_Profit': f"{total_profit:.2f}",
            'Est_ROI_%': f"{roi:.2f}",
            'Required_Odds_for_Profit': f"{1/precision:.2f}" if precision > 0 else 'N/A'
        })
    else:
        # No mapping: just required odds
        profit_report.append({
            'Feature': feature,
            'Precision': precision,
            'Simulated_Bets': 'N/A (no odds mapping)',
            'Avg_Odds_On_Win': 'N/A',
            'Est_Profit': 'N/A',
            'Est_ROI_%': 'N/A',
            'Required_Odds_for_Profit': f"{1/precision:.2f}" if precision > 0 else 'N/A'
        })

# --- 4. Display and Save Report ---
if profit_report:
    report_df = pd.DataFrame(profit_report)
    print("\n--- Profitability Simulation Report ---")
    print(report_df.to_string())
    report_df.to_csv('/Users/batumbp/Files/betting/_DENEME2/results/profit_report.csv', index=False)
else:
    print("\nCould not generate profitability report. Check mappings and odds columns.")