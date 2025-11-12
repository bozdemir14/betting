"""
Interactive script to predict a single match
"""
from predict import MatchPredictor

def get_float_input(prompt, optional=False):
    """Get float input from user"""
    while True:
        try:
            value = input(prompt)
            if optional and value.strip() == '':
                return None
            return float(value)
        except ValueError:
            if optional:
                print("  Invalid input. Press Enter to skip or enter a number.")
            else:
                print("  Invalid input. Please enter a number.")

def main():
    print("=" * 60)
    print("FOOTBALL MATCH OUTCOME PREDICTOR")
    print("=" * 60)
    print("\nLoading model...")
    
    predictor = MatchPredictor()
    
    print("\n✓ Model loaded successfully!")
    print("\nEnter match details:")
    print("-" * 60)
    
    # Get team names
    home_team = input("\nHome team name: ").strip() or "Home Team"
    away_team = input("Away team name: ").strip() or "Away Team"
    
    print("\n📊 BETTING ODDS (decimal format, e.g., 1.85):")
    home_odds = get_float_input("  Home win odds: ")
    draw_odds = get_float_input("  Draw odds: ")
    away_odds = get_float_input("  Away win odds: ")
    
    print("\n⚽ OVER/UNDER 2.5 GOALS (optional, press Enter to skip):")
    under_2_5 = get_float_input("  Under 2.5 goals odds: ", optional=True)
    over_2_5 = get_float_input("  Over 2.5 goals odds: ", optional=True)
    
    # Optional: Team form
    print("\n📈 TEAM FORM (optional, press Enter to skip all):")
    add_form = input("  Add team form data? (y/n): ").lower().strip()
    
    home_form = None
    away_form = None
    
    if add_form == 'y':
        print(f"\n  {home_team} - Last 5 matches:")
        home_form = {
            'avg_goals_scored': get_float_input("    Average goals scored: ", optional=True),
            'avg_goals_conceded': get_float_input("    Average goals conceded: ", optional=True),
            'form_points': get_float_input("    Points (3 per win, 1 per draw): ", optional=True),
            'win_ratio': get_float_input("    Win ratio (e.g., 0.6 for 60%): ", optional=True)
        }
        
        print(f"\n  {away_team} - Last 5 matches:")
        away_form = {
            'avg_goals_scored': get_float_input("    Average goals scored: ", optional=True),
            'avg_goals_conceded': get_float_input("    Average goals conceded: ", optional=True),
            'form_points': get_float_input("    Points (3 per win, 1 per draw): ", optional=True),
            'win_ratio': get_float_input("    Win ratio (e.g., 0.6 for 60%): ", optional=True)
        }
    
    # Make prediction
    print("\n\n🤖 Analyzing match...")
    result = predictor.predict_from_odds(
        home_odds=home_odds,
        draw_odds=draw_odds,
        away_odds=away_odds,
        under_2_5=under_2_5,
        over_2_5=over_2_5,
        home_form=home_form,
        away_form=away_form
    )
    
    # Print results
    print("\n")
    predictor.print_prediction(result, home_team, away_team)
    
    # Ask if user wants to predict another match
    print("\n")
    again = input("Predict another match? (y/n): ").lower().strip()
    if again == 'y':
        print("\n" * 2)
        main()
    else:
        print("\n👋 Thanks for using the predictor!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Prediction cancelled. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check your inputs and try again.")
