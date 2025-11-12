import pandas as pd

# Load model results
results_df = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/model_results.csv')

# Load odds data
odds_df = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/generate_features/fikstur_tum_ligler_all_seasons.csv')

# For simplicity, assume some mappings (this is approximate)
# fav_win_away -> bet on 2 (away win), odds = column '2'
# no_draw_away -> no direct bet, but can use 1&2 or 2&0 if available, but here not, so calculate required
# For others, similar

mappings = {
    'fav_win_away': '2',
    'no_draw_away': None,  # no direct, calculate required
    'fav_double_chance_away': '1&2',  # if available, but not in this CSV
    # Add more as needed
}

report = []

for _, row in results_df.iterrows():
    feature = row['Feature']
    precision = row['Precision_True']
    required_odds = 1 / precision if precision > 0 else float('inf')
    available_odds = None
    if feature in mappings and mappings[feature]:
        col = mappings[feature]
        if col in odds_df.columns:
            # Convert to numeric, replace '-' with NaN
            numeric_odds = pd.to_numeric(odds_df[col], errors='coerce')
            available_odds = numeric_odds.mean()
    
    profitable = available_odds and available_odds > required_odds
    if available_odds:
        note = f"Current odds {available_odds:.2f}, {'profitable' if profitable else 'not profitable (need > {required_odds:.2f})'}"
    else:
        note = f"Unavailable - need odds > {required_odds:.2f} to be profitable"
    report.append({
        'Feature': feature,
        'Precision': precision,
        'Required_Odds': required_odds,
        'Available_Odds': available_odds,
        'Note': note
    })
    required_odds = 1 / precision if precision > 0 else float('inf')
    available_odds = None
    if feature in mappings and mappings[feature]:
        col = mappings[feature]
        if col in odds_df.columns:
            # Convert to numeric, replace '-' with NaN
            numeric_odds = pd.to_numeric(odds_df[col], errors='coerce')
            available_odds = numeric_odds.mean()
    
    profitable = available_odds and available_odds > required_odds
    if available_odds:
        note = f"Current odds {available_odds:.2f}, {'profitable' if profitable else 'not profitable (need > {required_odds:.2f})'}"
    else:
        note = f"Unavailable - need odds > {required_odds:.2f} to be profitable"
report_df = pd.DataFrame(report)
print(report_df.head(10))  # Show first 10

# Save report
report_df.to_csv('/Users/batumbp/Files/betting/_DENEME2/profit_report.csv', index=False)