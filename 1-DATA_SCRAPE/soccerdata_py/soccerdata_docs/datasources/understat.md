---
title: "Understat"
---

This page was generated from
[doc/datasources/Understat.ipynb](https://github.com/probberechts/soccerdata/blob/1.8.7/doc/datasources/Understat.ipynb).  
You can [download the notebook](Understat.ipynb),

```
[2]:
```

```
import soccerdata as sd
```

# Understat

```
[3]:
```

```
understat = sd.Understat(leagues="ENG-Premier League", seasons="2015/2016")
print(understat.__doc__)
```

```
Provides pd.DataFrames from data at https://understat.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/Understat``.

    Parameters
    ----------
    proxy : 'tor' or dict or list(dict) or callable, optional
        Use a proxy to hide your IP address. Valid options are:
            - "tor": Uses the Tor network. Tor should be running in
              the background on port 9050.
            - dict: A dictionary with the proxy to use. The dict should be
              a mapping of supported protocols to proxy addresses. For example::

                  {
                      'http': 'http://10.10.1.10:3128',
                      'https': 'http://10.10.1.10:1080',
                  }

            - list(dict): A list of proxies to choose from. A different proxy will
              be selected from this list after failed requests, allowing rotating
              proxies.
            - callable: A function that returns a valid proxy. This function will
              be called after failed requests, allowing rotating proxies.
    no_cache : bool
        If True, will not use cached data.
    no_store : bool
        If True, will not store downloaded data.
    data_dir : Path
        Path to directory where data will be cached.
```

## Leagues

```
[4]:
```

```
leagues = understat.read_leagues()
leagues.head()
```

```
[4]:
```

|  | league\_id | url |
| --- | --- | --- |
| league |  |  |
| ENG-Premier League | 1 | https://understat.com/league/EPL |

## Seasons

```
[5]:
```

```
seasons = understat.read_seasons()
seasons.head()
```

```
[5]:
```

|  |  | league\_id | season\_id | url |
| --- | --- | --- | --- | --- |
| league | season |  |  |  |
| ENG-Premier League | 1516 | 1 | 2015 | https://understat.com/league/EPL/2015 |

## Schedule

```
[6]:
```

```
schedule = understat.read_schedule()
schedule.head()
```

```
[6]:
```

|  |  |  | league\_id | season\_id | game\_id | date | home\_team\_id | away\_team\_id | home\_team | away\_team | away\_team\_code | home\_team\_code | home\_goals | away\_goals | home\_xg | away\_xg | is\_result | has\_data | url |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 1516 | 2015-08-08 Bournemouth-Aston Villa | 1 | 2015 | 82 | 2015-08-08 18:00:00 | 73 | 71 | Bournemouth | Aston Villa | AVL | BOU | 0 | 1 | 0.876106 | 0.782253 | True | True | https://understat.com/match/82 |
| 2015-08-08 Chelsea-Swansea | 1 | 2015 | 86 | 2015-08-08 20:30:00 | 80 | 84 | Chelsea | Swansea | SWA | CHE | 2 | 2 | 0.64396 | 2.59203 | True | True | https://understat.com/match/86 |
| 2015-08-08 Everton-Watford | 1 | 2015 | 83 | 2015-08-08 18:00:00 | 72 | 90 | Everton | Watford | WAT | EVE | 2 | 2 | 0.604226 | 0.557892 | True | True | https://understat.com/match/83 |
| 2015-08-08 Leicester-Sunderland | 1 | 2015 | 84 | 2015-08-08 18:00:00 | 75 | 77 | Leicester | Sunderland | SUN | LEI | 4 | 2 | 2.56803 | 1.45946 | True | True | https://understat.com/match/84 |
| 2015-08-08 Manchester United-Tottenham | 1 | 2015 | 81 | 2015-08-08 15:45:00 | 89 | 82 | Manchester United | Tottenham | TOT | MUN | 1 | 0 | 0.627539 | 0.6746 | True | True | https://understat.com/match/81 |

## Team match stats

```
[7]:
```

```
team_match_stats = understat.read_team_match_stats()
team_match_stats.head()
```

```
[7]:
```

|  |  |  | league\_id | season\_id | game\_id | date | home\_team\_id | away\_team\_id | home\_team | away\_team | away\_team\_code | home\_team\_code | ... | away\_ppda | away\_deep\_completions | home\_points | home\_expected\_points | home\_goals | home\_xg | home\_np\_xg | home\_np\_xg\_difference | home\_ppda | home\_deep\_completions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 1516 | 2015-08-08 Bournemouth-Aston Villa | 1 | 2015 | 82 | 2015-08-08 18:00:00 | 73 | 71 | Bournemouth | Aston Villa | AVL | BOU | ... | 11.846154 | 2 | 0 | 1.3912 | 0 | 0.876106 | 0.876106 | 0.093853 | 6.9 | 11 |
| 2015-08-08 Chelsea-Swansea | 1 | 2015 | 86 | 2015-08-08 20:30:00 | 80 | 84 | Chelsea | Swansea | SWA | CHE | ... | 8.833333 | 5 | 1 | 0.1836 | 2 | 0.64396 | 0.64396 | -1.1869 | 10.363636 | 10 |
| 2015-08-08 Everton-Watford | 1 | 2015 | 83 | 2015-08-08 18:00:00 | 72 | 90 | Everton | Watford | WAT | EVE | ... | 17.157895 | 4 | 1 | 1.3301 | 2 | 0.604226 | 0.604226 | 0.046334 | 6.65 | 5 |
| 2015-08-08 Leicester-Sunderland | 1 | 2015 | 84 | 2015-08-08 18:00:00 | 75 | 77 | Leicester | Sunderland | SUN | LEI | ... | 9.555556 | 6 | 3 | 2.1323 | 4 | 2.56803 | 1.80686 | 0.3474 | 10.88 | 5 |
| 2015-08-08 Manchester United-Tottenham | 1 | 2015 | 81 | 2015-08-08 15:45:00 | 89 | 82 | Manchester United | Tottenham | TOT | MUN | ... | 8.21875 | 10 | 3 | 1.2482 | 1 | 0.627539 | 0.627539 | -0.047061 | 13.826087 | 4 |

5 rows × 26 columns

## Player season stats

```
[8]:
```

```
player_season_stats = understat.read_player_season_stats()
player_season_stats.head()
```

```
[8]:
```

|  |  |  | league\_id | season\_id | team | team\_id | player\_id | position | matches | minutes | goals | xg | np\_goals | np\_xg | assists | xa | shots | key\_passes | yellow\_cards | red\_cards | xg\_chain | xg\_buildup |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | player |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 1516 | Aaron Cresswell | 1 | 2015 | West Ham | 81 | 534 | D M | 37 | 3319 | 2 | 1.092563 | 2 | 1.092563 | 4 | 3.294618 | 28 | 40 | 1 | 0 | 10.339367 | 6.831139 |
| Aaron Lennon | 1 | 2015 | Everton | 72 | 593 | F M S | 25 | 1534 | 5 | 2.226095 | 5 | 2.226095 | 0 | 1.697951 | 18 | 23 | 1 | 0 | 5.535392 | 1.90374 |
| Aaron Ramsey | 1 | 2015 | Arsenal | 83 | 504 | M S | 31 | 2624 | 5 | 8.614323 | 5 | 8.614323 | 4 | 4.046242 | 69 | 37 | 4 | 0 | 23.282566 | 14.176444 |
| Abdul Rahman Baba | 1 | 2015 | Chelsea | 80 | 684 | D S | 15 | 1018 | 0 | 0.379115 | 0 | 0.379115 | 1 | 0.179241 | 6 | 3 | 1 | 0 | 3.869669 | 3.490554 |
| Adam Bogdan | 1 | 2015 | Liverpool | 87 | 698 | GK | 2 | 180 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0 | 0 | 0 | 0.120216 | 0.120216 |

## Player match stats

```
[9]:
```

```
player_match_stats = understat.read_player_match_stats()
player_match_stats.head()
```

```
[9]:
```

|  |  |  |  |  | league\_id | season\_id | game\_id | team\_id | player\_id | position | position\_id | minutes | goals | own\_goals | shots | xg | xa | xg\_chain | xg\_buildup |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game | team | player |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 1516 | 2015-08-08 Bournemouth-Aston Villa | Aston Villa | Ashley Westwood | 1 | 2015 | 82 | 71 | 669 | MC | 9 | 90 | 0 | 0 | 0 | 0.0 | 0.374082 | 0.131937 | 0.131937 |
| Brad Guzan | 1 | 2015 | 82 | 71 | 662 | GK | 1 | 90 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Carlos Sánchez | 1 | 2015 | 82 | 71 | 667 | Sub | 17 | 18 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Ciaran Clark | 1 | 2015 | 82 | 71 | 875 | DC | 3 | 90 | 0 | 0 | 0 | 0.0 | 0.0 | 0.131937 | 0.131937 |
| Gabriel Agbonlahor | 1 | 2015 | 82 | 71 | 890 | FW | 15 | 90 | 0 | 0 | 2 | 0.13016 | 0.113668 | 0.243828 | 0.0 |

## Shot events

```
[10]:
```

```
shot_events = understat.read_shot_events()
shot_events.head()
```

```
[10]:
```

|  |  |  |  |  | league\_id | season\_id | game\_id | date | shot\_id | team\_id | player\_id | assist\_player\_id | assist\_player | xg | location\_x | location\_y | minute | body\_part | situation | result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game | team | player |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 1516 | 2015-08-08 Bournemouth-Aston Villa | Aston Villa | Gabriel Agbonlahor | 1 | 2015 | 82 | 2015-08-08 18:00:00 | 487146 | 71 | 890 | <NA> | <NA> | 0.075484 | 0.86 | 0.503 | 67 | Left Foot | Open Play | Blocked Shot |
| Gabriel Agbonlahor | 1 | 2015 | 82 | 2015-08-08 18:00:00 | 487150 | 71 | 890 | 548651 | Micah Richards | 0.054676 | 0.795 | 0.507 | 81 | Left Foot | Open Play | Saved Shot |
| Idrissa Gueye | 1 | 2015 | 82 | 2015-08-08 18:00:00 | 487136 | 71 | 668 | 548653 | Jordan Veretout | 0.018269 | 0.742 | 0.598 | 26 | Right Foot | Open Play | Missed Shot |
| Idrissa Gueye | 1 | 2015 | 82 | 2015-08-08 18:00:00 | 487144 | 71 | 668 | 548657 | Gabriel Agbonlahor | 0.113668 | 0.883 | 0.561 | 47 | Left Foot | Open Play | Saved Shot |
| Leandro Bacuna | 1 | 2015 | 82 | 2015-08-08 18:00:00 | 487141 | 71 | 674 | <NA> | <NA> | 0.097371 | 0.786 | 0.437 | 42 | Right Foot | Direct Freekick | Blocked Shot |