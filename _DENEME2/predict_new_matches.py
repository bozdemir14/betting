import pandas as pd
import joblib
import numpy as np

# Feature to odds column mapping (same as analysis script)
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

def predict_match_probabilities(new_match_data, model_dir='/Users/batumbp/Files/betting/_DENEME2/results/models/',
                               encoder_path='/Users/batumbp/Files/betting/_DENEME2/results/encoder.pkl'):
    """
    Predict probabilities for new match data using trained models.
    Shows both model predictions and implied probabilities from odds where available.

    Parameters:
    new_match_data: DataFrame with match data. Should include odds columns if available.

    Returns:
    DataFrame with predictions for all features
    """

    # Load the encoder
    encoder = joblib.load(encoder_path)

    # Prepare input data
    input_cols = ['Favorite_Odds', 'Favorite_Team', 'Lig', 'Season', 'Hafta']
    for col in input_cols:
        new_match_data[col] = new_match_data[col].astype('category')

    X_new = new_match_data[input_cols]

    # Encode the new data
    X_new_encoded = encoder.transform(X_new)

    # Get list of available models
    import os
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.pkl')]

    # Initialize results DataFrame
    results = new_match_data.copy()

    # Collect all prediction data first to avoid DataFrame fragmentation
    model_proba_data = {}
    implied_proba_data = {}
    odds_available_data = {}

    # Predict for each feature
    for model_file in model_files:
        feature_name = model_file.replace('.pkl', '')
        model_path = os.path.join(model_dir, model_file)

        try:
            # Load model
            model = joblib.load(model_path)

            # Get probability for positive class
            proba = model.predict_proba(X_new_encoded)[:, 1]

            # Store model probability
            model_proba_data[f'{feature_name}_model_proba'] = proba

            # Add implied probability if odds mapping exists and odds column is available
            if feature_name in FEATURE_TO_ODDS_MAPPING:
                odds_col = FEATURE_TO_ODDS_MAPPING[feature_name]
                if odds_col in new_match_data.columns:
                    # Calculate implied probability as 1/odds
                    odds_values = pd.to_numeric(new_match_data[odds_col], errors='coerce')
                    implied_proba = 1 / odds_values
                    implied_proba_data[f'{feature_name}_implied_proba'] = implied_proba
                    odds_available_data[f'{feature_name}_odds_available'] = True
                else:
                    implied_proba_data[f'{feature_name}_implied_proba'] = np.nan
                    odds_available_data[f'{feature_name}_odds_available'] = False
            else:
                implied_proba_data[f'{feature_name}_implied_proba'] = np.nan
                odds_available_data[f'{feature_name}_odds_available'] = False

        except Exception as e:
            print(f"Error predicting for {feature_name}: {e}")
            continue

    # Create DataFrames from collected data and concatenate at once
    if model_proba_data:
        model_proba_df = pd.DataFrame(model_proba_data, index=results.index)
        results = pd.concat([results, model_proba_df], axis=1)

    if implied_proba_data:
        implied_proba_df = pd.DataFrame(implied_proba_data, index=results.index)
        results = pd.concat([results, implied_proba_df], axis=1)

    if odds_available_data:
        odds_available_df = pd.DataFrame(odds_available_data, index=results.index)
        results = pd.concat([results, odds_available_df], axis=1)

    return results

# Example usage
if __name__ == "__main__":
    # Load data with odds for testing
    try:
        df = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/data/fikstur_feature_matrix_with_odds.csv')
        print("Loaded data with odds columns.")
    except FileNotFoundError:
        print("Odds data not found, loading basic data...")
        df = pd.read_csv('/Users/batumbp/Files/betting/_DENEME2/data/fikstur_feature_matrix_final.csv')

    # Take ALL matches (not just sample)
    sample_matches = df[['Favorite_Odds', 'Favorite_Team', 'Lig', 'Season', 'Hafta']].copy()

    # If odds columns are available, include them
    odds_columns = ['1', '0', '2', '1&0', '1&2', '2&0']  # Common odds columns
    available_odds_cols = [col for col in odds_columns if col in df.columns]
    if available_odds_cols:
        for col in available_odds_cols:
            sample_matches[col] = df[col].values

    print("Sample matches for prediction:")
    print(sample_matches)
    print()

    predictions = predict_match_probabilities(sample_matches)
    print("Predictions for sample matches (showing first few columns):")
    # Show only key columns to avoid overwhelming output
    key_cols = ['Favorite_Odds', 'Favorite_Team', 'Lig', 'Season', 'Hafta']
    proba_cols = [col for col in predictions.columns if '_model_proba' in col or '_implied_proba' in col][:10]  # Show first 10 proba columns
    display_cols = key_cols + proba_cols
    print(predictions[display_cols].head())

    # Save comprehensive predictions to CSV
    output_file = '/Users/batumbp/Files/betting/_DENEME2/results/comprehensive_predictions.csv'
    predictions.to_csv(output_file, index=False)
    print(f"\n💾 Comprehensive predictions saved to: {output_file}")
    print(f"📊 File contains {len(predictions)} matches with {len([col for col in predictions.columns if '_model_proba' in col])} features")
    print(f"🎯 Each feature shows: model probability + implied probability (when odds available)")

    # Show detailed comparison for first match and first few features
    print(f"\nDetailed comparison for first match (showing features with odds):")
    model_proba_cols = [col for col in predictions.columns if col.endswith('_model_proba')]

    for model_col in model_proba_cols[:5]:  # Show first 5 features
        feature_name = model_col.replace('_model_proba', '')
        model_proba = predictions[model_col].iloc[0]
        implied_col = f"{feature_name}_implied_proba"
        odds_available = predictions[f"{feature_name}_odds_available"].iloc[0] if f"{feature_name}_odds_available" in predictions.columns else False

        if odds_available and implied_col in predictions.columns:
            implied_proba = predictions[implied_col].iloc[0]
            if pd.notna(implied_proba):
                print(f"  {feature_name}: Model={model_proba:.3f}, Implied={implied_proba:.3f}")
            else:
                print(f"  {feature_name}: Model={model_proba:.3f}, Implied=N/A")
        else:
            print(f"  {feature_name}: Model={model_proba:.3f}, Implied=N/A (no odds)")