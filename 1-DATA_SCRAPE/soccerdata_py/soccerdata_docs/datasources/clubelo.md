---
title: "ClubElo"
---

This page was generated from
[doc/datasources/ClubElo.ipynb](https://github.com/probberechts/soccerdata/blob/1.8.7/doc/datasources/ClubElo.ipynb).  
You can [download the notebook](ClubElo.ipynb),

```
[2]:
```

```
import soccerdata as sd
```

# ClubElo

```
[3]:
```

```
elo = sd.ClubElo()
print(elo.__doc__)
```

```
Provides pd.DataFrames from CSV API at http://api.clubelo.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/ClubElo``.

    Since the source does not provide league names, this class will not filter
    by league. League names will be inserted from the other sources where
    available. Leagues that are only covered by clubelo.com will have NaN
    values.

    Parameters
    ----------
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

## ELO scores for all teams at specified date

```
[4]:
```

```
current_elo = elo.read_by_date()
current_elo.head()
```

```
[4]:
```

|  | rank | country | level | elo | from | to | league |
| --- | --- | --- | --- | --- | --- | --- | --- |
| team |  |  |  |  |  |  |  |
| Liverpool | 1.0 | ENG | 1 | 2047.083862 | 2022-04-20 | 2022-04-24 | ENG-Premier League |
| Man City | 2.0 | ENG | 1 | 2037.059937 | 2022-04-21 | 2022-04-23 | ENG-Premier League |
| Bayern | 3.0 | GER | 1 | 1984.775391 | 2022-04-18 | 2022-04-23 | GER-Bundesliga |
| Real Madrid | 4.0 | ESP | 1 | 1969.584351 | 2022-04-21 | 2022-04-26 | ESP-La Liga |
| Chelsea | 5.0 | ENG | 1 | 1921.101440 | 2022-04-21 | 2022-04-24 | ENG-Premier League |

## Full ELO history for one club

```
[5]:
```

```
barca_elo = elo.read_team_history("Barcelona")
barca_elo.head()
```

```
[5]:
```

|  | rank | team | country | level | elo | to |
| --- | --- | --- | --- | --- | --- | --- |
| from |  |  |  |  |  |  |
| 1939-10-22 | NaN | Barcelona | ESP | 1 | 1636.704590 | 1939-12-03 |
| 1939-12-04 | NaN | Barcelona | ESP | 1 | 1626.102173 | 1939-12-10 |
| 1939-12-11 | NaN | Barcelona | ESP | 1 | 1636.728271 | 1939-12-17 |
| 1939-12-18 | NaN | Barcelona | ESP | 1 | 1646.951660 | 1939-12-24 |
| 1939-12-25 | NaN | Barcelona | ESP | 1 | 1637.424316 | 1939-12-31 |