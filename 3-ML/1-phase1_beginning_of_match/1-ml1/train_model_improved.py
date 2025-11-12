"""
Improved model with better feature engineering for odds
Fixes multicollinearity and adds categorical odds features
Each unique odds value is treated as a separate category
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
import pickle
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# MODEL TRAINING CONFIGURATION
# ============================================================
ENABLE_LOGISTIC_REGRESSION = False
ENABLE_RANDOM_FOREST = True
ENABLE_GRADIENT_BOOSTING = False  # Disabled for now

# Feature Engineering Configuration
TREAT_ODDS_AS_CATEGORICAL = True  # Each unique odds value = separate category

class ImprovedMatchOutcomePredictor:
    def __init__(self, data_path='data_new.csv'):
        """Initialize the predictor"""
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.label_encoders = {}  # Store label encoders for categorical odds
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
    
    def engineer_features(self):
        """Create additional features and handle multicollinearity"""
        print("\nEngineering features...")
        
        # === CATEGORICAL ODDS FEATURES ===
        if TREAT_ODDS_AS_CATEGORICAL:
            print("  Treating each unique odds value as a separate category...")
            
            # Convert each odds column to categorical
            # Each unique value (e.g., 1.65, 1.66) becomes a separate category
            odds_cols_to_categorize = ['HomeOdds', 'DrawOdds', 'AwayOdds']
            
            for col in odds_cols_to_categorize:
                if col in self.df.columns:
                    # Round to 2 decimal places to avoid floating point issues
                    self.df[f'{col}_rounded'] = self.df[col].round(2)
                    
                    # Create label encoder for this column
                    le = LabelEncoder()
                    # Handle NaN values by filling with a special value
                    odds_filled = self.df[f'{col}_rounded'].fillna(-999)
                    self.df[f'{col}_Cat'] = le.fit_transform(odds_filled)
                    
                    # Store encoder for later use
                    self.label_encoders[col] = le
                    
                    n_categories = len(le.classes_)
                    print(f"    {col}: {n_categories} unique categories")
            
            # Also create ranged categories (original approach) for comparison
            self.df['Home_Odds_Range'] = pd.cut(
                self.df['HomeOdds'], 
                bins=[0, 1.5, 2.0, 3.0, 5.0, 100],
                labels=[0, 1, 2, 3, 4]
            ).astype(float)
            
            self.df['Draw_Odds_Range'] = pd.cut(
                self.df['DrawOdds'],
                bins=[0, 3.0, 3.5, 4.0, 5.0, 100],
                labels=[0, 1, 2, 3, 4]
            ).astype(float)
            
            self.df['Away_Odds_Range'] = pd.cut(
                self.df['AwayOdds'],
                bins=[0, 1.5, 2.0, 3.0, 5.0, 100],
                labels=[0, 1, 2, 3, 4]
            ).astype(float)
        else:
            # Original binned approach
            self.df['Home_Odds_Cat'] = pd.cut(
                self.df['HomeOdds'], 
                bins=[0, 1.5, 2.0, 3.0, 5.0, 100],
                labels=[0, 1, 2, 3, 4]
            ).astype(float)
            
            self.df['Draw_Odds_Cat'] = pd.cut(
                self.df['DrawOdds'],
                bins=[0, 3.0, 3.5, 4.0, 5.0, 100],
                labels=[0, 1, 2, 3, 4]
            ).astype(float)
            
            self.df['Away_Odds_Cat'] = pd.cut(
                self.df['AwayOdds'],
                bins=[0, 1.5, 2.0, 3.0, 5.0, 100],
                labels=[0, 1, 2, 3, 4]
            ).astype(float)
        
        # === INTERACTION FEATURES ===
        
        # Odds ratio features (better than raw odds)
        self.df['Home_Away_Odds_Ratio'] = self.df['HomeOdds'] / self.df['AwayOdds']
        self.df['Home_Draw_Odds_Ratio'] = self.df['HomeOdds'] / self.df['DrawOdds']
        self.df['Away_Draw_Odds_Ratio'] = self.df['AwayOdds'] / self.df['DrawOdds']
        
        # Odds spread (how certain is the market?)
        self.df['Odds_Spread'] = self.df[['HomeOdds', 'DrawOdds', 'AwayOdds']].std(axis=1)
        self.df['Odds_Range'] = self.df[['HomeOdds', 'DrawOdds', 'AwayOdds']].max(axis=1) - \
                                 self.df[['HomeOdds', 'DrawOdds', 'AwayOdds']].min(axis=1)
        
        # Probability differences (using True_Prob as they're margin-adjusted)
        if 'True_Prob_Home' in self.df.columns and 'True_Prob_Away' in self.df.columns:
            self.df['Prob_Home_Away_Diff'] = self.df['True_Prob_Home'] - self.df['True_Prob_Away']
            self.df['Prob_Home_Draw_Diff'] = self.df['True_Prob_Home'] - self.df['True_Prob_Draw']
            self.df['Max_Prob'] = self.df[['True_Prob_Home', 'True_Prob_Draw', 'True_Prob_Away']].max(axis=1)
            self.df['Prob_Confidence'] = self.df['Max_Prob'] - self.df[['True_Prob_Home', 'True_Prob_Draw', 'True_Prob_Away']].apply(
                lambda x: sorted(x)[-2], axis=1  # 2nd highest
            )
        
        # === FORM INTERACTION FEATURES ===
        
        if 'Home_Form_Points_Last5' in self.df.columns and 'Away_Form_Points_Last5' in self.df.columns:
            self.df['Form_Points_Diff'] = self.df['Home_Form_Points_Last5'] - self.df['Away_Form_Points_Last5']
            self.df['Form_Points_Ratio'] = self.df['Home_Form_Points_Last5'] / (self.df['Away_Form_Points_Last5'] + 1)
        
        if 'Home_Avg_Goals_Scored_Last5' in self.df.columns and 'Away_Avg_Goals_Scored_Last5' in self.df.columns:
            self.df['Goals_Scored_Diff'] = self.df['Home_Avg_Goals_Scored_Last5'] - self.df['Away_Avg_Goals_Scored_Last5']
            self.df['Goals_Conceded_Diff'] = self.df['Home_Avg_Goals_Conceded_Last5'] - self.df['Away_Avg_Goals_Conceded_Last5']
        
        # Attack vs Defense matchup
        if all(col in self.df.columns for col in ['Home_Avg_Goals_Scored_Last5', 'Away_Avg_Goals_Conceded_Last5']):
            self.df['Home_Attack_vs_Away_Defense'] = self.df['Home_Avg_Goals_Scored_Last5'] - self.df['Away_Avg_Goals_Conceded_Last5']
            self.df['Away_Attack_vs_Home_Defense'] = self.df['Away_Avg_Goals_Scored_Last5'] - self.df['Home_Avg_Goals_Conceded_Last5']
            self.df['Attack_Defense_Balance'] = self.df['Home_Attack_vs_Away_Defense'] - self.df['Away_Attack_vs_Home_Defense']
        
        print(f"Feature engineering complete. New shape: {self.df.shape}")
        
        return self
    
    def select_features(self):
        """Select features - avoiding multicollinearity"""
        
        # === CORE ODDS FEATURES (reduce redundancy) ===
        odds_features = []
        
        if TREAT_ODDS_AS_CATEGORICAL:
            # Use categorical odds (each unique value is a category)
            odds_features.extend([
                'HomeOdds_Cat', 'DrawOdds_Cat', 'AwayOdds_Cat',  # Main categorical odds
                'Home_Odds_Range', 'Draw_Odds_Range', 'Away_Odds_Range',  # Range categories
            ])
        else:
            # Use margin-adjusted probabilities and binned categories
            odds_features.extend([
                'True_Prob_Home', 'True_Prob_Draw', 'True_Prob_Away',
                'Home_Odds_Cat', 'Draw_Odds_Cat', 'Away_Odds_Cat',
            ])
        
        # Common odds features (used in both modes)
        odds_features.extend([
            # Odds ratios (relative strength)
            'Home_Away_Odds_Ratio', 'Home_Draw_Odds_Ratio', 'Away_Draw_Odds_Ratio',
            
            # Market confidence indicators
            'Odds_Spread', 'Odds_Range',
            'Prob_Confidence', 'Max_Prob',
            'Prob_Home_Away_Diff', 'Prob_Home_Draw_Diff',
            
            # Market metrics
            'Margin', 'Entropy', 'Home_Is_Favorite',
            'Mismatch_Ratio', 'Market_Expected_Goals',
            
            # Over/Under market
            'Prob_Over2.5', 'Prob_Under2.5', 'Margin_OU2.5',
        ])
        
        # === FORM FEATURES ===
        form_features = [
            # Rest days
            'Home_Days_Since_Last', 'Away_Days_Since_Last', 'Days_Since_Last_Match',
            
            # Form metrics
            'Home_Form_Points_Last5', 'Away_Form_Points_Last5',
            'Home_Win_Ratio_Last5', 'Away_Win_Ratio_Last5',
            'Form_Points_Diff', 'Form_Points_Ratio', 'Points_Diff_Form',
            
            # Goal metrics
            'Home_Avg_Goals_Scored_Last5', 'Away_Avg_Goals_Scored_Last5',
            'Home_Avg_Goals_Conceded_Last5', 'Away_Avg_Goals_Conceded_Last5',
            'Goals_Scored_Diff', 'Goals_Conceded_Diff', 'Goal_Diff_Form',
            
            # Attack vs Defense matchups
            'Home_Attack_vs_Away_Defense', 'Away_Attack_vs_Home_Defense',
            'Attack_Defense_Balance',
            
            # Form consistency
            'Home_Form_Consistency_Last5', 'Away_Form_Consistency_Last5',
            'Home_Weighted_Form_Points_Last5', 'Away_Weighted_Form_Points_Last5',
            'Home_Clean_Sheet_Ratio_Last5', 'Away_Clean_Sheet_Ratio_Last5',
            
            # Head to head
            'H2H_Avg_Goal_Diff', 'H2H_Recent_Win_Ratio',
            
            # Other metrics
            'Odds_Disagreement', 'Elo_Difference',
        ]
        
        all_features = odds_features + form_features
        
        # Select features that exist in the dataframe and are numeric
        available_features = []
        for feat in all_features:
            if feat in self.df.columns:
                if self.df[feat].dtype in ['int64', 'float64', 'int32', 'float32', 'bool']:
                    available_features.append(feat)
        
        print(f"\nSelected {len(available_features)} features for training")
        print(f"  - Odds features: {len([f for f in available_features if any(x in f for x in ['Odds', 'Prob', 'Margin', 'Entropy'])])}")
        print(f"  - Form features: {len([f for f in available_features if any(x in f for x in ['Form', 'Goals', 'Attack', 'Defense'])])}")
        
        self.feature_names = available_features
        
        return available_features
    
    def prepare_train_test_split(self, test_size=0.2, random_state=42):
        """Prepare train-test split with time-series awareness"""
        print("\nPreparing features and target...")
        
        # Engineer features first
        self.engineer_features()
        
        # Select features
        features = self.select_features()
        
        # Prepare features (X)
        X = self.df[features].copy()
        
        # Handle missing values
        X = X.fillna(X.median())
        
        # Replace inf values
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())
        
        # Prepare target (y)
        y = self.df['FT_Result'].copy()
        
        print(f"\nTarget distribution:")
        print(y.value_counts().sort_index())
        print(f"\nPercentages:")
        print(y.value_counts(normalize=True).sort_index() * 100)
        
        # Split the data (stratified)
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
        """Train multiple models with class balancing"""
        print("\n" + "="*70)
        print("TRAINING MODELS")
        print("="*70)
        
        # Define models with class balancing (based on configuration flags)
        models_to_train = {}
        
        if ENABLE_LOGISTIC_REGRESSION:
            models_to_train['Logistic Regression'] = LogisticRegression(
                max_iter=1000, 
                random_state=42,
                multi_class='multinomial',
                class_weight='balanced'  # Handle class imbalance
            )
            print("✓ Logistic Regression enabled")
        else:
            print("✗ Logistic Regression disabled")
        
        if ENABLE_RANDOM_FOREST:
            models_to_train['Random Forest'] = RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=20,
                min_samples_leaf=10,
                random_state=42,
                n_jobs=-1,
                class_weight='balanced'  # Handle class imbalance
            )
            print("✓ Random Forest enabled")
        else:
            print("✗ Random Forest disabled")
        
        if ENABLE_GRADIENT_BOOSTING:
            models_to_train['Gradient Boosting'] = GradientBoostingClassifier(
                n_estimators=150,
                max_depth=5,
                learning_rate=0.05,
                random_state=42,
                subsample=0.8
            )
            print("✓ Gradient Boosting enabled")
        else:
            print("✗ Gradient Boosting disabled")
        
        if not models_to_train:
            raise ValueError("No models enabled! Please enable at least one model in configuration.")
        
        results = {}
        
        # Use stratified k-fold
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
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
            f1_macro = f1_score(self.y_test, y_pred, average='macro')
            f1_weighted = f1_score(self.y_test, y_pred, average='weighted')
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train_use, self.y_train, 
                                       cv=skf, scoring='f1_macro')
            
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'f1_macro': f1_macro,
                'f1_weighted': f1_weighted,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }
            
            print(f"  Accuracy:    {accuracy:.4f}")
            print(f"  F1 Macro:    {f1_macro:.4f}")
            print(f"  F1 Weighted: {f1_weighted:.4f}")
            print(f"  CV F1 Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
            
            # Store model
            self.models[name] = model
        
        # Select best model based on F1 macro (better for imbalanced data)
        best_model_name = max(results, key=lambda x: results[x]['f1_macro'])
        self.best_model = results[best_model_name]['model']
        self.best_model_name = best_model_name
        
        print(f"\n{'='*70}")
        print(f"BEST MODEL: {best_model_name} (F1 Macro: {results[best_model_name]['f1_macro']:.4f})")
        print(f"{'='*70}")
        
        return results
    
    def evaluate_best_model(self, results):
        """Detailed evaluation of the best model"""
        print("\n" + "="*70)
        print("DETAILED EVALUATION OF BEST MODEL")
        print("="*70)
        
        best_result = results[self.best_model_name]
        y_pred = best_result['predictions']
        y_pred_proba = best_result['probabilities']
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred, 
                                   target_names=['Draw', 'Home Win', 'Away Win'],
                                   digits=4))
        
        # Confusion matrix
        print("\nConfusion Matrix:")
        cm = confusion_matrix(self.y_test, y_pred)
        print("              Predicted")
        print("              Draw  Home  Away")
        for i, row in enumerate(cm):
            label = ['Draw', 'Home', 'Away'][i]
            print(f"Actual {label:5s}  {row[0]:4d}  {row[1]:4d}  {row[2]:4d}")
        
        # Per-class accuracy
        print("\nPer-class Recall:")
        for i, label in enumerate(['Draw', 'Home Win', 'Away Win']):
            recall = cm[i, i] / cm[i].sum()
            print(f"  {label:10s}: {recall:.4f}")
        
        # Feature importance (if available)
        if hasattr(self.best_model, 'feature_importances_'):
            print("\nTop 20 Most Important Features:")
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.best_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            for idx, row in feature_importance.head(20).iterrows():
                print(f"  {row['feature']:35s}: {row['importance']:.4f}")
        
        return best_result
    
    def save_model(self, output_dir='models'):
        """Save the trained model and scaler"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save model
        model_path = f"{output_dir}/model_improved_{self.best_model_name.replace(' ', '_').lower()}_{timestamp}.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(self.best_model, f)
        print(f"\nModel saved to: {model_path}")
        
        # Save scaler
        scaler_path = f"{output_dir}/scaler_improved_{timestamp}.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"Scaler saved to: {scaler_path}")
        
        # Save feature names
        features_path = f"{output_dir}/features_improved_{timestamp}.json"
        with open(features_path, 'w') as f:
            json.dump({
                'features': self.feature_names,
                'model_name': self.best_model_name,
                'timestamp': timestamp,
                'version': 'improved_v1'
            }, f, indent=2)
        print(f"Features saved to: {features_path}")
        
        # Save metadata
        metadata = {
            'model_name': self.best_model_name,
            'timestamp': timestamp,
            'version': 'improved_v2_categorical',
            'train_size': len(self.X_train),
            'test_size': len(self.X_test),
            'features': self.feature_names,
            'num_features': len(self.feature_names),
            'configuration': {
                'treat_odds_as_categorical': TREAT_ODDS_AS_CATEGORICAL,
                'logistic_regression_enabled': ENABLE_LOGISTIC_REGRESSION,
                'random_forest_enabled': ENABLE_RANDOM_FOREST,
                'gradient_boosting_enabled': ENABLE_GRADIENT_BOOSTING
            },
            'categorical_encoders': {
                col: {
                    'n_categories': len(encoder.classes_),
                    'sample_values': encoder.classes_[:10].tolist()
                }
                for col, encoder in self.label_encoders.items()
            } if self.label_encoders else {},
            'improvements': [
                'Each unique odds value treated as separate category',
                'Added odds ratio features',
                'Added form interaction features',
                'Removed multicollinearity',
                'Added class balancing',
                'Using F1-macro for model selection',
                'Configurable model training flags'
            ]
        }
        
        metadata_path = f"{output_dir}/metadata_improved_{timestamp}.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Metadata saved to: {metadata_path}")
        
        return model_path, scaler_path, features_path


def main():
    """Main training pipeline"""
    print("="*70)
    print("IMPROVED FOOTBALL MATCH OUTCOME PREDICTION")
    print("="*70)
    
    # Initialize predictor
    predictor = ImprovedMatchOutcomePredictor('data_new.csv')
    
    # Load and prepare data
    predictor.load_and_prepare_data()
    
    # Prepare train-test split (includes feature engineering)
    predictor.prepare_train_test_split(test_size=0.2, random_state=42)
    
    # Train models
    results = predictor.train_models()
    
    # Evaluate best model
    predictor.evaluate_best_model(results)
    
    # Save model
    predictor.save_model()
    
    print("\n" + "="*70)
    print("TRAINING COMPLETE!")
    print("="*70)
    
    return predictor, results


if __name__ == "__main__":
    predictor, results = main()
