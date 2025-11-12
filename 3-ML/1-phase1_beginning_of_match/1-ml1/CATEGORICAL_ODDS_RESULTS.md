# Categorical Odds Training Results

## Configuration

### Model Training Flags
```python
ENABLE_LOGISTIC_REGRESSION = True   ✓ Enabled
ENABLE_RANDOM_FOREST = True         ✓ Enabled
ENABLE_GRADIENT_BOOSTING = False    ✗ Disabled
```

### Odds Treatment
```python
TREAT_ODDS_AS_CATEGORICAL = True
```

**Each unique odds value is now a separate category:**
- `1.65` and `1.66` are completely different categories
- No numeric relationship assumed between similar values
- The model learns patterns for each specific odds value independently

## Categorical Encoding Results

### Unique Categories Created:
- **HomeOdds**: 607 unique categories
- **DrawOdds**: 510 unique categories  
- **AwayOdds**: 863 unique categories

**Total**: 1,980 unique odds values treated as separate categories!

This means:
- Odds `1.65` has its own pattern
- Odds `1.66` has its own pattern
- Odds `2.50` has its own pattern
- etc.

## Training Results

### Models Trained:
1. ✓ **Logistic Regression** - Best Model
2. ✓ **Random Forest**
3. ✗ Gradient Boosting (disabled)

### Performance Comparison:

| Model | Accuracy | F1 Macro | F1 Weighted | CV Score |
|-------|----------|----------|-------------|----------|
| **Logistic Regression** | **53.6%** | **0.5107** | **0.5386** | 0.4803 ± 0.0073 |
| Random Forest | 54.6% | 0.5017 | 0.5363 | 0.4927 ± 0.0063 |

**Winner**: Logistic Regression (better F1 Macro for balanced predictions)

## Detailed Results (Logistic Regression)

### Classification Report:
```
              precision    recall  f1-score   support
        Draw     0.3234    0.3406    0.3318       320
    Home Win     0.6660    0.6313    0.6482       556
    Away Win     0.5439    0.5607    0.5522       387

    accuracy                         0.5360      1263
   macro avg     0.5111    0.5109    0.5107      1263
weighted avg     0.5418    0.5360    0.5386      1263
```

### Confusion Matrix:
```
              Predicted
              Draw  Home  Away
Actual Draw    109   107   104
Actual Home    127   351    78
Actual Away    101    69   217
```

### Per-Class Performance:
- **Draw Recall**: 34.1% (better than previous 33.4%)
- **Home Win Recall**: 63.1%
- **Away Win Recall**: 56.1%

## Comparison with Previous Approach

### Previous (Odds as Ranges):
- HomeOdds binned into 5 ranges: [0-1.5, 1.5-2.0, 2.0-3.0, 3.0-5.0, 5.0+]
- Draw Recall: 33.4%
- F1 Macro: 0.5152
- Accuracy: 54.2%

### Current (Each Odds = Category):
- HomeOdds: 607 unique categories (every value separate)
- Draw Recall: 34.1% ↑ (+0.7%)
- F1 Macro: 0.5107 ↓ (-0.0045)
- Accuracy: 53.6% ↓ (-0.6%)

### Analysis:
The categorical approach:
- ✓ **Slightly better draw prediction** (+0.7%)
- ✗ Slightly lower overall F1 and accuracy
- ⚠️ **Much higher dimensionality** (607+510+863 = 1,980 categories vs 15 bins)
- ⚠️ **Risk of overfitting** to specific odds values
- ⚠️ **Sparse data** - many odds values appear only a few times

## Why This Approach is Interesting (but risky)

### Advantages:
1. **Captures market inefficiencies** - If odds `1.85` consistently underperform vs `1.86`
2. **No assumptions** about numeric relationships
3. **Bookmaker-specific patterns** - Each odds reflects bookmaker confidence
4. **Draw prediction improved** slightly

### Disadvantages:
1. **High dimensionality** - 1,980 categories is a LOT
2. **Sparse data** - Many odds values appear only 1-5 times
3. **Overfitting risk** - Model may memorize specific odds
4. **Poor generalization** - New odds values (1.657) have no training data
5. **Computational cost** - More features = slower training

## Recommendations

### For Production Use:
**Use a hybrid approach:**

```python
# Keep both categorical AND range features
- HomeOdds_Cat (607 categories) - for specific patterns
- Home_Odds_Range (5 bins) - for generalization
- Home_Away_Odds_Ratio - for relative strength
- True_Prob_Home - for numeric relationships
```

This gives the model flexibility to:
- Learn specific odds patterns when data is sufficient
- Fall back to ranges/ratios when specific odds are rare
- Capture both categorical and continuous relationships

### When to Use Full Categorical:
✓ **Large dataset** (>100k matches)
✓ **Many samples per odds** value (>50 per category)
✓ **Market inefficiency detection** (arbitrage opportunities)
✓ **Ensemble with other approaches**

### When to Use Ranges:
✓ **Smaller dataset** (<10k matches) ← **Your case: 6,315 matches**
✓ **Better generalization** needed
✓ **Interpretability** matters
✓ **Production stability** required

## Next Steps

### Option 1: Increase Model Capacity
Try models that handle high-dimensional categorical data better:
```python
# XGBoost - excellent with categories
import xgboost as xgb
xgb.XGBClassifier(
    enable_categorical=True,
    max_cat_to_onehot=100  # Use native categorical handling
)

# CatBoost - specifically designed for categorical features
from catboost import CatBoostClassifier
CatBoostClassifier(
    cat_features=['HomeOdds_Cat', 'DrawOdds_Cat', 'AwayOdds_Cat']
)
```

### Option 2: Reduce Dimensionality
```python
# Group rare odds values
def group_rare_categories(df, col, min_count=10):
    value_counts = df[col].value_counts()
    rare_values = value_counts[value_counts < min_count].index
    df[col] = df[col].replace(rare_values, -1)  # "Other" category
    return df
```

### Option 3: Hybrid Approach (RECOMMENDED)
Keep both categorical and numeric features - let the model decide which to use.

## Files Saved

- Model: `models/model_improved_logistic_regression_20251109_233609.pkl`
- Scaler: `models/scaler_improved_20251109_233609.pkl`
- Features: `models/features_improved_20251109_233609.json`
- Metadata: `models/metadata_improved_20251109_233609.json`

The metadata includes:
- Number of categories per odds type
- Sample values for each category
- Configuration flags used
- All improvements applied
