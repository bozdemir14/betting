# 🎯 Match Prediction - Quick Start Guide

## Three Ways to Use the Model

### 1️⃣ **Interactive Mode (Easiest)**
Run the interactive script and follow the prompts:

```bash
python predict_interactive.py
```

You'll be asked to enter:
- Team names
- Betting odds (home/draw/away)
- Optional: Over/Under 2.5 odds
- Optional: Team form data

### 2️⃣ **Python Script (Most Flexible)**
Use in your own Python code:

```python
from predict import MatchPredictor

# Initialize predictor
predictor = MatchPredictor()

# Make prediction with just odds
result = predictor.predict_from_odds(
    home_odds=1.85,
    draw_odds=3.60,
    away_odds=4.20
)

# Print results
predictor.print_prediction(result, "Team A", "Team B")
```

### 3️⃣ **With Team Form Data (Most Accurate)**

```python
from predict import MatchPredictor

predictor = MatchPredictor()

# Define team form (from last 5 matches)
home_form = {
    'avg_goals_scored': 1.8,      # Average goals scored
    'avg_goals_conceded': 1.2,    # Average goals conceded
    'form_points': 9,              # Total points (W=3, D=1, L=0)
    'win_ratio': 0.6               # Win percentage (3/5 = 0.6)
}

away_form = {
    'avg_goals_scored': 1.4,
    'avg_goals_conceded': 1.6,
    'form_points': 6,
    'win_ratio': 0.4
}

# Make prediction
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
```

## 📊 Understanding the Output

The prediction will show:

1. **Odds**: The betting odds you provided
2. **Prediction**: Most likely outcome with confidence %
3. **Probabilities**: Model's probability for each outcome (Draw/Home/Away)
4. **Betting Recommendation**: 
   - Suggested bet
   - Confidence level (High/Medium/Low)
   - Expected Value (EV) - positive means value bet
   - Advice on whether to place the bet

### Interpreting Expected Value (EV)

- **EV > 20%**: Strong value bet ✅
- **EV > 10%**: Good value bet ✅
- **EV > 0%**: Slight value, consider bet ⚠️
- **EV < 0%**: No value, avoid bet ❌

## 💡 Examples

### Example 1: Strong Favorite
```python
result = predictor.predict_from_odds(
    home_odds=1.40,  # Strong home favorite
    draw_odds=4.50,
    away_odds=8.00
)
```

### Example 2: Even Match
```python
result = predictor.predict_from_odds(
    home_odds=2.60,  # Balanced odds
    draw_odds=3.20,
    away_odds=2.80
)
```

### Example 3: Away Favorite
```python
result = predictor.predict_from_odds(
    home_odds=5.50,  # Away team favored
    draw_odds=3.80,
    away_odds=1.65
)
```

## 🎲 Model Performance

Based on test data:
- **Overall Accuracy**: 58.9%
- **Draw Prediction**: 85.7% accuracy
- **Away Win Prediction**: 60.2% accuracy
- **Home Win Prediction**: 15.1% accuracy

**Note**: The model is most reliable for predicting draws and away wins. Home win predictions have lower accuracy.

## 📝 Tips for Best Results

1. **Always include Over/Under 2.5 odds** when available (improves accuracy)
2. **Add team form data** for more accurate predictions
3. **Look for high confidence predictions** (>60%)
4. **Focus on positive EV bets** (expected value > 10%)
5. **Use as one tool** in your betting strategy, not the only factor

## ⚠️ Disclaimer

This is a predictive model for educational purposes. Past performance does not guarantee future results. Always bet responsibly and never bet more than you can afford to lose.
