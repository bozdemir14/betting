"""
Train PRE-MATCH machine learning models to predict match outcomes
Only uses features available BEFORE the match starts (no actual match results)
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class PreMatchPredictor:
    def __init__(self, data_path='data_new.csv'):
        """Initialize the pre-match predictor"""
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
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
    
    def select_prematch_features(self):
        """Select only features available BEFORE match starts"""
        print("\n" + "="*60)
        print("SELECTING PRE-MATCH FEATURES ONLY")
        print("="*60)
        
        # Only betting odds and team form - NO match results
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
        missing_features = []
        for feat in all_features:
            if feat in self.df.columns:
                # Check if column is numeric
                if self.df[feat].dtype in ['int64', 'float64', 'int32', 'float32', 'bool']:
                    available_features.append(feat)
                else:
                    print(f"  Skipping {feat} (not numeric)")
            else:
                missing_features.append(feat)
        
        print(f"\nAvailable features: {len(available_features)}")
        print(f"Missing features: {len(missing_features)}")
        if missing_features:
            print(f"  Missing: {', '.join(missing_features[:5])}...")
        
        self.feature_names = available_features
        
        print("\nFeature categories:")
        odds_count = sum(1 for f in available_features if any(x in f for x in ['Odds', 'Prob', 'Margin', 'Entropy', 'Favorite', 'Underdog', 'Mismatch', 'Market', 'Expected']))
        form_count = sum(1 for f in available_features if any(x in f for x in ['Days', 'Avg', 'Form', 'Win_Ratio', 'Diff']))
        print(f"  Odds & Market features: {odds_count}")
        print(f"  Team Form features: {form_count}")
        
        return available_features
    
    def prepare_train_test_split(self, test_size=0.2, random_state=42):
        """Prepare train-test split"""
        print("\n" + "="*60)
        print("PREPARING TRAINING DATA")
        print("="*60)
        
        features = self.select_prematch_features()
        
        # Prepare features (X)
        X = self.df[features].copy()
        
        # Handle missing values
        print(f"\nMissing values before imputation:")
        missing_counts = X.isnull().sum()
        if missing_counts.sum() > 0:
            for col in missing_counts[missing_counts > 0].index:
                print(f"  {col}: {missing_counts[col]}")
        
        X = X.fillna(X.median())
        
        # Prepare target (y) - FT_Result is already numeric
        # 0: Draw, 1: Home Win, 2: Away Win
        y = self.df['FT_Result'].copy()
        
        print(f"\nTarget distribution:")
        for label, name in [(0, 'Draw'), (1, 'Home Win'), (2, 'Away Win')]:
            count = (y == label).sum()
            pct = count / len(y) * 100
            print(f"  {name}: {count} ({pct:.1f}%)")
        
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
        
        # Define models with more conservative settings to avoid overfitting
        models_to_train = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000, 
                random_state=42,
                multi_class='multinomial',
                C=1.0
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=200,
                max_depth=8,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=42,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=150,
                max_depth=4,
                min_samples_split=10,
                min_samples_leaf=5,
                learning_rate=0.1,
                random_state=42
            )
        }
        
        results = {}
        
        for name, model in models_to_train.items():
            print(f"\n{name}:")
            print(f"  Training...")
            
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
            train_accuracy = model.score(X_train_use, self.y_train)
            test_accuracy = accuracy_score(self.y_test, y_pred)
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train_use, self.y_train, cv=5)
            
            results[name] = {
                'model': model,
                'train_accuracy': train_accuracy,
                'test_accuracy': test_accuracy,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }
            
            print(f"  Train Accuracy: {train_accuracy:.4f}")
            print(f"  Test Accuracy:  {test_accuracy:.4f}")
            print(f"  CV Score:       {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
            
            # Store model
            self.models[name] = model
        
        # Select best model based on test accuracy
        best_model_name = max(results, key=lambda x: results[x]['test_accuracy'])
        self.best_model = results[best_model_name]['model']
        self.best_model_name = best_model_name
        
        print(f"\n{'='*60}")
        print(f"BEST MODEL: {best_model_name}")
        print(f"Test Accuracy: {results[best_model_name]['test_accuracy']:.4f}")
        print(f"{'='*60}")
        
        return results
    
    def evaluate_best_model(self, results):
        """Detailed evaluation of the best model"""
        print("\n" + "="*60)
        print("DETAILED EVALUATION")
        print("="*60)
        
        best_result = results[self.best_model_name]
        y_pred = best_result['predictions']
        y_pred_proba = best_result['probabilities']
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred, 
                                   target_names=['Draw', 'Home Win', 'Away Win'],
                                   digits=3))
        
        # Confusion matrix
        print("\nConfusion Matrix:")
        cm = confusion_matrix(self.y_test, y_pred)
        print("              Predicted")
        print("              Draw  Home  Away")
        for i, row in enumerate(cm):
            label = ['Draw', 'Home', 'Away'][i]
            print(f"Actual {label:5s}  {row[0]:4d}  {row[1]:4d}  {row[2]:4d}")
        
        # Calculate per-class accuracy
        print("\nPer-Class Accuracy:")
        for i, label in enumerate(['Draw', 'Home Win', 'Away Win']):
            correct = cm[i, i]
            total = cm[i].sum()
            acc = correct / total if total > 0 else 0
            print(f"  {label:10s}: {correct:3d}/{total:3d} = {acc:.3f}")
        
        # Feature importance (if available)
        if hasattr(self.best_model, 'feature_importances_'):
            print("\nTop 20 Most Important Features:")
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.best_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            for idx, row in feature_importance.head(20).iterrows():
                print(f"  {row['feature']:35s}: {row['importance']:.4f}")
        
        # Prediction confidence analysis
        print("\nPrediction Confidence Analysis:")
        max_probs = y_pred_proba.max(axis=1)
        print(f"  Average confidence: {max_probs.mean():.3f}")
        print(f"  Min confidence: {max_probs.min():.3f}")
        print(f"  Max confidence: {max_probs.max():.3f}")
        
        # Accuracy by confidence level
        high_conf = max_probs > 0.5
        if high_conf.sum() > 0:
            high_conf_acc = accuracy_score(self.y_test[high_conf], y_pred[high_conf])
            print(f"  High confidence (>0.5) predictions: {high_conf.sum()} ({high_conf.sum()/len(y_pred)*100:.1f}%)")
            print(f"  High confidence accuracy: {high_conf_acc:.3f}")
        
        return best_result
    
    def save_model(self, output_dir='models'):
        """Save the trained model and scaler"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save model
        model_path = f"{output_dir}/prematch_model_{self.best_model_name.replace(' ', '_').lower()}_{timestamp}.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(self.best_model, f)
        print(f"\nModel saved to: {model_path}")
        
        # Save scaler
        scaler_path = f"{output_dir}/prematch_scaler_{timestamp}.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"Scaler saved to: {scaler_path}")
        
        # Save feature names and metadata
        metadata = {
            'model_type': 'pre-match',
            'model_name': self.best_model_name,
            'timestamp': timestamp,
            'train_size': len(self.X_train),
            'test_size': len(self.X_test),
            'features': self.feature_names,
            'num_features': len(self.feature_names),
            'target_classes': {0: 'Draw', 1: 'Home Win', 2: 'Away Win'}
        }
        
        metadata_path = f"{output_dir}/prematch_metadata_{timestamp}.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Metadata saved to: {metadata_path}")
        
        return model_path, scaler_path, metadata_path


def main():
    """Main training pipeline"""
    print("="*60)
    print("PRE-MATCH FOOTBALL OUTCOME PREDICTION")
    print("="*60)
    print("\nThis model predicts match outcomes using ONLY information")
    print("available BEFORE the match starts (odds + team form)")
    
    # Initialize predictor
    predictor = PreMatchPredictor('data_new.csv')
    
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
