---
title: "WhoScored"
---

This page was generated from
[doc/datasources/WhoScored.ipynb](https://github.com/probberechts/soccerdata/blob/1.8.7/doc/datasources/WhoScored.ipynb).  
You can [download the notebook](WhoScored.ipynb),

```
[3]:
```

```
import soccerdata as sd
```

# WhoScored

```
[4]:
```

```
ws = sd.WhoScored(leagues="ENG-Premier League", seasons=2021)
print(ws.__doc__)
```

```
/cw/dtaijupiter/NoCsBack/dtai/pieterr/Projects/soccerdata/soccerdata/_common.py:493: UserWarning: Season id "2021" is ambiguous: interpreting as "20-21"
  warnings.warn(msg, stacklevel=1)
```

```
Provides pd.DataFrames from data available at http://whoscored.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/WhoScored``.

    Parameters
    ----------
    leagues : string or iterable, optional
        IDs of Leagues to include.
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
    path_to_browser : Path, optional
        Path to the Chrome executable.
    headless : bool, default: True
        If True, will run Chrome in headless mode. Setting this to False might
        help to avoid getting blocked. Only supported for Selenium <4.13.
```

## Game schedule

```
[5]:
```

```
epl_schedule = ws.read_schedule()
epl_schedule.head()
```

```
[5]:
```

|  |  |  | stage\_id | game\_id | status | start\_time | home\_team\_id | home\_team | home\_yellow\_cards | home\_red\_cards | away\_team\_id | away\_team | away\_yellow\_cards | away\_red\_cards | has\_incidents\_summary | has\_preview | score\_changed\_at | elapsed | last\_scorer | is\_top\_match | home\_team\_country\_code | away\_team\_country\_code | comment\_count | is\_lineup\_confirmed | is\_stream\_available | match\_is\_opta | home\_team\_country\_name | away\_team\_country\_name | date | home\_score | away\_score | incidents | bets | aggregate\_winner\_field | winner\_field | period | extra\_result\_field | home\_extratime\_score | away\_extratime\_score | home\_penalty\_score | away\_penalty\_score | started\_at\_utc | first\_half\_ended\_at\_utc | second\_half\_started\_at\_utc | stage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | 2020-09-12 Crystal Palace-Southampton | 18685 | 1485186 | 6 | 2020-09-12T15:00:00 | 162 | Crystal Palace | 2 | 0 | 18 | Southampton | 1 | 0 | True | True | 2020-09-12 15:14:31Z | FT | 0.0 | False | gb-eng | gb-eng | 6 | True | False | False | England | England | 2020-09-12 14:00:00+00:00 | 1 | 0 | [{'minute': '13', 'type': 1, 'subType': 1, 'pl... | None | None | 0.0 | 7 | None | None | None | None | None | 2020-09-12T14:01:42Z | None | 2020-09-12T15:04:01Z | None |
| 2020-09-12 Fulham-Arsenal | 18685 | 1485187 | 6 | 2020-09-12T12:30:00 | 170 | Fulham | 2 | 0 | 13 | Arsenal | 2 | 0 | True | True | 2020-09-12 13:48:13Z | FT | 1.0 | True | gb-eng | gb-eng | 15 | True | False | False | England | England | 2020-09-12 11:30:00+00:00 | 0 | 3 | [{'minute': '8', 'type': 1, 'subType': 1, 'pla... | None | None | 1.0 | 7 | None | None | None | None | None | 2020-09-12T11:32:23Z | None | 2020-09-12T12:35:50Z | None |
| 2020-09-12 Liverpool-Leeds United | 18685 | 1485188 | 6 | 2020-09-12T17:30:00 | 26 | Liverpool | 1 | 0 | 19 | Leeds United | 0 | 0 | True | True | 2020-09-12 19:15:39Z | FT | 0.0 | True | gb-eng | gb-eng | 61 | True | False | False | England | England | 2020-09-12 16:30:00+00:00 | 4 | 3 | [{'minute': '4', 'type': 1, 'subType': 2, 'pla... | None | None | 0.0 | 7 | None | None | None | None | None | 2020-09-12T16:30:21Z | None | 2020-09-12T17:32:57Z | None |
| 2020-09-12 West Ham United-Newcastle | 18685 | 1485191 | 6 | 2020-09-12T20:00:00 | 29 | West Ham United | 2 | 0 | 23 | Newcastle | 2 | 0 | True | True | 2020-09-12 21:45:39Z | FT | 1.0 | False | gb-eng | gb-eng | 10 | True | False | False | England | England | 2020-09-12 19:00:00+00:00 | 0 | 2 | [{'minute': '56', 'type': 1, 'subType': 1, 'pl... | None | None | 1.0 | 7 | None | None | None | None | None | 2020-09-12T19:00:32Z | None | 2020-09-12T20:03:20Z | None |
| 2020-09-13 Tottenham-Everton | 18685 | 1485189 | 6 | 2020-09-13T16:30:00 | 30 | Tottenham | 1 | 0 | 31 | Everton | 0 | 0 | True | True | 2020-09-13 17:41:16Z | FT | 1.0 | True | gb-eng | gb-eng | 32 | True | False | False | England | England | 2020-09-13 15:30:00+00:00 | 0 | 1 | [{'minute': '55', 'type': 1, 'subType': 1, 'pl... | None | None | 1.0 | 7 | None | None | None | None | None | 2020-09-13T15:30:20Z | None | 2020-09-13T16:31:33Z | None |

## Injured and suspended players

```
[6]:
```

```
missing_players = ws.read_missing_players(match_id=1485184)
missing_players.head()
```

```
[6]:
```

|  |  |  |  |  | game\_id | player\_id | reason | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game | team | player |  |  |  |  |
| ENG-Premier League | 2021 | 2021-01-12 Burnley-Manchester United | Burnley | Charlie Taylor | 1485184 | 107462 | injured doubtful | Doubtful |
| Dwight McNeil | 1485184 | 357427 | injured doubtful | Doubtful |
| Jay Rodriguez | 1485184 | 33891 | injured doubtful | Doubtful |
| Jimmy Dunne | 1485184 | 366743 | injured doubtful | Doubtful |
| Manchester United | Eric Bailly | 1485184 | 243814 | injured doubtful | Doubtful |

## Match event stream data

```
[7]:
```

```
events = ws.read_events(match_id=1485184)
events.head()
```

```
[7]:
```

|  |  |  |  | game\_id | period | minute | second | expanded\_minute | type | outcome\_type | team\_id | team | player\_id | player | x | y | end\_x | end\_y | goal\_mouth\_y | goal\_mouth\_z | blocked\_x | blocked\_y | qualifiers | is\_touch | is\_shot | is\_goal | card\_type | related\_event\_id | related\_player\_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game | id |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | 2021-01-12 Burnley-Manchester United | 2253458317 | 1485184 | PreMatch | 0 | 0.0 | 0 | FormationSet | Successful | 184 | Burnley | NaN | NaN | 0.0 | 0.0 | NaN | NaN | NaN | NaN | NaN | NaN | [{'type': {'displayName': 'TeamPlayerFormation... | False | NaN | NaN | NaN | NaN | NaN |
| 2253458375 | 1485184 | PreMatch | 0 | 0.0 | 0 | FormationSet | Successful | 32 | Man Utd | NaN | NaN | 0.0 | 0.0 | NaN | NaN | NaN | NaN | NaN | NaN | [{'type': {'displayName': 'CaptainPlayerId', '... | False | NaN | NaN | NaN | NaN | NaN |
| 2253487469 | 1485184 | FirstHalf | 0 | 0.0 | 0 | Start | Successful | 184 | Burnley | NaN | NaN | 0.0 | 0.0 | NaN | NaN | NaN | NaN | NaN | NaN | [] | False | NaN | NaN | NaN | NaN | NaN |
| 2253487473 | 1485184 | FirstHalf | 0 | 0.0 | 0 | Start | Successful | 32 | Man Utd | NaN | NaN | 0.0 | 0.0 | NaN | NaN | NaN | NaN | NaN | NaN | [] | False | NaN | NaN | NaN | NaN | NaN |
| 2253487625 | 1485184 | FirstHalf | 0 | 0.0 | 0 | Pass | Successful | 184 | Burnley | 79050.0 | Ashley Westwood | 50.3 | 50.3 | 30.5 | 50.3 | NaN | NaN | NaN | NaN | [{'type': {'displayName': 'Angle', 'value': 21... | True | NaN | NaN | NaN | NaN | NaN |

Match event stream data can be returned in various formats, which can be selected with the “output\_fmt” parameter.

* `events` (default): Returns a dataframe with all events.
* `raw`: Returns the original unformatted WhoScored JSON.
* `spadl`: Returns a dataframe with the [SPADL representation](https://socceraction.readthedocs.io/en/latest/documentation/SPADL.html#spadl) of the original events.
* `atomic-spadl`: Returns a dataframe with the [Atomic-SPADL representation](https://socceraction.readthedocs.io/en/latest/documentation/SPADL.html#atomic-spadl) of the original events.
* `loader`: Returns a `socceration.data.opta.OptaLoader` instance

```
[8]:
```

```
events = ws.read_events(match_id=1485184, output_fmt="raw")

import json  # noqa

print(json.dumps(events[1485184][0], indent=2))
```

```
{
  "eventId": 2,
  "expandedMinute": 0,
  "id": 2253487473,
  "isTouch": false,
  "minute": 0,
  "outcomeType": {
    "displayName": "Successful",
    "value": 1
  },
  "period": {
    "displayName": "FirstHalf",
    "value": 1
  },
  "qualifiers": [],
  "satisfiedEventsTypes": [],
  "second": 0,
  "teamId": 32,
  "type": {
    "displayName": "Start",
    "value": 32
  },
  "x": 0,
  "y": 0
}
```

```
[9]:
```

```
actions = ws.read_events(match_id=1485184, output_fmt="spadl")
actions.head()
```

```
/cw/dtaijupiter/NoCsBack/dtai/pieterr/Projects/soccerdata/.venv/lib/python3.11/site-packages/socceraction/spadl/opta.py:219: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  ).bfill()
```

```
[9]:
```

|  | game\_id | original\_event\_id | period\_id | time\_seconds | team\_id | player\_id | start\_x | end\_x | start\_y | end\_y | type\_id | result\_id | bodypart\_id | action\_id | player | team |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1485184 | 2253487625 | 1 | 0.0 | 184 | 79050.0 | 52.815 | 32.025 | 34.204 | 34.204 | 0 | 1 | 0 | 0 | Ashley Westwood | Burnley |
| 1 | 1485184 | 2253487639 | 1 | 2.0 | 184 | 131464.0 | 31.080 | 38.220 | 36.312 | 15.844 | 0 | 1 | 0 | 1 | James Tarkowski | Burnley |
| 2 | 1485184 | NaN | 1 | 4.5 | 184 | 80067.0 | 38.220 | 43.365 | 15.844 | 12.512 | 21 | 1 | 0 | 2 | Matthew Lowton | Burnley |
| 3 | 1485184 | 2253487685 | 1 | 7.0 | 184 | 80067.0 | 43.365 | 90.300 | 12.512 | 49.708 | 0 | 1 | 0 | 3 | Matthew Lowton | Burnley |
| 4 | 1485184 | 2253487689 | 1 | 11.0 | 184 | 93473.0 | 90.300 | 105.000 | 49.708 | 38.828 | 11 | 0 | 4 | 4 | Robbie Brady | Burnley |

```
[10]:
```

```
atomic_actions = ws.read_events(match_id=1485184, output_fmt="atomic-spadl")
atomic_actions.head()
```

```
/cw/dtaijupiter/NoCsBack/dtai/pieterr/Projects/soccerdata/.venv/lib/python3.11/site-packages/socceraction/spadl/opta.py:219: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  ).bfill()
```

```
[10]:
```

|  | game\_id | original\_event\_id | action\_id | period\_id | time\_seconds | team\_id | player\_id | x | y | dx | dy | type\_id | bodypart\_id | player | team |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1485184 | 2253487625 | 0 | 1 | 0.00 | 184 | 79050.0 | 52.815 | 34.204 | -20.790 | 0.000 | 0 | 0 | Ashley Westwood | Burnley |
| 1 | 1485184 | 2253487625 | 1 | 1 | 1.00 | 184 | 131464.0 | 32.025 | 34.204 | 0.000 | 0.000 | 23 | 0 | James Tarkowski | Burnley |
| 2 | 1485184 | 2253487639 | 2 | 1 | 2.00 | 184 | 131464.0 | 31.080 | 36.312 | 7.140 | -20.468 | 0 | 0 | James Tarkowski | Burnley |
| 3 | 1485184 | 2253487639 | 3 | 1 | 3.25 | 184 | 80067.0 | 38.220 | 15.844 | 0.000 | 0.000 | 23 | 0 | Matthew Lowton | Burnley |
| 4 | 1485184 | NaN | 4 | 1 | 4.50 | 184 | 80067.0 | 38.220 | 15.844 | 5.145 | -3.332 | 21 | 0 | Matthew Lowton | Burnley |

```
[11]:
```

```
# Scrape all games and return a socceration.data.opta.OptaLoader
loader = ws.read_events(output_fmt="loader")

# Now use this loader to load the data
print("Games:")
df_games = loader.games(competition_id="ENG-Premier League", season_id="2021")
display(df_games.head())

print("Teams:")
df_teams = loader.teams(game_id=1485184)
display(df_teams.head())

print("Players:")
df_players = loader.players(game_id=1485184)
display(df_players.head())

print("Events:")
df_events = loader.events(game_id=1485184)
display(df_events.head())

# You can use the socceraction package to convert the events
# to SPADL and to compute xT or VAEP action values
```

```
Games:
```

|  | game\_id | season\_id | competition\_id | game\_day | game\_date | home\_team\_id | away\_team\_id | home\_score | away\_score | duration | referee | venue | attendance | home\_manager | away\_manager |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1485494 | 2021 | ENG-Premier League | None | 2021-04-04 12:00:00 | 18 | 184 | 3 | 2 | 98 | Andre Marriner | St. Mary's Stadium | 0 | Ralph Hasenhüttl | Sean Dyche |
| 1 | 1485300 | 2021 | ENG-Premier League | None | 2020-12-16 20:00:00 | 170 | 211 | 0 | 0 | 95 | Robert Jones | Craven Cottage | 0 | Scott Parker | Graham Potter |
| 2 | 1485264 | 2021 | ENG-Premier League | None | 2020-12-06 19:15:00 | 26 | 161 | 4 | 0 | 97 | Craig Pawson | Anfield | 2000 | Jürgen Klopp | Nuno Espírito Santo |
| 3 | 1485519 | 2021 | ENG-Premier League | None | 2021-05-16 16:30:00 | 175 | 26 | 1 | 2 | 102 | Mike Dean | The Hawthorns | 0 | Sam Allardyce | Jürgen Klopp |
| 4 | 1485436 | 2021 | ENG-Premier League | None | 2021-03-19 20:00:00 | 170 | 19 | 1 | 2 | 100 | David Coote | Craven Cottage | 0 | Scott Parker | Marcelo Bielsa |

```
Teams:
```

|  | team\_id | team\_name |
| --- | --- | --- |
| 0 | 184 | Burnley |
| 1 | 32 | Man Utd |

```
Players:
```

|  | game\_id | team\_id | player\_id | player\_name | is\_starter | minutes\_played | jersey\_number | starting\_position |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1485184 | 184 | 105720 | Nick Pope | True | 102 | 1 | GK |
| 1 | 1485184 | 184 | 80067 | Matthew Lowton | True | 102 | 2 | DR |
| 2 | 1485184 | 184 | 94935 | Ben Mee | True | 102 | 6 | DC |
| 3 | 1485184 | 184 | 131464 | James Tarkowski | True | 102 | 5 | DC |
| 4 | 1485184 | 184 | 24148 | Erik Pieters | True | 102 | 23 | DL |

```
Events:
```

|  | game\_id | event\_id | period\_id | team\_id | player\_id | type\_id | timestamp | minute | second | outcome | start\_x | start\_y | end\_x | end\_y | qualifiers | related\_player\_id | touch | goal | shot | type\_name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1485184 | 2253487473 | 1 | 32 | NaN | 32 | 2021-01-12 20:15:00 | 0 | 0 | True | 0.0 | 0.0 | 0.0 | 0.0 | {} | NaN | False | False | False | start |
| 1 | 1485184 | 2253487469 | 1 | 184 | NaN | 32 | 2021-01-12 20:15:00 | 0 | 0 | True | 0.0 | 0.0 | 0.0 | 0.0 | {} | NaN | False | False | False | start |
| 2 | 1485184 | 2253487625 | 1 | 184 | 79050.0 | 1 | 2021-01-12 20:15:00 | 0 | 0 | True | 50.3 | 50.3 | 30.5 | 50.3 | {213: '3.1', 178: True, 141: '50.3', 212: '20.... | NaN | True | False | False | pass |
| 3 | 1485184 | 2253487639 | 1 | 184 | 131464.0 | 1 | 2021-01-12 20:15:02 | 0 | 2 | True | 29.6 | 53.4 | 36.4 | 23.3 | {178: True, 213: '5.0', 212: '21.7', 141: '23.... | NaN | True | False | False | pass |
| 4 | 1485184 | 2253487685 | 1 | 184 | 80067.0 | 1 | 2021-01-12 20:15:07 | 0 | 7 | True | 41.3 | 18.4 | 86.0 | 73.1 | {1: True, 213: '0.7', 56: 'Center', 178: True,... | NaN | True | False | False | pass |

```
[ ]:
```

```

```