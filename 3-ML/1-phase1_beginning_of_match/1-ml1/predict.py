"""
Predict football match outcomes using the trained model
"""
import pandas as pd
import numpy as np
import pickle
import json
import os
from datetime import datetime

class MatchPredictor:
    def __init__(self, model_dir='models'):
        """Initialize predictor with latest model"""
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.metadata = None
        self.feature_names = None
        self.load_latest_model()
    
    def load_latest_model(self):
        """Load the most recent pre-match model"""
        # Find latest prematch model files
        model_files = [f for f in os.listdir(self.model_dir) if f.startswith('prematch_model_') and f.endswith('.pkl')]
        if not model_files:
            raise FileNotFoundError(f"No pre-match model found in {self.model_dir}")
        
        # Get the latest model
        latest_model = sorted(model_files)[-1]
        # Extract timestamp: prematch_model_random_forest_20251109_175623.pkl -> 20251109_175623
        parts = latest_model.replace('.pkl', '').split('_')
        timestamp = '_'.join(parts[-2:])  # Get last two parts (date_time)
        
        model_path = os.path.join(self.model_dir, latest_model)
        scaler_path = os.path.join(self.model_dir, f'prematch_scaler_{timestamp}.pkl')
        metadata_path = os.path.join(self.model_dir, f'prematch_metadata_{timestamp}.json')
        
        print(f"Loading model: {latest_model}")
        
        # Load model
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        # Load scaler
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        # Load metadata
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
            self.feature_names = self.metadata['features']
        
        print(f"Model type: {self.metadata['model_name']}")
        print(f"Features: {len(self.feature_names)}")
        print(f"Trained on {self.metadata['train_size']} matches")
        print()
    
    def predict_from_odds(self, home_odds, draw_odds, away_odds, 
                         under_2_5=None, over_2_5=None,
                         home_form=None, away_form=None):
        """
        Predict match outcome from betting odds and optional form data
        
        Parameters:
        -----------
        home_odds : float
            Decimal odds for home win (e.g., 1.75)
        draw_odds : float
            Decimal odds for draw (e.g., 3.40)
        away_odds : float
            Decimal odds for away win (e.g., 4.50)
        under_2_5 : float, optional
            Odds for under 2.5 goals
        over_2_5 : float, optional
            Odds for over 2.5 goals
        home_form : dict, optional
            Dict with keys: avg_goals_scored, avg_goals_conceded, form_points, win_ratio
        away_form : dict, optional
            Dict with keys: avg_goals_scored, avg_goals_conceded, form_points, win_ratio
        
        Returns:
        --------
        dict : Prediction results with probabilities and recommendation
        """
        # Create a DataFrame with the input
        data = self._create_feature_dict(
            home_odds, draw_odds, away_odds,
            under_2_5, over_2_5,
            home_form, away_form
        )
        
        # Create DataFrame with all features
        df = pd.DataFrame([data])
        
        # Ensure all required features are present
        for feat in self.feature_names:
            if feat not in df.columns:
                df[feat] = np.nan
        
        # Select only the features the model expects
        X = df[self.feature_names]
        
        # Fill missing values with median from training (approximation)
        X = X.fillna(X.median())
        X = X.fillna(0)  # If still NaN, use 0
        
        # Scale features (only for Logistic Regression)
        if 'logistic' in self.metadata['model_name'].lower():
            X_scaled = self.scaler.transform(X)
            prediction = self.model.predict(X_scaled)[0]
            probabilities = self.model.predict_proba(X_scaled)[0]
        else:
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
        
        # Map prediction to outcome
        outcome_map = {0: 'Draw', 1: 'Home Win', 2: 'Away Win'}
        predicted_outcome = outcome_map[prediction]
        
        # Create result dictionary
        result = {
            'prediction': predicted_outcome,
            'probabilities': {
                'Draw': float(probabilities[0]),
                'Home Win': float(probabilities[1]),
                'Away Win': float(probabilities[2])
            },
            'confidence': float(probabilities[prediction]),
            'odds': {
                'Home': home_odds,
                'Draw': draw_odds,
                'Away': away_odds
            }
        }
        
        # Add betting recommendation
        result['recommendation'] = self._get_betting_recommendation(result)
        
        return result
    
    def _create_feature_dict(self, home_odds, draw_odds, away_odds,
                            under_2_5, over_2_5,
                            home_form, away_form):
        """Create feature dictionary from inputs"""
        data = {}
        
        # Basic odds
        data['HomeOdds'] = home_odds
        data['DrawOdds'] = draw_odds
        data['AwayOdds'] = away_odds
        
        # Calculate implied probabilities
        data['Prob_Home'] = 1 / home_odds if home_odds > 0 else 0
        data['Prob_Draw'] = 1 / draw_odds if draw_odds > 0 else 0
        data['Prob_Away'] = 1 / away_odds if away_odds > 0 else 0
        
        # Calculate margin (bookmaker overround)
        total_prob = data['Prob_Home'] + data['Prob_Draw'] + data['Prob_Away']
        data['Margin'] = total_prob - 1
        
        # True probabilities (removing margin)
        if total_prob > 0:
            data['True_Prob_Home'] = data['Prob_Home'] / total_prob
            data['True_Prob_Draw'] = data['Prob_Draw'] / total_prob
            data['True_Prob_Away'] = data['Prob_Away'] / total_prob
        
        # Entropy (uncertainty measure)
        probs = [data['True_Prob_Home'], data['True_Prob_Draw'], data['True_Prob_Away']]
        data['Entropy'] = -sum(p * np.log(p) if p > 0 else 0 for p in probs)
        
        # Favorite/Underdog analysis
        data['Favorite_Odds'] = min(home_odds, draw_odds, away_odds)
        data['Underdog_Odds'] = max(home_odds, draw_odds, away_odds)
        data['Mismatch_Ratio'] = data['Underdog_Odds'] / data['Favorite_Odds'] if data['Favorite_Odds'] > 0 else 0
        data['Home_Is_Favorite'] = 1 if home_odds == data['Favorite_Odds'] else 0
        
        # Over/Under 2.5 goals
        if under_2_5 is not None and over_2_5 is not None:
            data['Under2.5'] = under_2_5
            data['Over2.5'] = over_2_5
            data['Prob_Under2.5'] = 1 / under_2_5 if under_2_5 > 0 else 0
            data['Prob_Over2.5'] = 1 / over_2_5 if over_2_5 > 0 else 0
            total_ou = data['Prob_Under2.5'] + data['Prob_Over2.5']
            data['Margin_OU2.5'] = total_ou - 1
            
            # Expected goals from market
            true_prob_over = data['Prob_Over2.5'] / total_ou if total_ou > 0 else 0.5
            data['Market_Expected_Goals'] = 2.5 + (true_prob_over - 0.5) * 2  # Rough estimate
        
        # Double chance odds (if not provided, estimate them)
        data['HomeDrawOdds'] = np.nan
        data['HomeAwayOdds'] = np.nan
        data['AwayDrawOdds'] = np.nan
        
        # Team form features
        if home_form:
            data['Home_Avg_Goals_Scored_Last5'] = home_form.get('avg_goals_scored', np.nan)
            data['Home_Avg_Goals_Conceded_Last5'] = home_form.get('avg_goals_conceded', np.nan)
            data['Home_Form_Points_Last5'] = home_form.get('form_points', np.nan)
            data['Home_Win_Ratio_Last5'] = home_form.get('win_ratio', np.nan)
        
        if away_form:
            data['Away_Avg_Goals_Scored_Last5'] = away_form.get('avg_goals_scored', np.nan)
            data['Away_Avg_Goals_Conceded_Last5'] = away_form.get('avg_goals_conceded', np.nan)
            data['Away_Form_Points_Last5'] = away_form.get('form_points', np.nan)
            data['Away_Win_Ratio_Last5'] = away_form.get('win_ratio', np.nan)
        
        # Form differences
        if home_form and away_form:
            home_gd = home_form.get('avg_goals_scored', 0) - home_form.get('avg_goals_conceded', 0)
            away_gd = away_form.get('avg_goals_scored', 0) - away_form.get('avg_goals_conceded', 0)
            data['Goal_Diff_Form'] = home_gd - away_gd
            data['Points_Diff_Form'] = home_form.get('form_points', 0) - away_form.get('form_points', 0)
        
        # Days since last match (if not provided, use default)
        data['Home_Days_Since_Last'] = np.nan
        data['Away_Days_Since_Last'] = np.nan
        
        return data
    
    def _get_betting_recommendation(self, result):
        """Generate betting recommendation based on prediction and odds"""
        pred = result['prediction']
        confidence = result['confidence']
        odds = result['odds']
        probs = result['probabilities']
        
        # Map prediction to odds
        odds_map = {'Home Win': odds['Home'], 'Draw': odds['Draw'], 'Away Win': odds['Away']}
        predicted_odds = odds_map[pred]
        
        # Calculate expected value
        expected_value = (confidence * predicted_odds) - 1
        
        recommendation = {
            'bet': pred,
            'confidence_level': 'High' if confidence > 0.6 else 'Medium' if confidence > 0.5 else 'Low',
            'expected_value': f"{expected_value:.2%}",
            'is_value_bet': expected_value > 0.1,  # At least 10% edge
        }
        
        # Add betting advice
        if expected_value > 0.2:
            recommendation['advice'] = f"Strong value bet on {pred} (EV: {expected_value:.1%})"
        elif expected_value > 0.1:
            recommendation['advice'] = f"Good value on {pred} (EV: {expected_value:.1%})"
        elif expected_value > 0:
            recommendation['advice'] = f"Slight value on {pred} (EV: {expected_value:.1%})"
        else:
            recommendation['advice'] = f"No value bet - odds don't reflect edge"
        
        return recommendation
    
    def print_prediction(self, result, home_team="Home", away_team="Away"):
        """Pretty print prediction results"""
        print("=" * 60)
        print(f"MATCH PREDICTION: {home_team} vs {away_team}")
        print("=" * 60)
        
        print("\n📊 ODDS:")
        print(f"  Home Win: {result['odds']['Home']:.2f}")
        print(f"  Draw:     {result['odds']['Draw']:.2f}")
        print(f"  Away Win: {result['odds']['Away']:.2f}")
        
        print("\n🎯 PREDICTION:")
        print(f"  {result['prediction']} ({result['confidence']:.1%} confidence)")
        
        print("\n📈 PROBABILITIES:")
        for outcome, prob in sorted(result['probabilities'].items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(prob * 50)
            print(f"  {outcome:10s}: {prob:.1%} {bar}")
        
        print("\n💰 BETTING RECOMMENDATION:")
        rec = result['recommendation']
        print(f"  Bet on: {rec['bet']}")
        print(f"  Confidence: {rec['confidence_level']}")
        print(f"  Expected Value: {rec['expected_value']}")
        print(f"  ✓ {rec['advice']}" if rec['is_value_bet'] else f"  ✗ {rec['advice']}")
        
        print("\n" + "=" * 60)


def main():
    """Example usage"""
    print("Loading prediction model...\n")
    predictor = MatchPredictor()
    
    print("=" * 60)
    print("EXAMPLE 1: Basic prediction with odds only")
    print("=" * 60)
    
    # Example: Strong home favorite
    result = predictor.predict_from_odds(
        home_odds=1.50,  # Home is favorite
        draw_odds=4.00,
        away_odds=6.50,
        under_2_5=2.10,
        over_2_5=1.75
    )
    predictor.print_prediction(result, "Manchester City", "Fulham")
    
    print("\n" * 2)
    print("=" * 60)
    print("EXAMPLE 2: Prediction with team form data")
    print("=" * 60)
    
    # Example: Even match with form data
    home_form = {
        'avg_goals_scored': 1.8,
        'avg_goals_conceded': 1.2,
        'form_points': 9,  # 3 wins in last 5
        'win_ratio': 0.6
    }
    
    away_form = {
        'avg_goals_scored': 1.4,
        'avg_goals_conceded': 1.6,
        'form_points': 6,  # 2 wins in last 5
        'win_ratio': 0.4
    }
    
    result = predictor.predict_from_odds(
        home_odds=2.20,
        draw_odds=3.40,
        away_odds=3.20,
        under_2_5=2.00,
        over_2_5=1.85,
        home_form=home_form,
        away_form=away_form
    )
    predictor.print_prediction(result, "Arsenal", "Chelsea")
    
    print("\n\n📝 TO PREDICT YOUR OWN MATCH:")
    print("="*60)
    print("""
from predict import MatchPredictor

predictor = MatchPredictor()

result = predictor.predict_from_odds(
    home_odds=1.85,
    draw_odds=3.60,
    away_odds=4.20,
    under_2_5=2.05,  # optional
    over_2_5=1.80    # optional
)

predictor.print_prediction(result, "Team A", "Team B")
    """)


if __name__ == "__main__":
    main()
