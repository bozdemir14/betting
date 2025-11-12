---
title: "Sofascore"
---

This page was generated from
[doc/datasources/Sofascore.ipynb](https://github.com/probberechts/soccerdata/blob/1.8.7/doc/datasources/Sofascore.ipynb).  
You can [download the notebook](Sofascore.ipynb),

```
[1]:
```

```
import pandas as pd

pd.set_option("display.max_columns", None)
```

```
[2]:
```

```
%env SOCCERDATA_LOGLEVEL=ERROR
%env SOCCERDATA_NOCACHE=True
%env SOCCERDATA_NOSTORE=True
```

```
env: SOCCERDATA_LOGLEVEL=ERROR
env: SOCCERDATA_NOCACHE=True
env: SOCCERDATA_NOSTORE=True
```

```
[3]:
```

```
import soccerdata as sd
```

# Sofascore

```
[4]:
```

```
sofascore = sd.Sofascore(leagues="ESP-La Liga", seasons="2022/2023")
print(sofascore.__doc__)
```

```
Provides pd.DataFrames from data available at http://www.sofascore.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/Sofascore``.

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
league_table = sofascore.read_league_table()
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
| 2223 | Atlético Madrid | 38 | 23 | 8 | 7 | 70 | 33 | 37 | 77 |
| 2223 | Real Sociedad | 38 | 21 | 8 | 9 | 51 | 35 | 16 | 71 |
| 2223 | Villarreal | 38 | 19 | 7 | 12 | 59 | 40 | 19 | 64 |

## Read schedule

```
[8]:
```

```
schedule = sofascore.read_schedule()
schedule.head()
```

```
[8]:
```

|  |  |  | round | week | date | home\_team | away\_team | home\_score | away\_score | game\_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game |  |  |  |  |  |  |  |  |
| ESP-La Liga | 2223 | 2022-08-12 Osasuna-Sevilla | None | 1 | 2022-08-12 15:00:00 | Osasuna | Sevilla | 2 | 1 | 10408559 |
| 2022-08-13 Barcelona-Rayo Vallecano | None | 1 | 2022-08-13 15:00:00 | Barcelona | Rayo Vallecano | 0 | 0 | 10408557 |
| 2022-08-13 Celta Vigo-Espanyol | None | 1 | 2022-08-13 11:00:00 | Celta Vigo | Espanyol | 2 | 2 | 10408645 |
| 2022-08-13 Real Valladolid-Villarreal | None | 1 | 2022-08-13 13:00:00 | Real Valladolid | Villarreal | 0 | 3 | 10408563 |
| 2022-08-14 Almería-Real Madrid | None | 1 | 2022-08-14 16:00:00 | Almería | Real Madrid | 1 | 2 | 10408712 |

```
[ ]:
```

```

```