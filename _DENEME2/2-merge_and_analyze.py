import pandas as pd
import numpy as np
import os

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
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"Error: Main data file '{DATA_FILE}' not found.")
    exit()

# Load test indices for consistent split
test_indices = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/results/test_indices.csv', header=None).squeeze()
test_df = df.loc[test_indices]

# Get list of features from predictions directory
predictions_dir = '/Users/batumbp/Files/betting/_DENEME2/results/predictions'
all_features = [f.replace('.csv', '') for f in os.listdir(predictions_dir) if f.endswith('.csv')]

profit_report = []

for feature in all_features:
    # 1. Load the saved predictions for this feature
    try:
        preds_df = pd.read_csv(f'/Users/batumbp/Files/betting/_DENEME2/results/predictions/{feature}.csv', index_col=0)
    except FileNotFoundError:
        continue

    # 2. Merge predictions with the test set containing odds
    backtest_df = test_df.join(preds_df)

    # 3. Check if odds mapping exists
    if feature in FEATURE_TO_ODDS_MAPPING:
        odds_col = FEATURE_TO_ODDS_MAPPING[feature]
        if odds_col not in backtest_df.columns:
            profit_report.append({
                'Feature': feature,
                'Value_Bets_Found': 'N/A (odds column missing)',
                'Win_Rate_on_Value_Bets': 'N/A',
                'Avg_Odds_Bet': 'N/A',
                'Total_Profit': 'N/A',
                'ROI_%': 'N/A',
                'Avg_Required_Odds_for_Value': f"{1 / backtest_df['predicted_proba'].mean():.2f}"
            })
            continue

        # Convert odds to numeric and drop invalid rows
        backtest_df['odds'] = pd.to_numeric(backtest_df[odds_col], errors='coerce')
        backtest_df.dropna(subset=['odds', 'predicted_proba'], inplace=True)

        # 4. Implement the value betting logic
        backtest_df['implied_proba'] = 1 / backtest_df['odds']
        value_bets = backtest_df[backtest_df['predicted_proba'] > backtest_df['implied_proba']].copy()

        if not value_bets.empty:
            # 5. Calculate profit and ROI on the value bets
            num_bets = len(value_bets)
            
            # Calculate profit for each bet
            # Profit is (odds - 1) for a win, -1 for a loss
            value_bets['profit'] = np.where(value_bets['true_label'] == 1, value_bets['odds'] - 1, -1)
            
            total_profit = value_bets['profit'].sum()
            roi = (total_profit / num_bets) * 100
            
            # 6. Gather metrics for the report
            win_rate = value_bets['true_label'].mean()
            avg_odds_bet = value_bets['odds'].mean()
            avg_required_odds = 1 / value_bets['predicted_proba'].mean()
            
            profit_report.append({
                'Feature': feature,
                'Value_Bets_Found': num_bets,
                'Win_Rate_on_Value_Bets': f"{win_rate:.2%}",
                'Avg_Odds_Bet': f"{avg_odds_bet:.2f}",
                'Total_Profit': f"{total_profit:.2f}",
                'ROI_%': f"{roi:.2f}",
                'Avg_Required_Odds_for_Value': f"{avg_required_odds:.2f}"
            })
            # Note: Only report features that have actual value bets to focus on actionable insights

# --- 4. Display and Save Report ---
if profit_report:
    report_df = pd.DataFrame(profit_report)
    print("\n--- Value Betting Backtest Report ---")
    print(report_df.to_string())
    report_df.to_csv('/Users/batumbp/Files/betting/_DENEME2/results/profit_report_value_betting.csv', index=False)
else:
    print("\nCould not generate profitability report. Check mappings and odds columns.")