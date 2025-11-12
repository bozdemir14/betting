"""
Train machine learning models to predict match outcomes
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
import pickle
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class MatchOutcomePredictor:
    def __init__(self, data_path='data_new.csv'):
        """Initialize the predictor"""
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.models = {}
        self.best_model = None
        self.feature_names = None
        
    def load_and_prepare_data(self):
        """Load data and prepare for training"""
        print("Loading data...")
        self.df = pd.read_csv(self.data_path)
        print(f"Data loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        
        # Remove rows with missing target
        initial_rows = len(self.df)
        self.df = self.df.dropna(subset=['FT_Result'])
        print(f"Removed {initial_rows - len(self.df)} rows with missing outcome")
        
        return self
    
    def select_features(self):
        """Select features for training - ONLY PRE-MATCH FEATURES"""
        # This is a PRE-MATCH prediction model
        # EXCLUDE any features that contain match outcome information:
        # - Full-time scores (FTHG, FTAG)
        # - Half-time scores (HTHG, HTAG, HT_Goal_Diff, HT_BTTS, etc.)
        # - Match events (Total_Goals, BTTS, Clean_Sheet, Comeback_Status, etc.)
        
        # ONLY use features available BEFORE the match starts
        
        odds_features = [
            'HomeOdds', 'DrawOdds', 'AwayOdds',
            'HomeDrawOdds', 'HomeAwayOdds', 'AwayDrawOdds',
            'Under2.5', 'Over2.5',
            'Prob_Home', 'Prob_Draw', 'Prob_Away',
            'True_Prob_Home', 'True_Prob_Draw', 'True_Prob_Away',
            'Margin', 'Entropy',
            'Favorite_Odds', 'Underdog_Odds', 'Mismatch_Ratio',
            'Home_Is_Favorite',
            'Prob_Over2.5', 'Prob_Under2.5', 'Margin_OU2.5',
            'Market_Expected_Goals'
        ]
        
        # Historical form features (available before match)
        form_features = [
            'Home_Days_Since_Last', 'Away_Days_Since_Last',
            'Home_Avg_Goals_Scored_Last5', 'Home_Avg_Goals_Conceded_Last5',
            'Home_Form_Points_Last5', 'Home_Win_Ratio_Last5',
            'Away_Avg_Goals_Scored_Last5', 'Away_Avg_Goals_Conceded_Last5',
            'Away_Form_Points_Last5', 'Away_Win_Ratio_Last5',
            'Home_Form_Consistency_Last5', 'Home_Weighted_Form_Points_Last5',
            'Home_Clean_Sheet_Ratio_Last5', 'Away_Form_Consistency_Last5',
            'Away_Weighted_Form_Points_Last5', 'Away_Clean_Sheet_Ratio_Last5',
            'Goal_Diff_Form', 'Points_Diff_Form',
            'H2H_Avg_Goal_Diff', 'H2H_Recent_Win_Ratio',
            'Days_Since_Last_Match', 'Odds_Disagreement', 'Elo_Difference'
        ]
        
        all_features = odds_features + form_features
        
        # Select features that exist in the dataframe and are numeric
        available_features = []
        for feat in all_features:
            if feat in self.df.columns:
                # Check if column is numeric
                if self.df[feat].dtype in ['int64', 'float64', 'int32', 'float32', 'bool']:
                    available_features.append(feat)
        
        print(f"\nSelected {len(available_features)} numeric features for training")
        self.feature_names = available_features
        
        return available_features
    
    def prepare_train_test_split(self, test_size=0.2, random_state=42):
        """Prepare train-test split"""
        print("\nPreparing features and target...")
        
        features = self.select_features()
        
        # Prepare features (X)
        X = self.df[features].copy()
        
        # Handle missing values
        X = X.fillna(X.median())
        
        # Prepare target (y) - FT_Result is already numeric
        # 0: Draw, 1: Home Win, 2: Away Win
        y = self.df['FT_Result'].copy()
        
        print(f"\nTarget distribution:")
        print(y.value_counts().sort_index())
        print(f"\nPercentages:")
        print(y.value_counts(normalize=True).sort_index() * 100)
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"\nTrain set: {self.X_train.shape[0]} samples")
        print(f"Test set: {self.X_test.shape[0]} samples")
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        return self
    
    def train_models(self):
        """Train multiple models"""
        print("\n" + "="*60)
        print("TRAINING MODELS")
        print("="*60)
        
        # Define models
        models_to_train = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000, 
                random_state=42,
                multi_class='multinomial'
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
        }
        
        results = {}
        
        for name, model in models_to_train.items():
            print(f"\nTraining {name}...")
            
            # Use scaled data for Logistic Regression, raw for tree-based models
            if 'Logistic' in name:
                X_train_use = self.X_train_scaled
                X_test_use = self.X_test_scaled
            else:
                X_train_use = self.X_train
                X_test_use = self.X_test
            
            # Train
            model.fit(X_train_use, self.y_train)
            
            # Predict
            y_pred = model.predict(X_test_use)
            y_pred_proba = model.predict_proba(X_test_use)
            
            # Evaluate
            accuracy = accuracy_score(self.y_test, y_pred)
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train_use, self.y_train, cv=5)
            
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }
            
            print(f"  Accuracy: {accuracy:.4f}")
            print(f"  CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
            
            # Store model
            self.models[name] = model
        
        # Select best model
        best_model_name = max(results, key=lambda x: results[x]['accuracy'])
        self.best_model = results[best_model_name]['model']
        self.best_model_name = best_model_name
        
        print(f"\n{'='*60}")
        print(f"BEST MODEL: {best_model_name}")
        print(f"{'='*60}")
        
        return results
    
    def evaluate_best_model(self, results):
        """Detailed evaluation of the best model"""
        print("\n" + "="*60)
        print("DETAILED EVALUATION OF BEST MODEL")
        print("="*60)
        
        best_result = results[self.best_model_name]
        y_pred = best_result['predictions']
        y_pred_proba = best_result['probabilities']
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred, 
                                   target_names=['Draw', 'Home Win', 'Away Win']))
        
        # Confusion matrix
        print("\nConfusion Matrix:")
        cm = confusion_matrix(self.y_test, y_pred)
        print("              Predicted")
        print("              Draw  Home  Away")
        for i, row in enumerate(cm):
            label = ['Draw', 'Home', 'Away'][i]
            print(f"Actual {label:5s}  {row[0]:4d}  {row[1]:4d}  {row[2]:4d}")
        
        # Feature importance (if available)
        if hasattr(self.best_model, 'feature_importances_'):
            print("\nTop 15 Most Important Features:")
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.best_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            for idx, row in feature_importance.head(15).iterrows():
                print(f"  {row['feature']:30s}: {row['importance']:.4f}")
        
        return best_result
    
    def save_model(self, output_dir='models'):
        """Save the trained model and scaler"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save model
        model_path = f"{output_dir}/model_{self.best_model_name.replace(' ', '_').lower()}_{timestamp}.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(self.best_model, f)
        print(f"\nModel saved to: {model_path}")
        
        # Save scaler
        scaler_path = f"{output_dir}/scaler_{timestamp}.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"Scaler saved to: {scaler_path}")
        
        # Save feature names
        features_path = f"{output_dir}/features_{timestamp}.json"
        with open(features_path, 'w') as f:
            json.dump({
                'features': self.feature_names,
                'model_name': self.best_model_name,
                'timestamp': timestamp
            }, f, indent=2)
        print(f"Features saved to: {features_path}")
        
        # Save metadata
        metadata = {
            'model_name': self.best_model_name,
            'timestamp': timestamp,
            'train_size': len(self.X_train),
            'test_size': len(self.X_test),
            'features': self.feature_names,
            'num_features': len(self.feature_names)
        }
        
        metadata_path = f"{output_dir}/metadata_{timestamp}.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Metadata saved to: {metadata_path}")
        
        return model_path, scaler_path, features_path
    
    def predict_new_matches(self, new_data):
        """Make predictions on new data"""
        if self.best_model is None:
            raise ValueError("No model trained yet. Run train_models() first.")
        
        # Prepare features
        X_new = new_data[self.feature_names].copy()
        X_new = X_new.fillna(X_new.median())
        
        # Scale if needed
        if 'Logistic' in self.best_model_name:
            X_new_scaled = self.scaler.transform(X_new)
            predictions = self.best_model.predict(X_new_scaled)
            probabilities = self.best_model.predict_proba(X_new_scaled)
        else:
            predictions = self.best_model.predict(X_new)
            probabilities = self.best_model.predict_proba(X_new)
        
        return predictions, probabilities


def main():
    """Main training pipeline"""
    print("="*60)
    print("FOOTBALL MATCH OUTCOME PREDICTION")
    print("="*60)
    
    # Initialize predictor
    predictor = MatchOutcomePredictor('data_new.csv')
    
    # Load and prepare data
    predictor.load_and_prepare_data()
    
    # Prepare train-test split
    predictor.prepare_train_test_split(test_size=0.2, random_state=42)
    
    # Train models
    results = predictor.train_models()
    
    # Evaluate best model
    predictor.evaluate_best_model(results)
    
    # Save model
    predictor.save_model()
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    
    return predictor, results


if __name__ == "__main__":
    predictor, results = main()
