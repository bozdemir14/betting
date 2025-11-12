"""
Quick Data Explorer for the enriched soccer dataset
Use this to understand your data before modeling
"""

import pandas as pd
import numpy as np

def explore_data():
    """Explore the enriched dataset"""
    
    print("="*80)
    print("SOCCER DATASET EXPLORER")
    print("="*80)
    
    # Load data
    df = pd.read_csv('/Users/batumbp/Files/betting/ML/data.csv')
    
    print(f"\n📊 Dataset Overview:")
    print(f"   Shape: {df.shape[0]} matches × {df.shape[1]} features")
    print(f"   Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    # League distribution
    print(f"\n🏆 Leagues in dataset:")
    league_counts = df['League'].value_counts()
    for league, count in league_counts.items():
        print(f"   {league}: {count} matches")
    
    # Team statistics
    print(f"\n⚽ Team statistics:")
    teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique()
    print(f"   Total teams: {len(teams)}")
    
    # Most common matchups
    df['Matchup'] = df['HomeTeam'] + ' vs ' + df['AwayTeam']
    top_matchups = df['Matchup'].value_counts().head(5)
    print(f"\n🔥 Most frequent matchups:")
    for matchup, count in top_matchups.items():
        print(f"   {matchup}: {count} times")
    
    # Result distribution
    print(f"\n📈 Match outcomes:")
    result_map = {0: 'Home Win', 1: 'Draw', 2: 'Away Win'}
    for result, label in result_map.items():
        count = (df['FT_Result'] == result).sum()
        pct = count / len(df) * 100
        print(f"   {label}: {count} ({pct:.1f}%)")
    
    # Odds analysis
    print(f"\n💰 Odds statistics:")
    print(f"   Average Home Odds: {df['HomeOdds'].mean():.2f} (range: {df['HomeOdds'].min():.2f}-{df['HomeOdds'].max():.2f})")
    print(f"   Average Draw Odds: {df['DrawOdds'].mean():.2f} (range: {df['DrawOdds'].min():.2f}-{df['DrawOdds'].max():.2f})")
    print(f"   Average Away Odds: {df['AwayOdds'].mean():.2f} (range: {df['AwayOdds'].min():.2f}-{df['AwayOdds'].max():.2f})")
    print(f"   Average Bookmaker Margin: {df['Margin'].mean():.3f} ({df['Margin'].mean()*100:.1f}%)")
    
    # Goals analysis
    print(f"\n⚽ Goals statistics:")
    print(f"   Average total goals per match: {df['Total_Goals'].mean():.2f}")
    print(f"   Average home goals: {df['FTHG'].mean():.2f}")
    print(f"   Average away goals: {df['FTAG'].mean():.2f}")
    print(f"   Matches with over 2.5 goals: {(df['Total_Goals'] > 2.5).sum()} ({(df['Total_Goals'] > 2.5).sum()/len(df)*100:.1f}%)")
    print(f"   Matches with BTTS: {df['BTTS'].sum()} ({df['BTTS'].sum()/len(df)*100:.1f}%)")
    print(f"   Home clean sheets: {df['Home_Clean_Sheet'].sum()} ({df['Home_Clean_Sheet'].sum()/len(df)*100:.1f}%)")
    print(f"   Away clean sheets: {df['Away_Clean_Sheet'].sum()} ({df['Away_Clean_Sheet'].sum()/len(df)*100:.1f}%)")
    
    # Halftime analysis
    print(f"\n⏱️ Halftime statistics:")
    ht_result_map = {0: 'Home Leading', 1: 'Draw', 2: 'Away Leading'}
    for result, label in ht_result_map.items():
        count = (df['HT_Result'] == result).sum()
        pct = count / len(df) * 100
        print(f"   {label} at HT: {count} ({pct:.1f}%)")
    print(f"   Average halftime goals: {(df['HTHG'] + df['HTAG']).mean():.2f}")
    print(f"   Comebacks: {df['Comeback_Required'].sum()} ({df['Comeback_Required'].sum()/len(df)*100:.1f}%)")
    
    # Market efficiency
    print(f"\n📊 Market efficiency insights:")
    print(f"   Average market entropy: {df['Entropy'].mean():.3f}")
    print(f"   Average mismatch ratio: {df['Mismatch_Ratio'].mean():.2f}")
    print(f"   Home team is favorite: {df['Home_Is_Favorite'].sum()} times ({df['Home_Is_Favorite'].sum()/len(df)*100:.1f}%)")
    
    # When favorite wins
    favorites_correct = 0
    for idx, row in df.iterrows():
        if row['Home_Is_Favorite'] == 1 and row['FT_Result'] == 0:
            favorites_correct += 1
        elif row['Home_Is_Favorite'] == 0 and row['FT_Result'] == 2:
            favorites_correct += 1
    
    print(f"   Favorite wins: {favorites_correct} ({favorites_correct/len(df)*100:.1f}%)")
    
    # Data quality
    print(f"\n🔍 Data quality:")
    total_cells = len(df) * len(df.columns)
    missing_cells = df.isna().sum().sum()
    print(f"   Total cells: {total_cells:,}")
    print(f"   Missing cells: {missing_cells:,} ({missing_cells/total_cells*100:.2f}%)")
    print(f"\n   Features with missing values:")
    missing_by_col = df.isna().sum()
    missing_by_col = missing_by_col[missing_by_col > 0].sort_values(ascending=False)
    for col, count in missing_by_col.items():
        pct = count / len(df) * 100
        print(f"      {col}: {count} ({pct:.1f}%)")
    
    # Form data availability
    form_available = df['Home_Form_Points_Last5'].notna().sum()
    print(f"\n   Matches with form data: {form_available} ({form_available/len(df)*100:.1f}%)")
    
    # Interesting patterns
    print(f"\n🎯 Interesting patterns:")
    
    # Home advantage
    home_goals_total = df['FTHG'].sum()
    away_goals_total = df['FTAG'].sum()
    print(f"   Home advantage: {home_goals_total} home goals vs {away_goals_total} away goals")
    print(f"   Goal ratio (home/away): {home_goals_total/away_goals_total:.2f}")
    
    # High scoring matches
    high_scoring = df[df['Total_Goals'] >= 5]
    print(f"   High-scoring matches (5+ goals): {len(high_scoring)} ({len(high_scoring)/len(df)*100:.1f}%)")
    
    # Low scoring matches
    low_scoring = df[df['Total_Goals'] <= 1]
    print(f"   Low-scoring matches (0-1 goals): {len(low_scoring)} ({len(low_scoring)/len(df)*100:.1f}%)")
    
    # Big upsets (favorite with odds < 1.5 loses)
    strong_favorites = df[df['Favorite_Odds'] < 1.5]
    upsets = 0
    for idx, row in strong_favorites.iterrows():
        if row['Home_Is_Favorite'] == 1 and row['FT_Result'] != 0:
            upsets += 1
        elif row['Home_Is_Favorite'] == 0 and row['FT_Result'] != 2:
            upsets += 1
    print(f"   Major upsets (favorite <1.5 odds loses): {upsets} ({upsets/len(strong_favorites)*100:.1f}% of strong favorite matches)")
    
    print(f"\n{'='*80}")
    print("✓ Exploration complete!")
    print(f"{'='*80}\n")
    
    # Sample interesting matches
    print("📝 Sample of interesting matches:\n")
    interesting = df.nsmallest(5, 'Favorite_Odds')[['HomeTeam', 'AwayTeam', 'FT_Score', 
                                                      'Favorite_Odds', 'FT_Result', 
                                                      'Market_Expected_Goals']].copy()
    result_labels = {0: 'H', 1: 'D', 2: 'A'}
    interesting['Result'] = interesting['FT_Result'].map(result_labels)
    interesting = interesting.drop('FT_Result', axis=1)
    interesting.columns = ['Home', 'Away', 'Score', 'Fav_Odds', 'Exp_Goals', 'Result']
    print(interesting.to_string(index=False))
    
    print("\n" + "="*80)

if __name__ == "__main__":
    explore_data()
