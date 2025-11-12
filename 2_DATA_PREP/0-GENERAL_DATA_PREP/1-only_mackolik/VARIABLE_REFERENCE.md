# Variable Reference Guide

**Dataset**: Soccer Match Prediction  
**Total Variables**: 73  
**Last Updated**: November 9, 2025

---

## Quick Reference

### Variable Availability
- **Pre-Match Variables**: 60 (available before kickoff)
- **Halftime Variables**: 10 (available at halftime)
- **Post-Match Variables**: 3 (target variables only)

### Variable Types
- **Numerical (Continuous)**: 52
- **Categorical**: 15
- **Binary**: 6

---

## Complete Variable Reference Table

| # | Variable Name | Type | Data Type | Availability | Model Input | Target | Description | Value Range | Missing % |
|---|--------------|------|-----------|--------------|-------------|--------|-------------|-------------|-----------|
| 1 | Season | Categorical | String | Pre-Match | Metadata | No | Season identifier (e.g., "2022/2023") | Categorical | 0.0% |
| 2 | League | Categorical | String | Pre-Match | Dense/OHE | No | League name | Categorical | 0.0% |
| 3 | Week | Numerical | Integer | Pre-Match | Dense | No | Match week number | 1-38 | 0.0% |
| 4 | Date | Datetime | DateTime | Pre-Match | Metadata | No | Match date | 2022-2025 | 0.0% |
| 5 | Code | Categorical | String | Pre-Match | Metadata | No | Match code (usually "MS") | Categorical | 0.0% |
| 6 | HomeTeam | Categorical | String | Pre-Match | Metadata/Emb | No | Home team name | Categorical | 0.0% |
| 7 | AwayTeam | Categorical | String | Pre-Match | Metadata/Emb | No | Away team name | Categorical | 0.0% |
| 8 | FT_Score | Categorical | String | Post-Match | No | No | Full-time score string (e.g., "2-1") | Format: "X-Y" | 0.0% |
| 9 | HT_Score | Categorical | String | Halftime | No | No | Half-time score string (e.g., "1-0") | Format: "X-Y" | 0.0% |
| 10 | HomeOdds | Numerical | Float | Pre-Match | Dense/Emb | No | Home win odds | 1.01-50.0 | 1.3% |
| 11 | DrawOdds | Numerical | Float | Pre-Match | Dense/Emb | No | Draw odds | 2.0-20.0 | 0.2% |
| 12 | AwayOdds | Numerical | Float | Pre-Match | Dense/Emb | No | Away win odds | 1.01-50.0 | 0.3% |
| 13 | HomeDrawOdds | Numerical | Float | Pre-Match | Dense | No | Double chance: Home or Draw | 1.0-10.0 | High |
| 14 | HomeAwayOdds | Numerical | Float | Pre-Match | Dense | No | Double chance: Home or Away | 1.0-5.0 | High |
| 15 | AwayDrawOdds | Numerical | Float | Pre-Match | Dense | No | Double chance: Away or Draw | 1.0-10.0 | High |
| 16 | Under2.5 | Numerical | Float | Pre-Match | Dense | No | Under 2.5 goals odds | 1.1-5.0 | 0.7% |
| 17 | Over2.5 | Numerical | Float | Pre-Match | Dense | No | Over 2.5 goals odds | 1.1-5.0 | 0.7% |
| 18 | FTHG | Numerical | Integer | Post-Match | No | Yes | Full-time home goals | 0-10 | 0.0% |
| 19 | FTAG | Numerical | Integer | Post-Match | No | Yes | Full-time away goals | 0-10 | 0.0% |
| 20 | HTHG | Numerical | Integer | Halftime | Dense | Yes* | Half-time home goals | 0-6 | 0.0% |
| 21 | HTAG | Numerical | Integer | Halftime | Dense | Yes* | Half-time away goals | 0-6 | 0.0% |
| 22 | FT_Result | Categorical | Integer | Post-Match | No | Yes | Full-time result (0=H, 1=D, 2=A) | 0, 1, 2 | 0.0% |
| 23 | HT_Result | Categorical | Integer | Halftime | Dense | Yes* | Half-time result (0=H, 1=D, 2=A) | 0, 1, 2 | 0.0% |
| 24 | Prob_Home | Numerical | Float | Pre-Match | Dense | No | Implied probability of home win | 0.0-1.0 | 0.6% |
| 25 | Prob_Draw | Numerical | Float | Pre-Match | Dense | No | Implied probability of draw | 0.0-1.0 | 0.6% |
| 26 | Prob_Away | Numerical | Float | Pre-Match | Dense | No | Implied probability of away win | 0.0-1.0 | 0.6% |
| 27 | Margin | Numerical | Float | Pre-Match | Dense | No | Bookmaker margin (overround) | 0.0-0.2 | 0.6% |
| 28 | True_Prob_Home | Numerical | Float | Pre-Match | Dense | No | Margin-adjusted home win prob | 0.0-1.0 | 0.6% |
| 29 | True_Prob_Draw | Numerical | Float | Pre-Match | Dense | No | Margin-adjusted draw prob | 0.0-1.0 | 0.6% |
| 30 | True_Prob_Away | Numerical | Float | Pre-Match | Dense | No | Margin-adjusted away win prob | 0.0-1.0 | 0.6% |
| 31 | Entropy | Numerical | Float | Pre-Match | Dense | No | Market uncertainty measure | 0.0-1.6 | 0.6% |
| 32 | Favorite_Odds | Numerical | Float | Pre-Match | Dense | No | Lower of home/away odds | 1.01-20.0 | 0.6% |
| 33 | Underdog_Odds | Numerical | Float | Pre-Match | Dense | No | Higher of home/away odds | 1.01-50.0 | 0.6% |
| 34 | Mismatch_Ratio | Numerical | Float | Pre-Match | Dense | No | Underdog odds / Favorite odds | 1.0-30.0 | 0.6% |
| 35 | Home_Is_Favorite | Binary | Integer | Pre-Match | Dense | No | Is home team favorite? (1=Yes, 0=No) | 0, 1 | 0.6% |
| 36 | Prob_Over2.5 | Numerical | Float | Pre-Match | Dense | No | Probability of over 2.5 goals | 0.0-1.0 | 0.7% |
| 37 | Prob_Under2.5 | Numerical | Float | Pre-Match | Dense | No | Probability of under 2.5 goals | 0.0-1.0 | 0.7% |
| 38 | Margin_OU2.5 | Numerical | Float | Pre-Match | Dense | No | Over/Under market margin | 0.0-0.2 | 0.7% |
| 39 | Market_Expected_Goals | Numerical | Float | Pre-Match | Dense | No | Market's expected total goals | 1.0-5.0 | 0.7% |
| 40 | HT_Goal_Diff | Numerical | Integer | Halftime | Dense | No | Half-time goal difference (home - away) | -6 to +6 | 0.0% |
| 41 | HT_BTTS | Binary | Integer | Halftime | Dense | No | Both teams scored at HT? (1=Yes, 0=No) | 0, 1 | 0.0% |
| 42 | Favorite_Winning_HT | Binary | Integer | Halftime | Dense | No | Is favorite winning at HT? (1=Yes, 0=No) | 0, 1 | 0.0% |
| 43 | Comeback_Required | Binary | Integer | Post-Match | No | No | Was comeback from HT deficit? (1=Yes, 0=No) | 0, 1 | 0.0% |
| 44 | HT_Score_Encoded | Categorical | String | Halftime | Embedding | No | Half-time score for embedding (e.g., "1-0") | Format: "X-Y" | 0.0% |
| 45 | Home_Days_Since_Last | Numerical | Float | Pre-Match | Dense | No | Days since home team's last match | 0-90 | 2.0% |
| 46 | Away_Days_Since_Last | Numerical | Float | Pre-Match | Dense | No | Days since away team's last match | 0-90 | 2.0% |
| 47 | Total_Goals | Numerical | Integer | Post-Match | No | No | Total goals in match | 0-15 | 0.0% |
| 48 | BTTS | Binary | Integer | Post-Match | No | No | Both teams scored? (1=Yes, 0=No) | 0, 1 | 0.0% |
| 49 | Home_Clean_Sheet | Binary | Integer | Post-Match | No | No | Home team clean sheet? (1=Yes, 0=No) | 0, 1 | 0.0% |
| 50 | Away_Clean_Sheet | Binary | Integer | Post-Match | No | No | Away team clean sheet? (1=Yes, 0=No) | 0, 1 | 0.0% |
| 51 | Home_Avg_Goals_Scored_Last5 | Numerical | Float | Pre-Match | Dense | No | Home team avg goals scored (last 5) | 0.0-5.0 | 1.2% |
| 52 | Home_Avg_Goals_Conceded_Last5 | Numerical | Float | Pre-Match | Dense | No | Home team avg goals conceded (last 5) | 0.0-5.0 | 1.2% |
| 53 | Home_Form_Points_Last5 | Numerical | Integer | Pre-Match | Dense | No | Home team total points (last 5) | 0-15 | 1.2% |
| 54 | Home_Win_Ratio_Last5 | Numerical | Float | Pre-Match | Dense | No | Home team win ratio (last 5) | 0.0-1.0 | 1.2% |
| 55 | Away_Avg_Goals_Scored_Last5 | Numerical | Float | Pre-Match | Dense | No | Away team avg goals scored (last 5) | 0.0-5.0 | 1.2% |
| 56 | Away_Avg_Goals_Conceded_Last5 | Numerical | Float | Pre-Match | Dense | No | Away team avg goals conceded (last 5) | 0.0-5.0 | 1.2% |
| 57 | Away_Form_Points_Last5 | Numerical | Integer | Pre-Match | Dense | No | Away team total points (last 5) | 0-15 | 1.2% |
| 58 | Away_Win_Ratio_Last5 | Numerical | Float | Pre-Match | Dense | No | Away team win ratio (last 5) | 0.0-1.0 | 1.2% |
| 59 | Home_Form_Consistency_Last5 | Numerical | Float | Pre-Match | Dense | No | Std dev of points (last 5) - lower is better | 0.0-2.0 | 1.2% |
| 60 | Home_Weighted_Form_Points_Last5 | Numerical | Float | Pre-Match | Dense | No | Weighted avg points (recent weighted more) | 0.0-3.0 | 1.2% |
| 61 | Home_Clean_Sheet_Ratio_Last5 | Numerical | Float | Pre-Match | Dense | No | Proportion of clean sheets (last 5) | 0.0-1.0 | 1.2% |
| 62 | Away_Form_Consistency_Last5 | Numerical | Float | Pre-Match | Dense | No | Std dev of points (last 5) - lower is better | 0.0-2.0 | 1.2% |
| 63 | Away_Weighted_Form_Points_Last5 | Numerical | Float | Pre-Match | Dense | No | Weighted avg points (recent weighted more) | 0.0-3.0 | 1.2% |
| 64 | Away_Clean_Sheet_Ratio_Last5 | Numerical | Float | Pre-Match | Dense | No | Proportion of clean sheets (last 5) | 0.0-1.0 | 1.2% |
| 65 | Goal_Diff_Form | Numerical | Float | Pre-Match | Dense | No | Difference in goal diff form (home - away) | -10.0 to +10.0 | 1.4% |
| 66 | Points_Diff_Form | Numerical | Integer | Pre-Match | Dense | No | Difference in points (last 5) | -15 to +15 | 1.4% |
| 67 | H2H_Avg_Goal_Diff | Numerical | Float | Pre-Match | Dense | No | Avg goal diff in recent H2H (home perspective) | -5.0 to +5.0 | 25.7% |
| 68 | H2H_Recent_Win_Ratio | Numerical | Float | Pre-Match | Dense | No | Home team win ratio in recent H2H | 0.0-1.0 | 25.7% |
| 69 | Days_Since_Last_Match | Numerical | Float | Pre-Match | Dense | No | Average rest days for both teams | 0-90 | 2.0% |
| 70 | Odds_Disagreement | Numerical | Float | Pre-Match | Dense | No | Std dev of 1X2 odds (market uncertainty) | 0.0-10.0 | 0.6% |
| 71 | Elo_Difference | Numerical | Float | Pre-Match | Dense | No | Simplified Elo-like rating diff (form+odds) | -200 to +200 | 2.0% |
| 72 | Comeback_Status | Categorical | Integer | Halftime | Dense | No | Match state at HT (0=Level, 1=Home lead, 2=Away lead) | 0, 1, 2 | 0.0% |
| 73 | First_Goal_Timing_Bucket | Binary | Integer | Halftime | Dense | No | First goal in 1st half? (0=No goals, 1=Goals) | 0, 1 | 0.0% |

---

## Variable Categories

### 1. Metadata Variables (Not Used as Model Features)
Variables used for reference, joining, or filtering but not for prediction.

| Variable | Purpose | Usage |
|----------|---------|-------|
| Season | Temporal reference | Train/test splitting, stratification |
| Date | Temporal ordering | Sorting, time-based validation |
| Code | Match identifier | Data quality checks |
| HomeTeam | Team identifier | Can be used as embedding input |
| AwayTeam | Team identifier | Can be used as embedding input |
| FT_Score | Human-readable result | Display purposes only |
| HT_Score | Human-readable HT state | Display purposes only |

### 2. Pre-Match Features (Available Before Kickoff)
**Count**: 60 features  
**Use Case**: Scenario 1 (Pre-Match Prediction Model)

#### 2.1 Betting Market Features (12 features)
- Core Odds: `HomeOdds`, `DrawOdds`, `AwayOdds`
- Double Chance: `HomeDrawOdds`, `HomeAwayOdds`, `AwayDrawOdds`
- Goal Markets: `Under2.5`, `Over2.5`
- Derived: `Prob_Home`, `Prob_Draw`, `Prob_Away`, `Margin`

**Model Usage**: Dense input + Embedding for core odds

#### 2.2 Market Intelligence Features (9 features)
- Probabilities: `True_Prob_Home`, `True_Prob_Draw`, `True_Prob_Away`
- Uncertainty: `Entropy`, `Odds_Disagreement`
- Strength: `Favorite_Odds`, `Underdog_Odds`, `Mismatch_Ratio`
- Flag: `Home_Is_Favorite`

**Model Usage**: Dense input

#### 2.3 Goal Market Features (4 features)
- `Prob_Over2.5`, `Prob_Under2.5`
- `Margin_OU2.5`, `Market_Expected_Goals`

**Model Usage**: Dense input

#### 2.4 Basic Form Features (8 features)
- Goals: `Home_Avg_Goals_Scored_Last5`, `Home_Avg_Goals_Conceded_Last5`, `Away_Avg_Goals_Scored_Last5`, `Away_Avg_Goals_Conceded_Last5`
- Points: `Home_Form_Points_Last5`, `Away_Form_Points_Last5`
- Win Rate: `Home_Win_Ratio_Last5`, `Away_Win_Ratio_Last5`

**Model Usage**: Dense input

#### 2.5 Advanced Form Features (6 features)
- Consistency: `Home_Form_Consistency_Last5`, `Away_Form_Consistency_Last5`
- Weighted: `Home_Weighted_Form_Points_Last5`, `Away_Weighted_Form_Points_Last5`
- Defense: `Home_Clean_Sheet_Ratio_Last5`, `Away_Clean_Sheet_Ratio_Last5`

**Model Usage**: Dense input

#### 2.6 Form Comparison Features (2 features)
- `Goal_Diff_Form`, `Points_Diff_Form`

**Model Usage**: Dense input

#### 2.7 Head-to-Head Features (2 features)
- `H2H_Avg_Goal_Diff`, `H2H_Recent_Win_Ratio`

**Model Usage**: Dense input  
**Note**: 25.7% missing - requires sufficient matchup history

#### 2.8 Context Features (3 features)
- Rest: `Days_Since_Last_Match`
- Market: `Odds_Disagreement`
- Strength: `Elo_Difference`

**Model Usage**: Dense input

#### 2.9 Rest/Fatigue Features (2 features)
- `Home_Days_Since_Last`, `Away_Days_Since_Last`

**Model Usage**: Dense input

### 3. Halftime Features (Available at Half-Time)
**Count**: 10 features  
**Use Case**: Scenario 2 (In-Play Prediction Model)

#### 3.1 Halftime Scores (2 features)
- `HTHG`, `HTAG`

**Model Usage**: Dense input, Target (Scenario 1 only)

#### 3.2 Halftime State (5 features)
- Result: `HT_Result`
- Difference: `HT_Goal_Diff`
- Flags: `HT_BTTS`, `Favorite_Winning_HT`
- Encoded: `HT_Score_Encoded`

**Model Usage**: Dense input + Embedding for `HT_Score_Encoded`

#### 3.3 In-Play Enhanced (2 features)
- `Comeback_Status`, `First_Goal_Timing_Bucket`

**Model Usage**: Dense input

### 4. Post-Match Variables (Target Variables Only)
**Count**: 3 features  
**Use Case**: Prediction targets

| Variable | Type | Task | Loss Function |
|----------|------|------|---------------|
| FT_Result | Classification | 3-class | Categorical Crossentropy |
| FTHG | Regression | Count data | Poisson |
| FTAG | Regression | Count data | Poisson |

**Additional Targets (Scenario 1 only)**:
- `HT_Result` - Classification (3-class)
- `HTHG` - Regression (Poisson)
- `HTAG` - Regression (Poisson)

---

## Model Input Configuration

### Scenario 1: Pre-Match Prediction

#### Dense Input (Standard Neural Network Path)
- **Count**: ~55 features
- **All numerical and binary features** from pre-match category
- **Preprocessing**: StandardScaler
- **Missing Value Handling**: SimpleImputer (median strategy)

#### Embedding Input (For High-Cardinality Categories)
- `HomeOdds` → Embedding(vocab_size, embedding_dim)
- `DrawOdds` → Embedding(vocab_size, embedding_dim)
- `AwayOdds` → Embedding(vocab_size, embedding_dim)
- Optional: `HomeTeam`, `AwayTeam` → Team embeddings

#### One-Hot Encoding Input
- `League` → One-hot encoding (6 leagues)

#### Exclude from Scenario 1
All halftime and post-match features:
- `HTHG`, `HTAG`, `HT_Result`, `HT_Score`, `HT_Goal_Diff`, `HT_BTTS`, `Favorite_Winning_HT`, `HT_Score_Encoded`, `Comeback_Status`, `First_Goal_Timing_Bucket`
- `FTHG`, `FTAG`, `FT_Result`, `FT_Score`, `Total_Goals`, `BTTS`, `Home_Clean_Sheet`, `Away_Clean_Sheet`, `Comeback_Required`

### Scenario 2: In-Play (Halftime) Prediction

#### Dense Input
- **Count**: ~65 features
- **All pre-match features** + **halftime state features**
- **Preprocessing**: StandardScaler
- **Missing Value Handling**: SimpleImputer (median strategy)

#### Embedding Input
- All pre-match embeddings
- `HT_Score_Encoded` → Embedding(vocab_size_ht, embedding_dim)

#### Exclude from Scenario 2
Only post-match features (except targets):
- `FT_Score`, `Total_Goals`, `BTTS`, `Home_Clean_Sheet`, `Away_Clean_Sheet`, `Comeback_Required`

---

## Data Type Specifications

### For Pandas Loading
```python
dtype_spec = {
    # Categorical
    'Season': 'str',
    'League': 'str',
    'Code': 'str',
    'HomeTeam': 'str',
    'AwayTeam': 'str',
    'FT_Score': 'str',
    'HT_Score': 'str',
    'HT_Score_Encoded': 'str',
    
    # Integer
    'Week': 'Int64',
    'FTHG': 'Int64',
    'FTAG': 'Int64',
    'HTHG': 'Int64',
    'HTAG': 'Int64',
    'FT_Result': 'Int64',
    'HT_Result': 'Int64',
    'Home_Form_Points_Last5': 'Int64',
    'Away_Form_Points_Last5': 'Int64',
    'Points_Diff_Form': 'Int64',
    'Total_Goals': 'Int64',
    'HT_Goal_Diff': 'Int64',
    'Comeback_Status': 'Int64',
    
    # Binary (store as int)
    'Home_Is_Favorite': 'Int64',
    'HT_BTTS': 'Int64',
    'Favorite_Winning_HT': 'Int64',
    'Comeback_Required': 'Int64',
    'BTTS': 'Int64',
    'Home_Clean_Sheet': 'Int64',
    'Away_Clean_Sheet': 'Int64',
    'First_Goal_Timing_Bucket': 'Int64',
    
    # Float - all others
}

parse_dates = ['Date']
```

---

## Missing Value Patterns

### Expected Missing Values
| Feature | Missing % | Reason | Handling Strategy |
|---------|-----------|--------|-------------------|
| H2H_Avg_Goal_Diff | 25.7% | New matchups, insufficient history | Fill with 0 (neutral) or drop rows |
| H2H_Recent_Win_Ratio | 25.7% | New matchups, insufficient history | Fill with 0.5 (neutral) or drop rows |
| Form features | ~1.2% | First 5 matches of season | Drop rows or use league averages |
| Home_Days_Since_Last | ~2.0% | First match of season | Fill with median or drop |
| Away_Days_Since_Last | ~2.0% | First match of season | Fill with median or drop |
| Betting odds | <1.3% | Odds not available | Drop rows (critical features) |

### Unexpected Missing Values (Should Investigate)
Any missing values in:
- Target variables (`FTHG`, `FTAG`, `FT_Result`, etc.)
- Core features (`League`, `HomeTeam`, `AwayTeam`, `Date`)

---

## Feature Scaling Requirements

### Requires Scaling (StandardScaler)
All numerical features except:
- Binary features (already 0/1)
- Probabilities (already 0-1)
- Count features used as targets

### Does Not Require Scaling
- Binary features: `Home_Is_Favorite`, `HT_BTTS`, `Favorite_Winning_HT`, etc.
- Probability features: `Prob_Home`, `Prob_Draw`, `Prob_Away`, `True_Prob_*`
- Ratio features: `Home_Win_Ratio_Last5`, `Away_Win_Ratio_Last5`, `H2H_Recent_Win_Ratio`

### Categorical Encoding Required
- **One-Hot**: `League` (6 categories)
- **Label Encoding + Embedding**: `HomeOdds`, `DrawOdds`, `AwayOdds`, `HT_Score_Encoded`
- **Optional Team Embedding**: `HomeTeam`, `AwayTeam` (149 teams)

---

## Feature Importance Guidelines

### Expected High-Importance Features
Based on domain knowledge and typical ML patterns:

**Tier 1 (Critical)**:
- `HomeOdds`, `DrawOdds`, `AwayOdds`
- `Prob_Home`, `Prob_Draw`, `Prob_Away`
- `Home_Form_Points_Last5`, `Away_Form_Points_Last5`

**Tier 2 (Very Important)**:
- `Goal_Diff_Form`, `Points_Diff_Form`
- `Market_Expected_Goals`
- `Entropy`, `Mismatch_Ratio`
- Halftime features (for Scenario 2)

**Tier 3 (Important)**:
- Advanced form features
- H2H features (when available)
- Context features

**Tier 4 (Supplementary)**:
- Double chance odds
- Individual rest days
- Consistency metrics

---

## Usage Examples

### Loading with Proper Types
```python
import pandas as pd

# Load with date parsing
df = pd.read_csv('output.csv', parse_dates=['Date'])

# Verify data types
print(df.dtypes)

# Check categorical unique values
print(f"Leagues: {df['League'].nunique()}")
print(f"Teams: {df['HomeTeam'].nunique() + df['AwayTeam'].nunique()}")
print(f"Seasons: {df['Season'].nunique()}")
```

### Feature Selection for Modeling
```python
# Pre-match features only (Scenario 1)
pre_match_features = [
    col for col in df.columns 
    if col not in [
        # Metadata
        'Season', 'Date', 'Code', 'HomeTeam', 'AwayTeam', 'FT_Score', 'HT_Score',
        # Halftime
        'HTHG', 'HTAG', 'HT_Result', 'HT_Goal_Diff', 'HT_BTTS', 
        'Favorite_Winning_HT', 'HT_Score_Encoded', 'Comeback_Status', 
        'First_Goal_Timing_Bucket',
        # Targets
        'FTHG', 'FTAG', 'FT_Result', 'Total_Goals', 'BTTS', 
        'Home_Clean_Sheet', 'Away_Clean_Sheet', 'Comeback_Required'
    ]
]

# Keep League for one-hot encoding
pre_match_features = ['League'] + [f for f in pre_match_features if f != 'League']

print(f"Pre-match features: {len(pre_match_features)}")
```

### Handling Missing Values
```python
# Strategy 1: Fill H2H with neutral values
df['H2H_Avg_Goal_Diff'] = df['H2H_Avg_Goal_Diff'].fillna(0)
df['H2H_Recent_Win_Ratio'] = df['H2H_Recent_Win_Ratio'].fillna(0.5)

# Strategy 2: Drop rows with missing critical features
critical_cols = ['HomeOdds', 'DrawOdds', 'AwayOdds', 
                 'Home_Form_Points_Last5', 'Away_Form_Points_Last5']
df_clean = df.dropna(subset=critical_cols)

print(f"Original: {len(df)}, After cleaning: {len(df_clean)}")
```

---

## Notes

### Temporal Considerations
- **Form features** use rolling calculations - only past matches included
- **H2H features** only use historical matchups before current match
- **No data leakage**: All features properly calculated with temporal awareness

### League-Specific Patterns
Different leagues may have different:
- Home advantage strength
- Average goals per match
- Market efficiency (odds accuracy)
- Season structure (38 vs 34 matches)

Consider league-specific normalization or stratification.

### Embedding Dimensions
Suggested embedding dimensions:
- **Odds** (continuous bucketed): 8-16 dimensions
- **HT_Score**: 16-32 dimensions (more variance)
- **Teams** (optional): 32-64 dimensions (149 teams)
- **League**: One-hot (only 6 categories)

---

**End of Variable Reference Guide**
