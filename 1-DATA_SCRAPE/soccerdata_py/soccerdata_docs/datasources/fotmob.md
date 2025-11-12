---
title: "FotMob"
---

This page was generated from
[doc/datasources/FotMob.ipynb](https://github.com/probberechts/soccerdata/blob/1.8.7/doc/datasources/FotMob.ipynb).  
You can [download the notebook](FotMob.ipynb),

```
[1]:
```

```
import pandas as pd

pd.set_option("display.max_columns", None)
```

```
[3]:
```

```
import soccerdata as sd
```

# FotMob

```
[4]:
```

```
fotmob = sd.FotMob(leagues="ESP-La Liga", seasons="2022/2023")
print(fotmob.__doc__)
```

```
Provides pd.DataFrames from data available at http://www.fotmob.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/FotMob``.

    Parameters
    ----------
    leagues : string or iterable, optional
        IDs of Leagues to include.
    seasons : string, int or list, optional
        Seasons to include. Supports multiple formats.
        Examples: '16-17'; 2016; '2016-17'; [14, 15, 16]
    proxy : 'tor' or dict or list(dict) or callable, optional
        Use a proxy to hide your IP address. Valid options are:
            - 'tor': Uses the Tor network. Tor should be running in
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

## Read league table

```
[5]:
```

```
league_table = fotmob.read_league_table()
league_table.head()
```

```
[5]:
```

|  |  | team | MP | W | D | L | GF | GA | GD | Pts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season |  |  |  |  |  |  |  |  |  |
| ESP-La Liga | 2223 | Barcelona | 38 | 28 | 4 | 6 | 70 | 20 | 50 | 88 |
| 2223 | Real Madrid | 38 | 24 | 6 | 8 | 75 | 36 | 39 | 78 |
| 2223 | Atletico Madrid | 38 | 23 | 8 | 7 | 70 | 33 | 37 | 77 |
| 2223 | Real Sociedad | 38 | 21 | 8 | 9 | 51 | 35 | 16 | 71 |
| 2223 | Villarreal | 38 | 19 | 7 | 12 | 59 | 40 | 19 | 64 |

## Read schedule

```
[6]:
```

```
schedule = fotmob.read_schedule()
schedule.head()
```

```
[6]:
```

|  |  |  | round | week | date | home\_team | away\_team | home\_score | away\_score | status | game\_id | url |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game |  |  |  |  |  |  |  |  |  |  |
| ESP-La Liga | 2223 | 2022-08-12 Osasuna-Sevilla | None | None | 2022-08-12 19:00:00+00:00 | Osasuna | Sevilla | 2 | 1 | FT | 3918013 | https://fotmob.com/matches/sevilla-vs-osasuna/... |
| 2022-08-13 Barcelona-Rayo Vallecano | None | None | 2022-08-13 19:00:00+00:00 | Barcelona | Rayo Vallecano | 0 | 0 | FT | 3918009 | https://fotmob.com/matches/rayo-vallecano-vs-b... |
| 2022-08-13 Celta Vigo-Espanyol | None | None | 2022-08-13 15:00:00+00:00 | Celta Vigo | Espanyol | 2 | 2 | FT | 3918011 | https://fotmob.com/matches/espanyol-vs-celta-v... |
| 2022-08-13 Real Valladolid-Villarreal | None | None | 2022-08-13 17:00:00+00:00 | Real Valladolid | Villarreal | 0 | 3 | FT | 3918016 | https://fotmob.com/matches/villarreal-vs-real-... |
| 2022-08-14 Almeria-Real Madrid | None | None | 2022-08-14 20:00:00+00:00 | Almeria | Real Madrid | 1 | 2 | FT | 3918014 | https://fotmob.com/matches/real-madrid-vs-alme... |

## Read team match stats

```
[7]:
```

```
match_stats = fotmob.read_team_match_stats(opponent_stats=False, team="Valencia")
match_stats.head()
```

```
[7]:
```

|  |  |  |  | Accurate passes | Ball possession | Big chances | Big chances missed | Corners | Expected goals (xG) | Fouls committed | Shots on target | Total shots | Accurate passes (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game | team |  |  |  |  |  |  |  |  |  |  |
| ESP-La Liga | 2223 | 2022-08-14 Valencia-Girona | Valencia | 285 | 46 | 2 | 1 | 4 | 1.62 | 18 | 2 | 17 | 0.81 |
| 2022-08-21 Athletic Club-Valencia | Valencia | 432 | 63 | 1 | 1 | 3 | 0.73 | 15 | 0 | 10 | 0.85 |
| 2022-08-29 Valencia-Atletico Madrid | Valencia | 513 | 70 | 0 | 0 | 6 | 0.51 | 15 | 2 | 12 | 0.88 |
| 2022-09-04 Valencia-Getafe | Valencia | 482 | 70 | 4 | 1 | 9 | 2.30 | 11 | 9 | 24 | 0.88 |
| 2022-09-10 Rayo Vallecano-Valencia | Valencia | 266 | 54 | 3 | 2 | 7 | 1.80 | 11 | 4 | 17 | 0.77 |