---
title: "Welcome to SoccerData’s docs!"
---

# Welcome to SoccerData’s docs!

Release v1.8.7. (`pip install soccerdata`)

[![SoccerData Downloads Per Month Badge](https://pepy.tech/badge/soccerdata/month)](https://pepy.tech/project/soccerdata)
[![License Badge](https://img.shields.io/pypi/l/soccerdata.svg)](https://pypi.org/project/soccerdata/)
[![Python Version Support Badge](https://img.shields.io/pypi/pyversions/soccerdata.svg)](https://pypi.org/project/soccerdata/)

**SoccerData** is a collection of scrapers to gather soccer data from popular
websites, including [Club Elo](https://www.clubelo.com/), [ESPN](https://www.espn.com/soccer/), [FBref](https://www.fbref.com/en/), [FiveThirtyEight](https://fivethirtyeight.com/soccer-predictions/),
[Football-Data.co.uk](https://www.football-data.co.uk/), [FotMob](https://fotmob.com/), [Sofascore](https://www.sofascore.com/), [SoFIFA](https://sofifa.com/), [Understat](https://understat.com/) and [WhoScored](https://www.whoscored.com/).

```
import soccerdata as sd

# Create a scraper class instance for the 2020/21 Premier League
fbref = sd.FBref('ENG-Premier League', '2021')

# Fetch data
games = fbref.read_schedule()
team_season_stats = fbref.read_team_season_stats(stat_type="passing")
player_season_stats = fbref.read_player_season_stats(stat_type="standard")
```

---

**Main features**

* Access current and historical soccer fixtures, forecasts, detailed match
  stats, event stream data and more.
* All data is provided in the form of Pandas DataFrames with sensible,
  matching column names and identifiers across datasets to make working with
  the data and combining data from multiple sources easy.
* Data is only downloaded when needed and cached locally to speed up your
  analyis scripts.
* Integrates with the [socceraction](https://socceraction.readthedocs.io/en/latest/documentation/data/opta.html#whoscored) package to allow analysis of event stream
  data.

Do you like it? [Let’s dive in!](intro.md)