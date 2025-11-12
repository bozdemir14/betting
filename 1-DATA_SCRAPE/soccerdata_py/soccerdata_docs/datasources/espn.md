---
title: "ESPN"
---

This page was generated from
[doc/datasources/ESPN.ipynb](https://github.com/probberechts/soccerdata/blob/1.8.7/doc/datasources/ESPN.ipynb).  
You can [download the notebook](ESPN.ipynb),

```
[2]:
```

```
import soccerdata as sd
```

# ESPN

```
[3]:
```

```
espn = sd.ESPN(leagues="ENG-Premier League", seasons=2021)
print(espn.__doc__)
```

```
/cw/dtaijupiter/NoCsBack/dtai/pieterr/Projects/soccerdata/soccerdata/_common.py:466: UserWarning: Season id "2021" is ambiguous: interpreting as "20-21"
  warnings.warn(msg)
```

```
Provides pd.DataFrames from JSON api available at http://site.api.espn.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/ESPN``.

    Parameters
    ----------
    leagues : string or iterable, optional
        IDs of leagues to include.

    seasons : string, int or list, optional
        Seasons to include. Supports multiple formats.
        Examples: '16-17'; 2016; '2016-17'; [14, 15, 16]
    proxy : 'tor' or or dict or list(dict) or callable, optional
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

## Game schedule

```
[4]:
```

```
epl_schedule = espn.read_schedule()
epl_schedule.head()
```

```
[4]:
```

|  |  |  | date | home\_team | away\_team | game\_id | league\_id |
| --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game |  |  |  |  |  |
| ENG-Premier League | 2021 | 2019-08-09 Liverpool-Norwich City | 2019-08-09 19:00:00+00:00 | Liverpool | Norwich City | 541844 | eng.1 |
| 2019-08-10 AFC Bournemouth-Sheffield United | 2019-08-10 14:00:00+00:00 | AFC Bournemouth | Sheffield United | 541840 | eng.1 |
| 2019-08-10 Burnley-Southampton | 2019-08-10 14:00:00+00:00 | Burnley | Southampton | 541841 | eng.1 |
| 2019-08-10 Crystal Palace-Everton | 2019-08-10 14:00:00+00:00 | Crystal Palace | Everton | 541839 | eng.1 |
| 2019-08-10 Tottenham Hotspur-Aston Villa | 2019-08-10 16:30:00+00:00 | Tottenham Hotspur | Aston Villa | 541837 | eng.1 |

## Match sheet data

```
[5]:
```

```
matchsheet = espn.read_matchsheet(match_id=541465)
matchsheet.head()
```

```
[5]:
```

|  |  |  |  | is\_home | venue | attendance | capacity | roster | fouls\_committed | yellow\_cards | red\_cards | offsides | won\_corners | saves | possession\_pct | total\_shots | shots\_on\_target |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game | team |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | 2020-07-26 West Ham United-Aston Villa | Aston Villa | False | None | 0 | None | [{'active': True, 'starter': True, 'jersey': '... | 16 | 2 | 0 | 0 | 0 | 3 | 63 | 10 | 1 |
| West Ham United | True | None | 0 | None | [{'active': True, 'starter': True, 'jersey': '... | 13 | 1 | 0 | 1 | 7 | 0 | 37 | 13 | 4 |

## Line ups

```
[6]:
```

```
lineups = espn.read_lineup(match_id=541465)
lineups.head()
```

```
[6]:
```

|  |  |  |  |  | is\_home | position | formation\_place | sub\_in | sub\_out | appearances | fouls\_committed | fouls\_suffered | own\_goals | red\_cards | sub\_ins | yellow\_cards | goal\_assists | shots\_on\_target | total\_goals | total\_shots | goals\_conceded | saves | shots\_faced | offsides |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game | team | player |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | 2020-07-26 West Ham United-Aston Villa | Aston Villa | Anwar El Ghazi | False | Substitute | 0 | 90 | end | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | NaN | 0.0 | 0.0 |
| Conor Hourihane | False | Center Left Midfielder | 10 | start | 76 | 1.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | NaN | 0.0 | 0.0 |
| Douglas Luiz | False | Defensive Midfielder | 4 | start | end | 1.0 | 2.0 | 2.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | NaN | 0.0 | 0.0 |
| Ezri Konsa | False | Center Right Defender | 5 | start | end | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | NaN | 0.0 | 0.0 |
| Frédéric Guilbert | False | Right Back | 2 | start | 76 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | NaN | 0.0 | 0.0 |