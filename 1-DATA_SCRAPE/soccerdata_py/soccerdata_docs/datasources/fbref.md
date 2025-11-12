---
title: "FBref"
---

This page was generated from
[doc/datasources/FBref.ipynb](https://github.com/probberechts/soccerdata/blob/1.8.7/doc/datasources/FBref.ipynb).  
You can [download the notebook](FBref.ipynb),

```
[3]:
```

```
import soccerdata as sd
```

# FBref

```
[4]:
```

```
fbref = sd.FBref(leagues="ENG-Premier League", seasons=2021)
print(fbref.__doc__)
```

```
Provides pd.DataFrames from data at http://fbref.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/FBref``.

    Parameters
    ----------
    leagues : string or iterable, optional
        IDs of leagues to include. For efficiently reading data from the Top-5
        European leagues, use "Big 5 European Leagues Combined".
    seasons : string, int or list, optional
        Seasons to include. Supports multiple formats.
        Examples: '16-17'; 2016; '2016-17'; [14, 15, 16]
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

```
/cw/dtaijupiter/NoCsBack/dtai/pieterr/Projects/soccerdata/soccerdata/_common.py:471: UserWarning: Season id "2021" is ambiguous: interpreting as "20-21"
  warnings.warn(msg, stacklevel=1)
```

## Team season stats

```
[5]:
```

```
team_season_stats = fbref.read_team_season_stats(stat_type="passing")
team_season_stats.head()
```

```
[5]:
```

|  |  |  | players\_used | 90s | Total | | | | | Short | | | Medium | | | Long | | | Ast | xAG | xA | A-xAG | KP | 1/3 | PPA | CrsPA | PrgP | url |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | Cmp | Att | Cmp% | TotDist | PrgDist | Cmp | Att | Cmp% | Cmp | Att | Cmp% | Cmp | Att | Cmp% |  |  |  |  |  |  |  |  |  |  |
| league | season | team |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | Arsenal | 29 | 38 | 18041 | 21807 | 82.7 | 306094 | 93540 | 8319 | 9236 | 90.1 | 7770 | 8814 | 88.2 | 1453 | 2621 | 55.4 | 38 | 35.1 | 35.3 | 2.9 | 332 | 1377 | 325 | 67 | 1760 | /en/squads/18bb7c10/2020-2021/Arsenal-Stats |
| Aston Villa | 24 | 38 | 12938 | 16996 | 76.1 | 235927 | 93009 | 5729 | 6654 | 86.1 | 5222 | 6209 | 84.1 | 1571 | 3074 | 51.1 | 38 | 37.4 | 31.4 | 0.6 | 403 | 1086 | 323 | 76 | 1420 | /en/squads/8602292d/2020-2021/Aston-Villa-Stats |
| Brighton | 27 | 38 | 15772 | 19871 | 79.4 | 283213 | 95248 | 6694 | 7654 | 87.5 | 6893 | 7960 | 86.6 | 1689 | 3090 | 54.7 | 24 | 33.2 | 34.9 | -9.2 | 358 | 1132 | 358 | 80 | 1516 | /en/squads/d07537b9/2020-2021/Brighton-and-Hov... |
| Burnley | 25 | 38 | 10825 | 15562 | 69.6 | 196816 | 82192 | 5117 | 6058 | 84.5 | 3688 | 4824 | 76.5 | 1553 | 3535 | 43.9 | 20 | 27.7 | 26.9 | -7.7 | 267 | 923 | 292 | 80 | 1012 | /en/squads/943e8050/2020-2021/Burnley-Stats |
| Chelsea | 27 | 38 | 21969 | 25799 | 85.2 | 360450 | 112392 | 10454 | 11454 | 91.3 | 8965 | 9976 | 89.9 | 1667 | 2703 | 61.7 | 38 | 41.5 | 37.1 | -3.5 | 448 | 1441 | 377 | 70 | 1798 | /en/squads/cff3d9bb/2020-2021/Chelsea-Stats |

## Team match stats

```
[6]:
```

```
team_match_stats = fbref.read_team_match_stats(stat_type="schedule", team="Manchester City")
team_match_stats.head()
```

```
[6]:
```

|  |  |  |  | date | time | round | day | venue | result | GF | GA | opponent | xG | xGA | Poss | Attendance | Captain | Formation | Referee | match\_report | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | team | game |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | Manchester City | 2020-09-21 Wolves-Manchester City | 2020-09-21 | 20:15:00 | Matchweek 2 | Mon | Away | W | 3 | 1 | Wolves | 1.9 | 0.6 | 65 | <NA> | Fernandinho | 4-2-3-1 | Andre Marriner | /en/matches/1c17eca3/Wolverhampton-Wanderers-M... | <NA> |
| 2020-09-27 Manchester City-Leicester City | 2020-09-27 | 16:30:00 | Matchweek 3 | Sun | Home | L | 2 | 5 | Leicester City | 0.9 | 2.9 | 72 | <NA> | Fernandinho | 4-2-3-1 | Michael Oliver | /en/matches/31c2a061/Manchester-City-Leicester... | <NA> |
| 2020-10-03 Leeds United-Manchester City | 2020-10-03 | 17:30:00 | Matchweek 4 | Sat | Away | D | 1 | 1 | Leeds United | 1.2 | 2.4 | 49 | <NA> | Kevin De Bruyne | 4-3-3 | Mike Dean | /en/matches/5ce15b58/Leeds-United-Manchester-C... | <NA> |
| 2020-10-17 Manchester City-Arsenal | 2020-10-17 | 17:30:00 | Matchweek 5 | Sat | Home | W | 1 | 0 | Arsenal | 1.3 | 0.9 | 58 | <NA> | Raheem Sterling | 3-1-4-2 | Chris Kavanagh | /en/matches/e95b8546/Manchester-City-Arsenal-O... | <NA> |
| 2020-10-24 West Ham-Manchester City | 2020-10-24 | 12:30:00 | Matchweek 6 | Sat | Away | D | 1 | 1 | West Ham | 1.0 | 0.3 | 69 | <NA> | Raheem Sterling | 4-3-3 | Anthony Taylor | /en/matches/2b0c0eca/West-Ham-United-Mancheste... | <NA> |

## Player season stats

```
[7]:
```

```
player_season_stats = fbref.read_player_season_stats(stat_type="standard")
player_season_stats.head()
```

```
[7]:
```

|  |  |  |  | nation | pos | age | born | Playing Time | | | | Performance | | | | | | | | Expected | | | | Progression | | | Per 90 Minutes | | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  | MP | Starts | Min | 90s | Gls | Ast | G+A | G-PK | PK | PKatt | CrdY | CrdR | xG | npxG | xAG | npxG+xAG | PrgC | PrgP | PrgR | Gls | Ast | G+A | G-PK | G+A-PK | xG | xAG | xG+xAG | npxG | npxG+xAG |
| league | season | team | player |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | Arsenal | Ainsley Maitland-Niles | ENG | MF,DF | 22 | 1997 | 11 | 5 | 490 | 5.4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.1 | 0.1 | 0.1 | 0.2 | 12 | 24 | 21 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.01 | 0.02 | 0.04 | 0.01 | 0.04 |
| Alexandre Lacazette | FRA | FW | 29 | 1991 | 31 | 22 | 1923 | 21.4 | 13 | 2 | 15 | 10 | 3 | 3 | 3 | 0 | 11.7 | 9.3 | 2.2 | 11.5 | 15 | 55 | 112 | 0.61 | 0.09 | 0.7 | 0.47 | 0.56 | 0.55 | 0.1 | 0.65 | 0.43 | 0.54 |
| Bernd Leno | GER | GK | 28 | 1992 | 35 | 35 | 3131 | 34.8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.0 | 0.0 | 0.0 | 0.0 | 0 | 2 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Bukayo Saka | ENG | FW,MF | 18 | 2001 | 32 | 30 | 2553 | 28.4 | 5 | 3 | 8 | 5 | 0 | 0 | 1 | 0 | 6.9 | 6.9 | 4.4 | 11.3 | 85 | 101 | 269 | 0.18 | 0.11 | 0.28 | 0.18 | 0.28 | 0.24 | 0.16 | 0.4 | 0.24 | 0.4 |
| Calum Chambers | ENG | DF | 25 | 1995 | 10 | 8 | 753 | 8.4 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.4 | 1.1 | 1.5 | 16 | 40 | 49 | 0.0 | 0.24 | 0.24 | 0.0 | 0.24 | 0.05 | 0.13 | 0.18 | 0.05 | 0.18 |

## Player match stats

```
[8]:
```

```
player_match_stats = fbref.read_player_match_stats(stat_type="passing", match_id="db261cb0")
player_match_stats.head()
```

```
[8]:
```

|  |  |  |  |  | jersey\_number | nation | pos | age | min | Total | | | | | Short | | | Medium | | | Long | | | Ast | xAG | xA | KP | 1/3 | PPA | CrsPA | PrgP | game\_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  | Cmp | Att | Cmp% | TotDist | PrgDist | Cmp | Att | Cmp% | Cmp | Att | Cmp% | Cmp | Att | Cmp% |  |  |  |  |  |  |  |  |  |
| league | season | game | team | player |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | 2020-09-12 Crystal Palace-Southampton | Crystal Palace | Andros Townsend | 10 | ENG | RM | 29-058 | 90 | 13 | 30 | 43.3 | 184 | 68 | 8 | 11 | 72.7 | 4 | 8 | 50.0 | 1 | 6 | 16.7 | 1 | 0.6 | 0.2 | 2 | 0 | 1 | 0 | 1 | db261cb0 |
| Cheikhou Kouyaté | 8 | SEN | CB | 30-266 | 90 | 11 | 19 | 57.9 | 207 | 109 | 3 | 4 | 75.0 | 3 | 6 | 50.0 | 3 | 6 | 50.0 | 0 | 0.0 | 0.0 | 0 | 1 | 0 | 0 | 2 | db261cb0 |
| Eberechi Eze | 25 | ENG | LM | 22-075 | 10 | 8 | 10 | 80.0 | 177 | 46 | 2 | 2 | 100.0 | 3 | 3 | 100.0 | 2 | 3 | 66.7 | 0 | 0.0 | 0.0 | 0 | 1 | 0 | 0 | 2 | db261cb0 |
| James McArthur | 18 | SCO | CM | 32-341 | 90 | 15 | 32 | 46.9 | 322 | 159 | 2 | 6 | 33.3 | 11 | 15 | 73.3 | 1 | 7 | 14.3 | 0 | 0.4 | 0.0 | 1 | 2 | 0 | 0 | 3 | db261cb0 |
| James McCarthy | 22 | IRL | CM | 29-305 | 73 | 14 | 23 | 60.9 | 281 | 75 | 4 | 6 | 66.7 | 6 | 10 | 60.0 | 3 | 5 | 60.0 | 0 | 0.0 | 0.1 | 0 | 0 | 0 | 0 | 2 | db261cb0 |

## Game schedule

```
[9]:
```

```
epl_schedule = fbref.read_schedule()
epl_schedule.head()
```

```
[9]:
```

|  |  |  | week | day | date | time | home\_team | home\_xg | score | away\_xg | away\_team | attendance | venue | referee | match\_report | notes | game\_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | 2020-09-12 Crystal Palace-Southampton | 1 | Sat | 2020-09-12 | 15:00 | Crystal Palace | 1.1 | 1–0 | 0.9 | Southampton | <NA> | Selhurst Park | Jonathan Moss | /en/matches/db261cb0/Crystal-Palace-Southampto... | <NA> | db261cb0 |
| 2020-09-12 Fulham-Arsenal | 1 | Sat | 2020-09-12 | 12:30 | Fulham | 0.1 | 0–3 | 1.9 | Arsenal | <NA> | Craven Cottage | Chris Kavanagh | /en/matches/bf52349b/Fulham-Arsenal-September-... | <NA> | bf52349b |
| 2020-09-12 Liverpool-Leeds United | 1 | Sat | 2020-09-12 | 17:30 | Liverpool | 2.7 | 4–3 | 0.3 | Leeds United | <NA> | Anfield | Michael Oliver | /en/matches/21b58926/Liverpool-Leeds-United-Se... | <NA> | 21b58926 |
| 2020-09-12 West Ham-Newcastle Utd | 1 | Sat | 2020-09-12 | 20:00 | West Ham | 1.0 | 0–2 | 1.6 | Newcastle Utd | <NA> | London Stadium | Stuart Attwell | /en/matches/78495ced/West-Ham-United-Newcastle... | <NA> | 78495ced |
| 2020-09-13 Tottenham-Everton | 1 | Sun | 2020-09-13 | 16:30 | Tottenham | 1.1 | 0–1 | 1.2 | Everton | <NA> | Tottenham Hotspur Stadium | Martin Atkinson | /en/matches/fc7f9aa1/Tottenham-Hotspur-Everton... | <NA> | fc7f9aa1 |

## Line ups

```
[10]:
```

```
lineups = fbref.read_lineup(match_id="db261cb0")
lineups.head()
```

```
[10]:
```

|  |  |  | jersey\_number | player | team | is\_starter | position | minutes\_played |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game |  |  |  |  |  |  |
| ENG-Premier League | 2021 | 2020-09-12 Crystal Palace-Southampton | 31 | Vicente Guaita | Crystal Palace | True | GK | 90 |
| 2020-09-12 Crystal Palace-Southampton | 2 | Joel Ward | Crystal Palace | True | RB | 90 |
| 2020-09-12 Crystal Palace-Southampton | 6 | Scott Dann | Crystal Palace | True | CB | 90 |
| 2020-09-12 Crystal Palace-Southampton | 8 | Cheikhou Kouyaté | Crystal Palace | True | CB | 90 |
| 2020-09-12 Crystal Palace-Southampton | 9 | Jordan Ayew | Crystal Palace | True | FW | 90 |

## Events

```
[11]:
```

```
events = fbref.read_events(match_id="db261cb0")
events.head()
```

```
[11]:
```

|  |  |  | team | minute | score | player1 | player2 | event\_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game |  |  |  |  |  |  |
| ENG-Premier League | 2021 | 2020-09-12 Crystal Palace-Southampton | Crystal Palace | 13 | 1:0 | Wilfried Zaha | Andros Townsend | goal |
| 2020-09-12 Crystal Palace-Southampton | Crystal Palace | 41 | 1:0 | Jeffrey Schlupp | None | yellow\_card |
| 2020-09-12 Crystal Palace-Southampton | Southampton | 46 | 1:0 | Jannik Vestergaard | Jan Bednarek | substitute\_in |
| 2020-09-12 Crystal Palace-Southampton | Southampton | 51 | 1:0 | Kyle Walker-Peters | None | yellow\_card |
| 2020-09-12 Crystal Palace-Southampton | Crystal Palace | 58 | 1:0 | James McCarthy | None | yellow\_card |

## Shot events

```
[12]:
```

```
shots = fbref.read_shot_events(match_id="db261cb0")
shots.head()
```

```
[12]:
```

|  |  |  | minute | player | team | xG | PSxG | outcome | distance | body\_part | notes | SCA 1 | | SCA 2 | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  | player | event | player | event |
| league | season | game |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | 2020-09-12 Crystal Palace-Southampton | 4 | Jack Stephens | Southampton | 0.07 | 0.09 | Saved | 10 | Head | <NA> | James Ward-Prowse | Pass (Dead) | Kyle Walker-Peters | Pass (Dead) |
| 2020-09-12 Crystal Palace-Southampton | 13 | Wilfried Zaha | Crystal Palace | 0.44 | 0.73 | Goal | 9 | Right Foot | Volley | Andros Townsend | Pass (Live) | James McCarthy | Interception |
| 2020-09-12 Crystal Palace-Southampton | 32 | Danny Ings | Southampton | 0.04 | 0.12 | Saved | 10 | Head | <NA> | Kyle Walker-Peters | Pass (Live) | William Smallbone | Pass (Live) |
| 2020-09-12 Crystal Palace-Southampton | 36 | Cheikhou Kouyaté | Crystal Palace | 0.15 | 0.09 | Saved | 11 | Right Foot | <NA> | Andros Townsend | Pass (Dead) | Wilfried Zaha | Fouled |
| 2020-09-12 Crystal Palace-Southampton | 46 | Nathan Redmond | Southampton | 0.07 | 0.03 | Saved | 14 | Right Foot | <NA> | Che Adams | Pass (Live) | Danny Ings | Pass (Live) |