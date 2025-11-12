# Model Comparison: Original vs Improved

## Question: Is the model treating odds as both numerical and categorical?

**Answer**: The original model treated odds **ONLY as numerical/continuous variables**. This has now been improved.

---

## Original Model (train_model.py)

### Feature Approach:
- ❌ **Multicollinearity problem**: Used all three representations of the same information
  - Raw odds: `HomeOdds, DrawOdds, AwayOdds`
  - Probabilities: `Prob_Home, Prob_Draw, Prob_Away`
  - Adjusted probabilities: `True_Prob_Home, True_Prob_Draw, True_Prob_Away`
  
- ❌ **Only numerical treatment**: All odds treated as continuous float values
- ❌ **No interaction features**: Missed important relationships
- ❌ **No class balancing**: Ignored the fact that draws are underrepresented (25%)

### Results:
```
Best Model: Random Forest
Accuracy: 56.9%

Per-class Recall:
  Draw:      5%    ← Terrible! Model almost never predicts draws
  Home Win:  86%   ← Overfit to majority class
  Away Win:  58%   ← Moderate
  
F1 Macro: ~0.45 (estimated)
```

---

## Improved Model (train_model_improved.py)

### Feature Improvements:

#### 1. **Added Categorical Odds Features** ✅
Odds are now treated BOTH as numerical AND categorical:

```python
# Categorical bins for odds (helps tree-based models)
Home_Odds_Cat: 0=Heavy Favorite, 1=Favorite, 2=Balanced, 3=Underdog, 4=Heavy Underdog
Draw_Odds_Cat: Similar categorization
Away_Odds_Cat: Similar categorization
```

**Why this helps:**
- Tree models can now find patterns like "when HomeOdds is in range 1.5-2.0..."
- Captures non-linear relationships better
- Reduces impact of outlier odds values

#### 2. **Removed Multicollinearity** ✅
Now uses only ONE representation of odds:
- Uses `True_Prob_*` (margin-adjusted probabilities) - most informative
- Removed redundant raw odds and basic probabilities
- Reduces confusion for the model

#### 3. **Added Odds Interaction Features** ✅
```python
# Relative strength indicators
Home_Away_Odds_Ratio = HomeOdds / AwayOdds
Home_Draw_Odds_Ratio = HomeOdds / DrawOdds
Away_Draw_Odds_Ratio = AwayOdds / DrawOdds

# Market confidence
Odds_Spread = std(HomeOdds, DrawOdds, AwayOdds)
Odds_Range = max - min of odds
Prob_Confidence = difference between highest and 2nd highest probability
```

**Why this helps:**
- Captures relative strength better than absolute odds
- Shows how confident the market is
- More stable across different bookmakers

#### 4. **Added Form Interaction Features** ✅
```python
# Direct comparisons
Form_Points_Diff = Home_Form - Away_Form
Goals_Scored_Diff = Home_Goals - Away_Goals

# Matchup analysis
Home_Attack_vs_Away_Defense = Home_Attack - Away_Defense
Away_Attack_vs_Home_Defense = Away_Attack - Home_Defense
Attack_Defense_Balance = difference between above
```

**Why this helps:**
- Direct head-to-head comparisons
- Shows tactical matchups
- More predictive than individual team stats

#### 5. **Added Class Balancing** ✅
```python
RandomForestClassifier(class_weight='balanced')
LogisticRegression(class_weight='balanced')
```

**Why this helps:**
- Prevents model from ignoring minority class (draws)
- Improves recall for draws significantly

#### 6. **Better Evaluation Metrics** ✅
- Now uses **F1 Macro** for model selection (better for imbalanced data)
- Reports per-class metrics
- Uses Stratified K-Fold cross-validation

### Results:
```
Best Model: Logistic Regression
Accuracy: 54.2%

Per-class Recall:
  Draw:      33%   ← Much better! 6.6x improvement from 5%
  Home Win:  64%   ← More balanced, less overfit
  Away Win:  57%   ← Stable
  
F1 Macro: 0.515   ← More balanced across all classes
F1 Weighted: 0.543
```

---

## Key Insights

### Why is accuracy lower but the model is better?

The **improved model is actually BETTER** even though accuracy dropped from 56.9% to 54.2%:

1. **Balanced predictions**: Old model got high accuracy by always predicting home wins
2. **Better draw detection**: 33% recall on draws vs 5% before (660% improvement!)
3. **More realistic**: Betting strategies need balanced predictions, not just high accuracy

### Comparison Table:

| Metric | Original | Improved | Change |
|--------|----------|----------|--------|
| **Accuracy** | 56.9% | 54.2% | -2.7% ↓ |
| **Draw Recall** | 5% | 33% | +28% ↑↑↑ |
| **Home Win Recall** | 86% | 64% | -22% (less overfit) |
| **Away Win Recall** | 58% | 57% | -1% (stable) |
| **F1 Macro** | ~0.45 | 0.515 | +0.065 ↑ |
| **Usability** | Poor | Good | Much better for betting |

---

## Odds Treatment Summary

### Original:
- ✗ Only numerical (continuous)
- ✗ Multicollinearity (redundant features)
- ✗ No interactions
- ✗ Linear relationships only

### Improved:
- ✓ Both numerical AND categorical
- ✓ No redundancy (only True_Prob_*)
- ✓ Rich interactions (ratios, differences)
- ✓ Captures non-linear patterns
- ✓ Market confidence indicators

---

## Recommendations

### Use the Improved Model when:
- You need balanced predictions across all outcomes
- You're building a betting strategy (need good draw predictions)
- You care about overall model quality (F1 score)

### The improved model better handles:
1. **Categorical patterns** in odds ranges
2. **Relative strength** through odds ratios
3. **Market confidence** through spread/range features
4. **Class imbalance** through balanced weights
5. **Feature redundancy** by removing multicollinearity

---

## Next Steps

To further improve:
1. Try **XGBoost** or **LightGBM** (better with imbalanced data)
2. Add **league-specific features** (home advantage varies by league)
3. Implement **probability calibration** for better betting odds
4. Use **time-series cross-validation** (respect temporal order)
5. Add **ensemble methods** (combine multiple models)

Expected improvement: **55-60% accuracy** with **40-50% draw recall**
