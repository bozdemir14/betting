"""
Feature Engineering Script for Soccer Match Prediction
Generates all possible features from the current dataset
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')


def parse_score(score_str):
    """Parse score string '2 - 1' into two integers"""
    if pd.isna(score_str) or score_str == '-':
        return None, None
    try:
        parts = str(score_str).split('-')
        home = int(parts[0].strip())
        away = int(parts[1].strip())
        return home, away
    except:
        return None, None


def calculate_result(home_goals, away_goals):
    """Calculate match result: 0=Home Win, 1=Draw, 2=Away Win"""
    if pd.isna(home_goals) or pd.isna(away_goals):
        return None
    if home_goals > away_goals:
        return 0  # Home Win
    elif home_goals == away_goals:
        return 1  # Draw
    else:
        return 2  # Away Win


def load_and_parse_data(file_path):
    """Load the CSV and parse basic features"""
    print("Loading data...")
    df = pd.read_csv(file_path)
    
    print(f"Loaded {len(df)} matches")
    
    # Parse scores
    print("Parsing scores...")
    df[['FTHG', 'FTAG']] = df['Skor'].apply(lambda x: pd.Series(parse_score(x)))
    df[['HTHG', 'HTAG']] = df['IY_Skor'].apply(lambda x: pd.Series(parse_score(x)))
    
    # Calculate results
    df['FT_Result'] = df.apply(lambda row: calculate_result(row['FTHG'], row['FTAG']), axis=1)
    df['HT_Result'] = df.apply(lambda row: calculate_result(row['HTHG'], row['HTAG']), axis=1)
    
    # Rename columns for clarity
    df = df.rename(columns={
        'Lig': 'League',
        'Hafta': 'Week',
        'Tarih': 'Date',
        'Kod': 'Code',
        'EvSahibi': 'HomeTeam',
        'Deplasman': 'AwayTeam',
        'Skor': 'FT_Score',
        'IY_Skor': 'HT_Score',
        '1': 'HomeOdds',
        '0': 'DrawOdds',
        '2': 'AwayOdds',
        '1&0': 'HomeDrawOdds',
        '1&2': 'HomeAwayOdds',
        '2&0': 'AwayDrawOdds',
        'Alt': 'Under2.5',
        'Üst': 'Over2.5'
    })
    
    # Parse date (format: dd/mm/yyyy for new file, handles full dates)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    
    # Handle missing odds (convert '-' to NaN)
    odds_columns = ['HomeOdds', 'DrawOdds', 'AwayOdds', 'HomeDrawOdds', 
                    'HomeAwayOdds', 'AwayDrawOdds', 'Under2.5', 'Over2.5']
    for col in odds_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def generate_odds_features(df):
    """Generate features derived from betting odds"""
    print("Generating odds-derived features...")
    
    # Implied probabilities (accounting for bookmaker margin)
    df['Prob_Home'] = 1 / df['HomeOdds']
    df['Prob_Draw'] = 1 / df['DrawOdds']
    df['Prob_Away'] = 1 / df['AwayOdds']
    
    # Bookmaker margin (overround)
    df['Margin'] = df['Prob_Home'] + df['Prob_Draw'] + df['Prob_Away'] - 1
    
    # True probabilities (remove margin)
    df['True_Prob_Home'] = df['Prob_Home'] / (df['Prob_Home'] + df['Prob_Draw'] + df['Prob_Away'])
    df['True_Prob_Draw'] = df['Prob_Draw'] / (df['Prob_Home'] + df['Prob_Draw'] + df['Prob_Away'])
    df['True_Prob_Away'] = df['Prob_Away'] / (df['Prob_Home'] + df['Prob_Draw'] + df['Prob_Away'])
    
    # Market entropy (uncertainty measure)
    df['Entropy'] = -(df['True_Prob_Home'] * np.log2(df['True_Prob_Home'] + 1e-10) +
                      df['True_Prob_Draw'] * np.log2(df['True_Prob_Draw'] + 1e-10) +
                      df['True_Prob_Away'] * np.log2(df['True_Prob_Away'] + 1e-10))
    
    # Favorite odds and underdog odds
    df['Favorite_Odds'] = df[['HomeOdds', 'AwayOdds']].min(axis=1)
    df['Underdog_Odds'] = df[['HomeOdds', 'AwayOdds']].max(axis=1)
    
    # Mismatch ratio (strength difference)
    df['Mismatch_Ratio'] = df['Underdog_Odds'] / df['Favorite_Odds']
    
    # Is home team favorite?
    df['Home_Is_Favorite'] = (df['HomeOdds'] < df['AwayOdds']).astype(int)
    
    return df


def generate_goal_market_features(df):
    """Generate features from Over/Under 2.5 goals market"""
    print("Generating goal market features...")
    
    # Probabilities for O/U 2.5
    df['Prob_Over2.5'] = 1 / df['Over2.5']
    df['Prob_Under2.5'] = 1 / df['Under2.5']
    
    # Margin for O/U market
    df['Margin_OU2.5'] = df['Prob_Over2.5'] + df['Prob_Under2.5'] - 1
    
    # Market expected goals (simplified approximation)
    # Higher over probability suggests more goals expected
    df['Market_Expected_Goals'] = 2.5 + (df['Prob_Over2.5'] - df['Prob_Under2.5']) * 2
    
    return df


def generate_team_form_features(df, n_matches=5):
    """Generate rolling form features for each team"""
    print(f"Generating team form features (last {n_matches} matches)...")
    
    # Sort by date and league
    df = df.sort_values(['League', 'Date']).reset_index(drop=True)
    
    # Initialize form columns (basic + advanced)
    form_columns = [
        'Home_Avg_Goals_Scored_Last5', 'Home_Avg_Goals_Conceded_Last5',
        'Home_Form_Points_Last5', 'Home_Win_Ratio_Last5',
        'Away_Avg_Goals_Scored_Last5', 'Away_Avg_Goals_Conceded_Last5',
        'Away_Form_Points_Last5', 'Away_Win_Ratio_Last5',
        'Home_Form_Consistency_Last5', 'Home_Weighted_Form_Points_Last5',
        'Home_Clean_Sheet_Ratio_Last5',
        'Away_Form_Consistency_Last5', 'Away_Weighted_Form_Points_Last5',
        'Away_Clean_Sheet_Ratio_Last5'
    ]
    
    for col in form_columns:
        df[col] = np.nan
    
    # Calculate form for each team
    teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique()
    
    for team in teams:
        # Get all matches for this team
        home_matches = df[df['HomeTeam'] == team].copy()
        away_matches = df[df['AwayTeam'] == team].copy()
        
        # Process home matches
        for idx in home_matches.index:
            # Get previous N matches for this team (both home and away)
            prev_home = df[(df['HomeTeam'] == team) & (df.index < idx) & (df['League'] == df.loc[idx, 'League'])].tail(n_matches)
            prev_away = df[(df['AwayTeam'] == team) & (df.index < idx) & (df['League'] == df.loc[idx, 'League'])].tail(n_matches)
            
            # Combine and get last N matches
            all_prev = pd.concat([
                prev_home[['Date', 'FTHG', 'FTAG', 'FT_Result']].assign(Location='Home'),
                prev_away[['Date', 'FTHG', 'FTAG', 'FT_Result']].assign(Location='Away')
            ]).sort_values('Date').tail(n_matches)
            
            if len(all_prev) > 0:
                # Calculate goals scored and conceded
                goals_scored = []
                goals_conceded = []
                points = []
                wins = []
                
                for _, match in all_prev.iterrows():
                    if match['Location'] == 'Home':
                        goals_scored.append(match['FTHG'])
                        goals_conceded.append(match['FTAG'])
                        if match['FT_Result'] == 0:  # Home win
                            points.append(3)
                            wins.append(1)
                        elif match['FT_Result'] == 1:  # Draw
                            points.append(1)
                            wins.append(0)
                        else:  # Loss
                            points.append(0)
                            wins.append(0)
                    else:  # Away
                        goals_scored.append(match['FTAG'])
                        goals_conceded.append(match['FTHG'])
                        if match['FT_Result'] == 2:  # Away win
                            points.append(3)
                            wins.append(1)
                        elif match['FT_Result'] == 1:  # Draw
                            points.append(1)
                            wins.append(0)
                        else:  # Loss
                            points.append(0)
                            wins.append(0)
                
                df.loc[idx, 'Home_Avg_Goals_Scored_Last5'] = np.mean(goals_scored)
                df.loc[idx, 'Home_Avg_Goals_Conceded_Last5'] = np.mean(goals_conceded)
                df.loc[idx, 'Home_Form_Points_Last5'] = np.sum(points)
                df.loc[idx, 'Home_Win_Ratio_Last5'] = np.mean(wins)
                
                # Advanced form features
                # Form consistency: standard deviation of points (lower = more consistent)
                df.loc[idx, 'Home_Form_Consistency_Last5'] = np.std(points) if len(points) > 1 else 0
                
                # Weighted form: recent matches count more (weights: [1, 2, 3, 4, 5])
                weights = np.arange(1, len(points) + 1)
                df.loc[idx, 'Home_Weighted_Form_Points_Last5'] = np.average(points, weights=weights)
                
                # Clean sheet ratio
                clean_sheets = sum(1 for g in goals_conceded if g == 0)
                df.loc[idx, 'Home_Clean_Sheet_Ratio_Last5'] = clean_sheets / len(goals_conceded)
        
        # Process away matches
        for idx in away_matches.index:
            # Get previous N matches for this team (both home and away)
            prev_home = df[(df['HomeTeam'] == team) & (df.index < idx) & (df['League'] == df.loc[idx, 'League'])].tail(n_matches)
            prev_away = df[(df['AwayTeam'] == team) & (df.index < idx) & (df['League'] == df.loc[idx, 'League'])].tail(n_matches)
            
            # Combine and get last N matches
            all_prev = pd.concat([
                prev_home[['Date', 'FTHG', 'FTAG', 'FT_Result']].assign(Location='Home'),
                prev_away[['Date', 'FTHG', 'FTAG', 'FT_Result']].assign(Location='Away')
            ]).sort_values('Date').tail(n_matches)
            
            if len(all_prev) > 0:
                # Calculate goals scored and conceded
                goals_scored = []
                goals_conceded = []
                points = []
                wins = []
                
                for _, match in all_prev.iterrows():
                    if match['Location'] == 'Home':
                        goals_scored.append(match['FTHG'])
                        goals_conceded.append(match['FTAG'])
                        if match['FT_Result'] == 0:  # Home win
                            points.append(3)
                            wins.append(1)
                        elif match['FT_Result'] == 1:  # Draw
                            points.append(1)
                            wins.append(0)
                        else:  # Loss
                            points.append(0)
                            wins.append(0)
                    else:  # Away
                        goals_scored.append(match['FTAG'])
                        goals_conceded.append(match['FTHG'])
                        if match['FT_Result'] == 2:  # Away win
                            points.append(3)
                            wins.append(1)
                        elif match['FT_Result'] == 1:  # Draw
                            points.append(1)
                            wins.append(0)
                        else:  # Loss
                            points.append(0)
                            wins.append(0)
                
                df.loc[idx, 'Away_Avg_Goals_Scored_Last5'] = np.mean(goals_scored)
                df.loc[idx, 'Away_Avg_Goals_Conceded_Last5'] = np.mean(goals_conceded)
                df.loc[idx, 'Away_Form_Points_Last5'] = np.sum(points)
                df.loc[idx, 'Away_Win_Ratio_Last5'] = np.mean(wins)
                
                # Advanced form features
                # Form consistency: standard deviation of points (lower = more consistent)
                df.loc[idx, 'Away_Form_Consistency_Last5'] = np.std(points) if len(points) > 1 else 0
                
                # Weighted form: recent matches count more (weights: [1, 2, 3, 4, 5])
                weights = np.arange(1, len(points) + 1)
                df.loc[idx, 'Away_Weighted_Form_Points_Last5'] = np.average(points, weights=weights)
                
                # Clean sheet ratio
                clean_sheets = sum(1 for g in goals_conceded if g == 0)
                df.loc[idx, 'Away_Clean_Sheet_Ratio_Last5'] = clean_sheets / len(goals_conceded)
    
    # Form differences
    df['Goal_Diff_Form'] = (df['Home_Avg_Goals_Scored_Last5'] - df['Home_Avg_Goals_Conceded_Last5']) - \
                           (df['Away_Avg_Goals_Scored_Last5'] - df['Away_Avg_Goals_Conceded_Last5'])
    df['Points_Diff_Form'] = df['Home_Form_Points_Last5'] - df['Away_Form_Points_Last5']
    
    return df


def generate_h2h_features(df, n_matches=5):
    """Generate head-to-head features between teams"""
    print(f"Generating head-to-head features (last {n_matches} H2H matches)...")
    
    df = df.sort_values(['League', 'Date']).reset_index(drop=True)
    
    # Initialize H2H columns
    df['H2H_Avg_Goal_Diff'] = np.nan
    df['H2H_Recent_Win_Ratio'] = np.nan
    
    for idx in df.index:
        home_team = df.loc[idx, 'HomeTeam']
        away_team = df.loc[idx, 'AwayTeam']
        league = df.loc[idx, 'League']
        current_date = df.loc[idx, 'Date']
        
        # Get previous H2H matches in same league
        h2h_matches = df[
            (df['League'] == league) &
            (df['Date'] < current_date) &
            (
                ((df['HomeTeam'] == home_team) & (df['AwayTeam'] == away_team)) |
                ((df['HomeTeam'] == away_team) & (df['AwayTeam'] == home_team))
            )
        ].tail(n_matches)
        
        if len(h2h_matches) > 0:
            goal_diffs = []
            home_wins = []
            
            for _, match in h2h_matches.iterrows():
                if match['HomeTeam'] == home_team:
                    # Current home team was home in this H2H match
                    goal_diff = match['FTHG'] - match['FTAG']
                    home_wins.append(1 if match['FT_Result'] == 0 else 0)
                else:
                    # Current home team was away in this H2H match
                    goal_diff = match['FTAG'] - match['FTHG']
                    home_wins.append(1 if match['FT_Result'] == 2 else 0)
                
                goal_diffs.append(goal_diff)
            
            df.loc[idx, 'H2H_Avg_Goal_Diff'] = np.mean(goal_diffs)
            df.loc[idx, 'H2H_Recent_Win_Ratio'] = np.mean(home_wins)
    
    return df


def generate_advanced_context_features(df):
    """Generate advanced contextual features"""
    print("Generating advanced context features...")
    
    # Days since last match (average of home and away)
    df['Days_Since_Last_Match'] = (df['Home_Days_Since_Last'] + df['Away_Days_Since_Last']) / 2
    
    # Market volatility: Odds disagreement
    # Higher values indicate more uncertainty/disagreement in the market
    df['Odds_Disagreement'] = df[['HomeOdds', 'DrawOdds', 'AwayOdds']].std(axis=1)
    
    # Simplified Elo-like difference based on form and odds
    # Positive = home team stronger, Negative = away team stronger
    df['Elo_Difference'] = (
        (df['Home_Form_Points_Last5'] - df['Away_Form_Points_Last5']) * 10 +
        (df['Prob_Home'] - df['Prob_Away']) * 100
    )
    
    return df


def generate_inplay_enhanced_features(df):
    """Generate enhanced in-play features for halftime prediction"""
    print("Generating enhanced in-play features...")
    
    # Comeback status: Is the team that's behind at HT trying to comeback?
    df['Comeback_Status'] = np.where(
        df['HT_Goal_Diff'] == 0, 0,  # No comeback needed (level)
        np.where(df['HT_Goal_Diff'] > 0, 1,  # Home leading
                 2)  # Away leading
    )
    
    # First goal timing bucket
    # 0 = No goals in first half, 1 = Goals in first half
    df['First_Goal_Timing_Bucket'] = np.where(
        (df['HTHG'] == 0) & (df['HTAG'] == 0), 0, 1
    )
    
    return df


def generate_halftime_features(df):
    """Generate features related to halftime state"""
    print("Generating halftime features...")
    
    # Goal difference at halftime
    df['HT_Goal_Diff'] = df['HTHG'] - df['HTAG']
    
    # Both teams to score at halftime
    df['HT_BTTS'] = ((df['HTHG'] > 0) & (df['HTAG'] > 0)).astype(int)
    
    # Favorite status at halftime
    df['Favorite_Winning_HT'] = np.where(
        df['Home_Is_Favorite'] == 1,
        (df['HTHG'] > df['HTAG']).astype(int),
        (df['HTAG'] > df['HTHG']).astype(int)
    )
    
    # Comeback required
    df['Comeback_Required'] = ((df['HT_Goal_Diff'] < 0) & (df['FTHG'] > df['FTAG'])).astype(int) | \
                              ((df['HT_Goal_Diff'] > 0) & (df['FTHG'] < df['FTAG'])).astype(int)
    
    # Halftime score encoded (for embedding)
    df['HT_Score_Encoded'] = df['HTHG'].astype(str) + '-' + df['HTAG'].astype(str)
    
    return df


def generate_match_context_features(df):
    """Generate contextual match features"""
    print("Generating match context features...")
    
    # Days since last match for each team
    df = df.sort_values(['League', 'Date']).reset_index(drop=True)
    
    df['Home_Days_Since_Last'] = np.nan
    df['Away_Days_Since_Last'] = np.nan
    
    teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique()
    
    for team in teams:
        # Home matches
        home_matches = df[df['HomeTeam'] == team].copy()
        for i, idx in enumerate(home_matches.index):
            if i > 0:
                prev_idx = home_matches.index[i-1]
                days_diff = (df.loc[idx, 'Date'] - df.loc[prev_idx, 'Date']).days
                df.loc[idx, 'Home_Days_Since_Last'] = days_diff
        
        # Away matches
        away_matches = df[df['AwayTeam'] == team].copy()
        for i, idx in enumerate(away_matches.index):
            if i > 0:
                prev_idx = away_matches.index[i-1]
                days_diff = (df.loc[idx, 'Date'] - df.loc[prev_idx, 'Date']).days
                df.loc[idx, 'Away_Days_Since_Last'] = days_diff
    
    # Total goals in match
    df['Total_Goals'] = df['FTHG'] + df['FTAG']
    
    # Both teams to score
    df['BTTS'] = ((df['FTHG'] > 0) & (df['FTAG'] > 0)).astype(int)
    
    # Clean sheets
    df['Home_Clean_Sheet'] = (df['FTAG'] == 0).astype(int)
    df['Away_Clean_Sheet'] = (df['FTHG'] == 0).astype(int)
    
    return df


def main():
    """Main execution function"""
    print("="*80)
    print("SOCCER MATCH PREDICTION - FEATURE ENGINEERING")
    print("="*80)
    
    # Get script directory for relative paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load and parse data (from script directory)
    input_file = os.path.join(script_dir, 'fikstur_tum_ligler_all_seasons.csv')
    df = load_and_parse_data(input_file)
    
    # Generate all feature categories
    df = generate_odds_features(df)
    df = generate_goal_market_features(df)
    df = generate_halftime_features(df)
    df = generate_match_context_features(df)
    df = generate_team_form_features(df, n_matches=5)
    df = generate_h2h_features(df, n_matches=5)
    df = generate_advanced_context_features(df)
    df = generate_inplay_enhanced_features(df)
    
    # Remove rows with missing target variables
    print("\nCleaning data...")
    initial_rows = len(df)
    df = df.dropna(subset=['FTHG', 'FTAG', 'HTHG', 'HTAG'])
    print(f"Removed {initial_rows - len(df)} rows with missing scores")
    
    # Save the enriched dataset (to script directory)
    output_file = os.path.join(script_dir, 'output.csv')
    df.to_csv(output_file, index=False)
    print(f"\n{'='*80}")
    print(f"✓ Feature engineering complete!")
    print(f"✓ Enriched dataset saved to: {output_file}")
    print(f"✓ Total matches: {len(df)}")
    print(f"✓ Total features: {len(df.columns)}")
    print(f"{'='*80}")
    
    # Display summary
    print("\n" + "="*80)
    print("FEATURE SUMMARY")
    print("="*80)
    
    feature_groups = {
        'Original Data': ['Season', 'League', 'Week', 'Date', 'Code', 'HomeTeam', 'AwayTeam'],
        'Scores & Results': ['FTHG', 'FTAG', 'HTHG', 'HTAG', 'FT_Result', 'HT_Result', 'Total_Goals'],
        'Betting Odds': ['HomeOdds', 'DrawOdds', 'AwayOdds', 'Under2.5', 'Over2.5'],
        'Odds-Derived': ['Prob_Home', 'Prob_Draw', 'Prob_Away', 'Margin', 'Entropy', 
                        'Favorite_Odds', 'Mismatch_Ratio', 'Home_Is_Favorite'],
        'Goal Market': ['Prob_Over2.5', 'Prob_Under2.5', 'Margin_OU2.5', 'Market_Expected_Goals'],
        'Basic Team Form (Last 5)': ['Home_Avg_Goals_Scored_Last5', 'Home_Avg_Goals_Conceded_Last5',
                               'Home_Form_Points_Last5', 'Home_Win_Ratio_Last5',
                               'Away_Avg_Goals_Scored_Last5', 'Away_Avg_Goals_Conceded_Last5',
                               'Away_Form_Points_Last5', 'Away_Win_Ratio_Last5'],
        'Advanced Team Form': ['Home_Form_Consistency_Last5', 'Home_Weighted_Form_Points_Last5',
                              'Home_Clean_Sheet_Ratio_Last5', 'Away_Form_Consistency_Last5',
                              'Away_Weighted_Form_Points_Last5', 'Away_Clean_Sheet_Ratio_Last5'],
        'Form Differences': ['Goal_Diff_Form', 'Points_Diff_Form'],
        'Head-to-Head (H2H)': ['H2H_Avg_Goal_Diff', 'H2H_Recent_Win_Ratio'],
        'Advanced Context': ['Days_Since_Last_Match', 'Odds_Disagreement', 'Elo_Difference'],
        'Halftime Features': ['HT_Goal_Diff', 'HT_BTTS', 'Favorite_Winning_HT', 
                             'Comeback_Required', 'HT_Score_Encoded'],
        'In-Play Enhanced': ['Comeback_Status', 'First_Goal_Timing_Bucket'],
        'Match Context': ['Home_Days_Since_Last', 'Away_Days_Since_Last', 'BTTS',
                         'Home_Clean_Sheet', 'Away_Clean_Sheet']
    }
    
    for group, features in feature_groups.items():
        available = [f for f in features if f in df.columns]
        print(f"\n{group}: {len(available)} features")
        for feat in available:
            print(f"  - {feat}")
    
    # Data quality report
    print("\n" + "="*80)
    print("DATA QUALITY REPORT")
    print("="*80)
    
    print(f"\nTotal matches: {len(df)}")
    print(f"Leagues: {df['League'].nunique()}")
    print(f"Teams: {pd.concat([df['HomeTeam'], df['AwayTeam']]).nunique()}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    print("\nMissing values by feature group:")
    for group, features in feature_groups.items():
        available = [f for f in features if f in df.columns]
        if available:
            missing_pct = df[available].isna().sum().sum() / (len(df) * len(available)) * 100
            print(f"  {group}: {missing_pct:.1f}% missing")
    
    print("\nTarget variable distribution:")
    result_map = {0: 'Home Win', 1: 'Draw', 2: 'Away Win'}
    for result, label in result_map.items():
        count = (df['FT_Result'] == result).sum()
        pct = count / len(df) * 100
        print(f"  {label}: {count} ({pct:.1f}%)")
    
    print("\n" + "="*80)
    print("Sample of enriched data:")
    print("="*80)
    print(df[['HomeTeam', 'AwayTeam', 'FT_Score', 'HomeOdds', 'DrawOdds', 'AwayOdds', 
              'Prob_Home', 'Entropy', 'Market_Expected_Goals']].head(10).to_string())
    
    print("\n" + "="*80)
    print("✓ Processing complete! Ready for model training.")
    print("="*80)


if __name__ == "__main__":
    main()
