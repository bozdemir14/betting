import pandas as pd

# Read the CSV file
df = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/fikstur_tum_ligler_all_seasons.csv')

# Identify odds columns
odds_columns = ['1', '0', '2', '1&0', '1&2', '2&0', 'Alt', 'Üst']

# Find the favorite odds (minimum among 1, 0, 2)
df['Favorite_Odds'] = df[['1', '0', '2']].min(axis=1)

# Determine if favorite is home or away
def get_favorite_team(row):
    odds = {'home': row['1'], 'draw': row['0'], 'away': row['2']}
    min_odds = min(odds.values())
    if odds['home'] == min_odds:
        return 'Home'
    elif odds['away'] == min_odds:
        return 'Away'
    else:
        return 'Draw'

df['Favorite_Team'] = df.apply(get_favorite_team, axis=1)

# Remove all other odds columns
df = df.drop(columns=odds_columns)

# Save to new CSV
df.to_csv('/Users/batumbp/Files/betting/_DENEME2/fikstur_favorites_only.csv', index=False)

print("Processed CSV saved as fikstur_favorites_only.csv")