# Prediction Variables

This file documents the outcome categories generated for each football match. Each variable represents a specific, verifiable outcome relative to the designated "favorite" team. The `_home` or `_away` suffix indicates the venue of the match from the favorite team's perspective.

### Primary Match Outcomes (Full-Time)

-   `fav_win`: The favorite team won the match.
-   `draw`: The match ended in a draw.
-   `fav_loss`: The favorite team lost the match.
-   `fav_double_chance`: The favorite team won or drew the match (did not lose).

### Goal-Based Outcomes (Full-Time)

-   `btts_yes`: Both teams scored at least one goal.
-   `btts_no`: At least one team failed to score.
-   `fav_win_to_nil`: The favorite team won and the opponent scored zero goals.
-   `fav_failed_to_score`: The favorite team scored zero goals.

### Goal Totals (Over/Under)

-   `match_goals_over_2.5`: The total goals scored in the match by both teams was 3 or more.
-   `match_goals_under_2.5`: The total goals scored in the match by both teams was 2 or less.
-   `ht_match_goals_over_1.5`: The total goals scored in the first half was 2 or more.
-   `ht_match_goals_under_1.5`: The total goals scored in the first half was 1 or less.

### Half-Time Outcomes

-   `ht_fav_win`: The favorite team was leading at half-time.
-   `ht_draw`: The match was a draw at half-time.
-   `ht_fav_loss`: The favorite team was losing at half-time.

### Narrative & Combined Outcomes

-   `fav_comeback_win`: The favorite team was losing at half-time but won the match at full-time.
-   `fav_threw_lead_loss`: The favorite team was winning at half-time but lost the match at full-time.
-   `fav_scored_both_halves`: The favorite team scored at least one goal in the first half AND at least one goal in the second half.

### Goal Timing

-   `fav_scored_first`: The favorite team scored the first goal of the match (where inferable).
-   `most_goals_1h`: More goals were scored in the first half than the second half.
-   `most_goals_2h`: More goals were scored in the second half than the first half.
-   `most_goals_equal`: An equal number of goals were scored in both halves.