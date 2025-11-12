# Model Improvement Recommendations

## Current Status
- **Accuracy**: 57% (Fixed from 100% - data leakage removed)
- **Main Issue**: Model over-predicts home wins, under-predicts draws

## Problems & Solutions

### 1. Class Imbalance
**Problem**: Target distribution is imbalanced
- Home Win: 44%
- Away Win: 31%
- Draw: 25%

**Solutions**:
```python
# Option A: Use class weights
RandomForestClassifier(class_weight='balanced')
GradientBoostingClassifier()  # manually set sample_weight

# Option B: SMOTE or undersampling
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)
```

### 2. Feature Engineering Improvements

**Add interaction features**:
```python
# Form difference features
'Form_Points_Diff' = Home_Form_Points - Away_Form_Points
'Goals_Scored_Diff' = Home_Goals_Scored - Away_Goals_Scored

# Odds interactions
'Odds_Confidence' = 1 / HomeOdds * DrawOdds * AwayOdds
'Home_Advantage_Strength' = HomeOdds / AwayOdds

# Recent form momentum
'Home_Last3_vs_Last5' = (Home_Form_Last3 - Home_Form_Last5)
```

**Add league strength indicators**:
- Average goals per game in league
- League competitiveness index
- Home advantage strength per league

### 3. Model Improvements

**Current**: Random Forest with default parameters

**Try**:
```python
# A. Tune Random Forest
RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    class_weight='balanced'
)

# B. XGBoost (usually better for imbalanced data)
import xgboost as xgb
xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    scale_pos_weight=2  # for class imbalance
)

# C. LightGBM (faster, often better)
import lightgbm as lgb
lgb.LGBMClassifier(
    n_estimators=200,
    num_leaves=31,
    learning_rate=0.05,
    class_weight='balanced'
)

# D. Ensemble of models (stacking)
from sklearn.ensemble import VotingClassifier
```

### 4. Evaluation Metrics

**Don't just use accuracy!** Football betting needs:
```python
# Profit-based evaluation
def betting_profit(y_true, y_pred_proba, odds):
    """Calculate profit if betting on predictions"""
    # Only bet when probability > odds imply
    # Track ROI

# Use F1-score per class
from sklearn.metrics import f1_score
f1_score(y_test, y_pred, average=None)  # per class

# Use log loss (better for probability calibration)
from sklearn.metrics import log_loss
```

### 5. Data Quality

**Check for**:
- Missing odds data (some matches have missing HomeDrawOdds)
- Outlier odds (very high/low odds may indicate data errors)
- Season boundary issues (form features across seasons)

**Add**:
```python
# Odds validation
df = df[df['HomeOdds'].between(1.01, 50)]
df = df[df['DrawOdds'].between(1.5, 30)]

# Feature scaling check
scaler.fit(X_train[outlier_mask == False])
```

### 6. Cross-Validation Strategy

**Current**: Random split (may have temporal leakage)

**Better**:
```python
# Time-series split (respect temporal order)
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)

# Or group by season
from sklearn.model_selection import GroupKFold
gkf = GroupKFold(n_splits=5)
cv_scores = cross_val_score(model, X, y, cv=gkf, groups=df['Season'])
```

### 7. Probability Calibration

Models may output poorly calibrated probabilities:
```python
from sklearn.calibration import CalibratedClassifierCV

# Calibrate probabilities
calibrated_model = CalibratedClassifierCV(
    base_model, 
    method='isotonic',  # or 'sigmoid'
    cv=5
)
calibrated_model.fit(X_train, y_train)
```

## Priority Actions (Quick Wins)

1. **Add class weights** to Random Forest
2. **Add interaction features** (form differences, odds ratios)
3. **Try XGBoost** with class weighting
4. **Use F1-score** per class instead of just accuracy
5. **Implement time-series CV** to prevent temporal leakage

## Expected Improvements

With these changes, you should see:
- **Draw prediction**: 5% → 30-40% recall
- **Overall accuracy**: 57% → 60-65%
- **F1-score**: Improve balance across all classes
- **Betting ROI**: Positive returns when betting on high-confidence predictions

## Notes on Realistic Expectations

**Football is inherently unpredictable!**
- Professional betting models: 55-60% accuracy
- 70%+ accuracy is unrealistic (if you see this, check for data leakage)
- Focus on **probability calibration** and **ROI** rather than accuracy
- Even 53-55% accuracy with good odds can be profitable
