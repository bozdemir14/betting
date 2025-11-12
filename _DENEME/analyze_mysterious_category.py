"""
Comprehensive Analysis of Mysterious_category Predictive Performance
This script analyzes the predictive power of Mysterious_category for various match outcomes.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency, f_oneway, kruskal
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)


def parse_score(score_str):
    """Parse score string like '1-6' into home and away goals."""
    try:
        home, away = map(int, score_str.split('-'))
        return home, away
    except:
        return None, None


def calculate_cramers_v(chi2, n, r, c):
    """Calculate Cramér's V for effect size."""
    return np.sqrt(chi2 / (n * min(r - 1, c - 1)))


def load_and_prepare_data(filepath):
    """Load data and create all target variables."""
    print("=" * 80)
    print("LOADING AND PREPARING DATA")
    print("=" * 80)
    
    df = pd.read_csv(filepath)
    
    # Rename the last column to Mysterious_category if it's named '1'
    if '1' in df.columns:
        df = df.rename(columns={'1': 'Mysterious_category'})
    
    print(f"\nTotal matches: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Parse full-time scores
    df[['FT_Home_Goals', 'FT_Away_Goals']] = df['Skor'].apply(
        lambda x: pd.Series(parse_score(x))
    )
    
    # Parse half-time scores
    df[['HT_Home_Goals', 'HT_Away_Goals']] = df['IY_Skor'].apply(
        lambda x: pd.Series(parse_score(x))
    )
    
    # Remove rows with invalid scores
    df = df.dropna(subset=['FT_Home_Goals', 'FT_Away_Goals', 
                           'HT_Home_Goals', 'HT_Away_Goals'])
    
    print(f"Valid matches after parsing: {len(df)}")
    
    # FULL-TIME TARGET VARIABLES
    # 1. Winner (Home/Draw/Away)
    df['FT_Winner'] = df.apply(
        lambda row: 'Home' if row['FT_Home_Goals'] > row['FT_Away_Goals']
        else ('Away' if row['FT_Home_Goals'] < row['FT_Away_Goals'] else 'Draw'),
        axis=1
    )
    
    # 2. Total goals
    df['FT_Total_Goals'] = df['FT_Home_Goals'] + df['FT_Away_Goals']
    
    # 3. Score difference (from home team perspective)
    df['FT_Score_Diff'] = df['FT_Home_Goals'] - df['FT_Away_Goals']
    
    # 4. Both teams to score
    df['FT_BTTS'] = ((df['FT_Home_Goals'] > 0) & (df['FT_Away_Goals'] > 0)).astype(int)
    
    # 5. Home team win to nil
    df['FT_Home_Win_To_Nil'] = ((df['FT_Home_Goals'] > df['FT_Away_Goals']) & 
                                  (df['FT_Away_Goals'] == 0)).astype(int)
    
    # 6. Away team win to nil
    df['FT_Away_Win_To_Nil'] = ((df['FT_Away_Goals'] > df['FT_Home_Goals']) & 
                                  (df['FT_Home_Goals'] == 0)).astype(int)
    
    # 7. Exact score (for distribution analysis)
    df['FT_Exact_Score'] = df['Skor']
    
    # HALF-TIME TARGET VARIABLES
    # 1. HT Winner
    df['HT_Winner'] = df.apply(
        lambda row: 'Home' if row['HT_Home_Goals'] > row['HT_Away_Goals']
        else ('Away' if row['HT_Home_Goals'] < row['HT_Away_Goals'] else 'Draw'),
        axis=1
    )
    
    # 2. HT Total goals
    df['HT_Total_Goals'] = df['HT_Home_Goals'] + df['HT_Away_Goals']
    
    # 3. HT Score difference
    df['HT_Score_Diff'] = df['HT_Home_Goals'] - df['HT_Away_Goals']
    
    # 4. HT Both teams to score
    df['HT_BTTS'] = ((df['HT_Home_Goals'] > 0) & (df['HT_Away_Goals'] > 0)).astype(int)
    
    # 5. HT Home team win to nil
    df['HT_Home_Win_To_Nil'] = ((df['HT_Home_Goals'] > df['HT_Away_Goals']) & 
                                  (df['HT_Away_Goals'] == 0)).astype(int)
    
    # 6. HT Away team win to nil
    df['HT_Away_Win_To_Nil'] = ((df['HT_Away_Goals'] > df['HT_Home_Goals']) & 
                                  (df['HT_Home_Goals'] == 0)).astype(int)
    
    # 7. HT Exact score
    df['HT_Exact_Score'] = df['IY_Skor']
    
    print(f"\nMysterous_category unique values: {df['Mysterious_category'].nunique()}")
    print(f"Sample categories: {df['Mysterious_category'].unique()[:10]}")
    
    return df


def analyze_categorical_outcome(df, predictor, outcome, outcome_name):
    """Perform chi-square test for categorical outcomes."""
    print(f"\n{'=' * 80}")
    print(f"ANALYZING: {outcome_name}")
    print(f"{'=' * 80}")
    
    # Create contingency table
    contingency = pd.crosstab(df[predictor], df[outcome])
    print(f"\nContingency Table:")
    print(contingency)
    
    # Perform chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency)
    
    # Calculate Cramér's V
    n = contingency.sum().sum()
    r, c = contingency.shape
    cramers_v = calculate_cramers_v(chi2, n, r, c)
    
    print(f"\nChi-Square Test Results:")
    print(f"  Chi-Square Statistic: {chi2:.4f}")
    print(f"  P-value: {p_value:.6f}")
    print(f"  Degrees of Freedom: {dof}")
    print(f"  Cramér's V (Effect Size): {cramers_v:.4f}")
    
    if p_value < 0.001:
        significance = "*** (Very Strong)"
    elif p_value < 0.01:
        significance = "** (Strong)"
    elif p_value < 0.05:
        significance = "* (Significant)"
    else:
        significance = "Not Significant"
    
    print(f"  Statistical Significance: {significance}")
    
    # Interpretation of Cramér's V
    if cramers_v < 0.1:
        effect = "Negligible"
    elif cramers_v < 0.3:
        effect = "Small"
    elif cramers_v < 0.5:
        effect = "Medium"
    else:
        effect = "Large"
    
    print(f"  Effect Size Interpretation: {effect}")
    
    # Calculate conditional probabilities
    print(f"\nConditional Probabilities (by {predictor}):")
    probs = pd.crosstab(df[predictor], df[outcome], normalize='index') * 100
    print(probs.round(2))
    
    return {
        'outcome': outcome_name,
        'chi2': chi2,
        'p_value': p_value,
        'cramers_v': cramers_v,
        'significance': significance,
        'effect_size': effect
    }


def analyze_continuous_outcome(df, predictor, outcome, outcome_name):
    """Perform ANOVA/Kruskal-Wallis test for continuous outcomes."""
    print(f"\n{'=' * 80}")
    print(f"ANALYZING: {outcome_name}")
    print(f"{'=' * 80}")
    
    # Group data by predictor
    groups = [group[outcome].values for name, group in df.groupby(predictor)]
    
    # Descriptive statistics
    print(f"\nDescriptive Statistics by {predictor}:")
    desc_stats = df.groupby(predictor)[outcome].agg(['count', 'mean', 'std', 'min', 'max'])
    print(desc_stats.round(3))
    
    # ANOVA test
    f_stat, p_value_anova = f_oneway(*groups)
    
    # Kruskal-Wallis test (non-parametric alternative)
    h_stat, p_value_kw = kruskal(*groups)
    
    print(f"\nANOVA Test Results:")
    print(f"  F-Statistic: {f_stat:.4f}")
    print(f"  P-value: {p_value_anova:.6f}")
    
    print(f"\nKruskal-Wallis Test Results (Non-parametric):")
    print(f"  H-Statistic: {h_stat:.4f}")
    print(f"  P-value: {p_value_kw:.6f}")
    
    # Effect size (Eta-squared)
    grand_mean = df[outcome].mean()
    ss_between = sum([len(group) * (group.mean() - grand_mean)**2 for group in groups])
    ss_total = sum([(x - grand_mean)**2 for group in groups for x in group])
    eta_squared = ss_between / ss_total if ss_total > 0 else 0
    
    print(f"  Eta-Squared (Effect Size): {eta_squared:.4f}")
    
    if p_value_anova < 0.001:
        significance = "*** (Very Strong)"
    elif p_value_anova < 0.01:
        significance = "** (Strong)"
    elif p_value_anova < 0.05:
        significance = "* (Significant)"
    else:
        significance = "Not Significant"
    
    print(f"  Statistical Significance: {significance}")
    
    return {
        'outcome': outcome_name,
        'f_stat': f_stat,
        'p_value_anova': p_value_anova,
        'h_stat': h_stat,
        'p_value_kw': p_value_kw,
        'eta_squared': eta_squared,
        'significance': significance
    }


def predictive_modeling_categorical(df, predictor, outcome, outcome_name):
    """Build a simple predictive model for categorical outcomes."""
    print(f"\n{'=' * 80}")
    print(f"PREDICTIVE MODELING: {outcome_name}")
    print(f"{'=' * 80}")
    
    # Encode predictor
    le = LabelEncoder()
    X = le.fit_transform(df[predictor]).reshape(-1, 1)
    y = df[outcome]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    rf.fit(X_train, y_train)
    
    # Predictions
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')
    
    print(f"\nPredictive Performance:")
    print(f"  Test Accuracy: {accuracy:.4f}")
    print(f"  Cross-Validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # Baseline (always predict most common class)
    baseline = y.value_counts(normalize=True).max()
    print(f"  Baseline Accuracy (Most Common): {baseline:.4f}")
    print(f"  Improvement over Baseline: {(accuracy - baseline):.4f}")
    
    return {
        'outcome': outcome_name,
        'accuracy': accuracy,
        'cv_accuracy': cv_scores.mean(),
        'baseline': baseline,
        'improvement': accuracy - baseline
    }


def predictive_modeling_continuous(df, predictor, outcome, outcome_name):
    """Build a simple predictive model for continuous outcomes."""
    print(f"\n{'=' * 80}")
    print(f"PREDICTIVE MODELING: {outcome_name}")
    print(f"{'=' * 80}")
    
    # Encode predictor
    le = LabelEncoder()
    X = le.fit_transform(df[predictor]).reshape(-1, 1)
    y = df[outcome]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=5)
    rf.fit(X_train, y_train)
    
    # Predictions
    y_pred = rf.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    # Baseline (always predict mean)
    baseline_pred = np.full_like(y_test, y_train.mean())
    baseline_rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))
    
    print(f"\nPredictive Performance:")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  R² Score: {r2:.4f}")
    print(f"  Baseline RMSE (Mean): {baseline_rmse:.4f}")
    print(f"  Improvement over Baseline: {(baseline_rmse - rmse):.4f}")
    
    return {
        'outcome': outcome_name,
        'rmse': rmse,
        'r2': r2,
        'baseline_rmse': baseline_rmse,
        'improvement': baseline_rmse - rmse
    }


def create_visualizations(df, predictor):
    """Create comprehensive visualizations."""
    print(f"\n{'=' * 80}")
    print("CREATING VISUALIZATIONS")
    print(f"{'=' * 80}")
    
    fig, axes = plt.subplots(4, 3, figsize=(20, 24))
    fig.suptitle(f'Relationship between {predictor} and Match Outcomes', 
                 fontsize=16, fontweight='bold')
    
    # 1. FT Winner
    ct = pd.crosstab(df[predictor], df['FT_Winner'], normalize='index') * 100
    ct.plot(kind='bar', ax=axes[0, 0], stacked=False)
    axes[0, 0].set_title('FT Winner Distribution')
    axes[0, 0].set_ylabel('Percentage (%)')
    axes[0, 0].legend(title='Winner')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. FT Total Goals
    df.boxplot(column='FT_Total_Goals', by=predictor, ax=axes[0, 1])
    axes[0, 1].set_title('FT Total Goals Distribution')
    axes[0, 1].set_xlabel(predictor)
    
    # 3. FT Score Difference
    df.boxplot(column='FT_Score_Diff', by=predictor, ax=axes[0, 2])
    axes[0, 2].set_title('FT Score Difference Distribution')
    axes[0, 2].set_xlabel(predictor)
    
    # 4. FT BTTS
    ct = pd.crosstab(df[predictor], df['FT_BTTS'], normalize='index') * 100
    ct.plot(kind='bar', ax=axes[1, 0])
    axes[1, 0].set_title('FT Both Teams To Score')
    axes[1, 0].set_ylabel('Percentage (%)')
    axes[1, 0].legend(['No', 'Yes'])
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 5. FT Home Goals
    df.boxplot(column='FT_Home_Goals', by=predictor, ax=axes[1, 1])
    axes[1, 1].set_title('FT Home Goals Distribution')
    axes[1, 1].set_xlabel(predictor)
    
    # 6. FT Away Goals
    df.boxplot(column='FT_Away_Goals', by=predictor, ax=axes[1, 2])
    axes[1, 2].set_title('FT Away Goals Distribution')
    axes[1, 2].set_xlabel(predictor)
    
    # 7. HT Winner
    ct = pd.crosstab(df[predictor], df['HT_Winner'], normalize='index') * 100
    ct.plot(kind='bar', ax=axes[2, 0], stacked=False)
    axes[2, 0].set_title('HT Winner Distribution')
    axes[2, 0].set_ylabel('Percentage (%)')
    axes[2, 0].legend(title='Winner')
    axes[2, 0].tick_params(axis='x', rotation=45)
    
    # 8. HT Total Goals
    df.boxplot(column='HT_Total_Goals', by=predictor, ax=axes[2, 1])
    axes[2, 1].set_title('HT Total Goals Distribution')
    axes[2, 1].set_xlabel(predictor)
    
    # 9. HT Score Difference
    df.boxplot(column='HT_Score_Diff', by=predictor, ax=axes[2, 2])
    axes[2, 2].set_title('HT Score Difference Distribution')
    axes[2, 2].set_xlabel(predictor)
    
    # 10. HT BTTS
    ct = pd.crosstab(df[predictor], df['HT_BTTS'], normalize='index') * 100
    ct.plot(kind='bar', ax=axes[3, 0])
    axes[3, 0].set_title('HT Both Teams To Score')
    axes[3, 0].set_ylabel('Percentage (%)')
    axes[3, 0].legend(['No', 'Yes'])
    axes[3, 0].tick_params(axis='x', rotation=45)
    
    # 11. HT Home Goals
    df.boxplot(column='HT_Home_Goals', by=predictor, ax=axes[3, 1])
    axes[3, 1].set_title('HT Home Goals Distribution')
    axes[3, 1].set_xlabel(predictor)
    
    # 12. HT Away Goals
    df.boxplot(column='HT_Away_Goals', by=predictor, ax=axes[3, 2])
    axes[3, 2].set_title('HT Away Goals Distribution')
    axes[3, 2].set_xlabel(predictor)
    
    plt.tight_layout()
    plt.savefig('/Users/batumbp/Files/betting/_DENEME/mysterious_category_analysis.png', 
                dpi=300, bbox_inches='tight')
    print("\nVisualizations saved to: mysterious_category_analysis.png")
    plt.close()


def main():
    """Main analysis pipeline."""
    filepath = '/Users/batumbp/Files/betting/_DENEME/data.csv'
    
    # Load data
    df = load_and_prepare_data(filepath)
    
    predictor = 'Mysterious_category'
    
    # Store all results
    categorical_results = []
    continuous_results = []
    model_results_cat = []
    model_results_cont = []
    
    print("\n" + "=" * 80)
    print("PART 1: CATEGORICAL OUTCOMES ANALYSIS")
    print("=" * 80)
    
    # Analyze categorical outcomes
    categorical_outcomes = [
        ('FT_Winner', 'Full-Time Winner'),
        ('FT_BTTS', 'Full-Time Both Teams To Score'),
        ('FT_Home_Win_To_Nil', 'Full-Time Home Win To Nil'),
        ('FT_Away_Win_To_Nil', 'Full-Time Away Win To Nil'),
        ('HT_Winner', 'Half-Time Winner'),
        ('HT_BTTS', 'Half-Time Both Teams To Score'),
        ('HT_Home_Win_To_Nil', 'Half-Time Home Win To Nil'),
        ('HT_Away_Win_To_Nil', 'Half-Time Away Win To Nil'),
    ]
    
    for outcome, name in categorical_outcomes:
        result = analyze_categorical_outcome(df, predictor, outcome, name)
        categorical_results.append(result)
    
    print("\n" + "=" * 80)
    print("PART 2: CONTINUOUS OUTCOMES ANALYSIS")
    print("=" * 80)
    
    # Analyze continuous outcomes
    continuous_outcomes = [
        ('FT_Total_Goals', 'Full-Time Total Goals'),
        ('FT_Home_Goals', 'Full-Time Home Goals'),
        ('FT_Away_Goals', 'Full-Time Away Goals'),
        ('FT_Score_Diff', 'Full-Time Score Difference'),
        ('HT_Total_Goals', 'Half-Time Total Goals'),
        ('HT_Home_Goals', 'Half-Time Home Goals'),
        ('HT_Away_Goals', 'Half-Time Away Goals'),
        ('HT_Score_Diff', 'Half-Time Score Difference'),
    ]
    
    for outcome, name in continuous_outcomes:
        result = analyze_continuous_outcome(df, predictor, outcome, name)
        continuous_results.append(result)
    
    print("\n" + "=" * 80)
    print("PART 3: PREDICTIVE MODELING - CATEGORICAL")
    print("=" * 80)
    
    # Predictive modeling for categorical
    for outcome, name in categorical_outcomes:
        result = predictive_modeling_categorical(df, predictor, outcome, name)
        model_results_cat.append(result)
    
    print("\n" + "=" * 80)
    print("PART 4: PREDICTIVE MODELING - CONTINUOUS")
    print("=" * 80)
    
    # Predictive modeling for continuous
    for outcome, name in continuous_outcomes:
        result = predictive_modeling_continuous(df, predictor, outcome, name)
        model_results_cont.append(result)
    
    # Create visualizations
    create_visualizations(df, predictor)
    
    # SUMMARY REPORT
    print("\n" + "=" * 80)
    print("COMPREHENSIVE SUMMARY REPORT")
    print("=" * 80)
    
    print("\n1. CATEGORICAL OUTCOMES - Statistical Tests")
    print("-" * 80)
    cat_df = pd.DataFrame(categorical_results)
    cat_df = cat_df.sort_values('p_value')
    print(cat_df.to_string(index=False))
    
    print("\n2. CONTINUOUS OUTCOMES - Statistical Tests")
    print("-" * 80)
    cont_df = pd.DataFrame(continuous_results)
    cont_df = cont_df.sort_values('p_value_anova')
    print(cont_df[['outcome', 'f_stat', 'p_value_anova', 'eta_squared', 'significance']].to_string(index=False))
    
    print("\n3. PREDICTIVE PERFORMANCE - Categorical")
    print("-" * 80)
    model_cat_df = pd.DataFrame(model_results_cat)
    model_cat_df = model_cat_df.sort_values('improvement', ascending=False)
    print(model_cat_df.to_string(index=False))
    
    print("\n4. PREDICTIVE PERFORMANCE - Continuous")
    print("-" * 80)
    model_cont_df = pd.DataFrame(model_results_cont)
    model_cont_df = model_cont_df.sort_values('r2', ascending=False)
    print(model_cont_df.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    
    # Find most predictive outcomes
    significant_cat = cat_df[cat_df['p_value'] < 0.05]
    print(f"\n{len(significant_cat)}/{len(cat_df)} categorical outcomes show statistical significance")
    
    if len(significant_cat) > 0:
        print("\nMost predictive categorical outcomes:")
        for idx, row in significant_cat.head(3).iterrows():
            print(f"  - {row['outcome']}: Cramér's V = {row['cramers_v']:.4f}, p = {row['p_value']:.6f}")
    
    significant_cont = cont_df[cont_df['p_value_anova'] < 0.05]
    print(f"\n{len(significant_cont)}/{len(cont_df)} continuous outcomes show statistical significance")
    
    if len(significant_cont) > 0:
        print("\nMost predictive continuous outcomes:")
        for idx, row in significant_cont.head(3).iterrows():
            print(f"  - {row['outcome']}: Eta² = {row['eta_squared']:.4f}, p = {row['p_value_anova']:.6f}")
    
    # Save results to CSV
    cat_df.to_csv('/Users/batumbp/Files/betting/_DENEME/categorical_analysis_results.csv', index=False)
    cont_df.to_csv('/Users/batumbp/Files/betting/_DENEME/continuous_analysis_results.csv', index=False)
    model_cat_df.to_csv('/Users/batumbp/Files/betting/_DENEME/predictive_model_categorical_results.csv', index=False)
    model_cont_df.to_csv('/Users/batumbp/Files/betting/_DENEME/predictive_model_continuous_results.csv', index=False)
    
    print("\n" + "=" * 80)
    print("Analysis complete! Results saved to:")
    print("  - mysterious_category_analysis.png")
    print("  - categorical_analysis_results.csv")
    print("  - continuous_analysis_results.csv")
    print("  - predictive_model_categorical_results.csv")
    print("  - predictive_model_continuous_results.csv")
    print("=" * 80)


if __name__ == "__main__":
    main()
