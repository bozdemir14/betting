---
title: "Match History"
---

This page was generated from
[doc/datasources/MatchHistory.ipynb](https://github.com/probberechts/soccerdata/blob/1.8.7/doc/datasources/MatchHistory.ipynb).  
You can [download the notebook](MatchHistory.ipynb),

```
[3]:
```

```
import soccerdata as sd
```

# Match History

```
[4]:
```

```
mh = sd.MatchHistory(leagues="ENG-Premier League", seasons=2021)
print(mh.__doc__)
```

```
/cw/dtaijupiter/NoCsBack/dtai/pieterr/Projects/soccerdata/soccerdata/_common.py:466: UserWarning: Season id "2021" is ambiguous: interpreting as "20-21"
  warnings.warn(msg)
```

```
Provides pd.DataFrames from CSV files available at http://www.football-data.co.uk/data.php.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/MatchHistory``.

    Parameters
    ----------
    leagues : string or iterable
        IDs of leagues to include.
    seasons : string, int or list
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
    data_dir : Path, optional
        Path to directory where data will be cached.
```

## Historic match results and betting odds

```
[5]:
```

```
hist = mh.read_games()
hist.head()
```

```
[5]:
```

|  |  |  | date | home\_team | away\_team | FTHG | FTAG | FTR | HTHG | HTAG | HTR | referee | HS | AS | HST | AST | HF | AF | HC | AC | HY | AY | HR | AR | B365H | B365D | B365A | BWH | BWD | BWA | IWH | IWD | IWA | PSH | PSD | PSA | WHH | WHD | WHA | VCH | VCD | VCA | MaxH | MaxD | MaxA | AvgH | AvgD | AvgA | B365>2.5 | B365<2.5 | P>2.5 | P<2.5 | Max>2.5 | Max<2.5 | Avg>2.5 | Avg<2.5 | AHh | B365AHH | B365AHA | PAHH | PAHA | MaxAHH | MaxAHA | AvgAHH | AvgAHA | B365CH | B365CD | B365CA | BWCH | BWCD | BWCA | IWCH | IWCD | IWCA | PSCH | PSCD | PSCA | WHCH | WHCD | WHCA | VCCH | VCCD | VCCA | MaxCH | MaxCD | MaxCA | AvgCH | AvgCD | AvgCA | B365C>2.5 | B365C<2.5 | PC>2.5 | PC<2.5 | MaxC>2.5 | MaxC<2.5 | AvgC>2.5 | AvgC<2.5 | AHCh | B365CAHH | B365CAHA | PCAHH | PCAHA | MaxCAHH | MaxCAHA | AvgCAHH | AvgCAHA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | season | game |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ENG-Premier League | 2021 | 2020-01-11 Aston Villa-Southampton | 2020-01-11 12:00:00 | Aston Villa | Southampton | 3 | 4 | A | 0 | 3 | A | D England | 19 | 9 | 10 | 4 | 12 | 17 | 11 | 1 | 1 | 2 | 0 | 0 | 2.45 | 3.5 | 2.80 | 2.35 | 3.60 | 2.85 | 2.50 | 3.35 | 2.75 | 2.53 | 3.72 | 2.81 | 2.50 | 3.5 | 2.75 | 2.40 | 3.60 | 2.80 | 2.60 | 3.84 | 2.85 | 2.46 | 3.60 | 2.78 | 1.66 | 2.2 | 1.66 | 2.37 | 1.69 | 2.38 | 1.65 | 2.27 | 0.00 | 1.83 | 2.07 | 1.87 | 2.07 | 1.87 | 2.09 | 1.83 | 2.05 | 2.60 | 3.50 | 2.62 | 2.50 | 3.60 | 2.70 | 2.55 | 3.50 | 2.70 | 2.69 | 3.56 | 2.73 | 2.60 | 3.50 | 2.62 | 2.50 | 3.60 | 2.70 | 2.70 | 3.70 | 2.80 | 2.57 | 3.55 | 2.69 | 1.66 | 2.20 | 1.70 | 2.29 | 1.71 | 2.37 | 1.66 | 2.24 | 0.00 | 1.93 | 1.97 | 1.95 | 1.98 | 1.97 | 2.04 | 1.89 | 1.98 |
| 2020-01-11 Man United-Arsenal | 2020-01-11 16:30:00 | Man United | Arsenal | 0 | 1 | A | 0 | 0 | D | M Dean | 8 | 7 | 2 | 2 | 12 | 12 | 6 | 3 | 3 | 3 | 0 | 0 | 2.00 | 3.6 | 3.60 | 2.00 | 3.70 | 3.60 | 2.05 | 3.45 | 3.55 | 2.05 | 3.78 | 3.73 | 2.05 | 3.6 | 3.60 | 2.05 | 3.60 | 3.50 | 2.10 | 3.85 | 3.76 | 2.04 | 3.66 | 3.58 | 1.72 | 2.1 | 1.76 | 2.19 | 1.81 | 2.22 | 1.74 | 2.12 | -0.50 | 2.05 | 1.85 | 2.05 | 1.88 | 2.09 | 1.90 | 2.04 | 1.84 | 1.95 | 3.60 | 3.80 | 1.95 | 3.60 | 3.90 | 2.00 | 3.50 | 3.80 | 2.02 | 3.65 | 3.97 | 2.00 | 3.50 | 3.80 | 1.95 | 3.50 | 4.00 | 2.06 | 3.75 | 4.00 | 1.99 | 3.59 | 3.87 | 1.90 | 1.90 | 1.96 | 1.96 | 1.99 | 2.10 | 1.88 | 1.95 | -0.50 | 2.00 | 1.90 | 2.03 | 1.90 | 2.05 | 1.92 | 2.00 | 1.88 |
| 2020-01-11 Newcastle-Everton | 2020-01-11 14:00:00 | Newcastle | Everton | 2 | 1 | H | 0 | 0 | D | S Attwell | 11 | 15 | 4 | 4 | 9 | 10 | 5 | 4 | 2 | 4 | 0 | 0 | 3.70 | 3.4 | 2.05 | 3.75 | 3.40 | 2.05 | 3.55 | 3.30 | 2.10 | 3.82 | 3.56 | 2.09 | 3.70 | 3.4 | 2.05 | 3.50 | 3.50 | 2.05 | 4.00 | 3.59 | 2.15 | 3.71 | 3.47 | 2.06 | 1.80 | 2.0 | 1.86 | 2.07 | 1.88 | 2.08 | 1.82 | 2.01 | 0.25 | 2.05 | 1.75 | 2.15 | 1.80 | 2.17 | 1.83 | 2.12 | 1.77 | 3.30 | 3.30 | 2.25 | 3.30 | 3.30 | 2.25 | 3.15 | 3.35 | 2.30 | 3.34 | 3.43 | 2.33 | 3.40 | 3.25 | 2.25 | 3.30 | 3.30 | 2.25 | 3.62 | 3.50 | 2.34 | 3.34 | 3.33 | 2.27 | 2.00 | 1.80 | 2.12 | 1.81 | 2.14 | 1.92 | 2.04 | 1.80 | 0.25 | 1.95 | 1.95 | 1.93 | 2.00 | 1.99 | 2.03 | 1.93 | 1.95 |
| 2020-01-11 Tottenham-Brighton | 2020-01-11 19:15:00 | Tottenham | Brighton | 2 | 1 | H | 1 | 0 | H | G Scott | 9 | 6 | 3 | 2 | 14 | 13 | 4 | 5 | 2 | 1 | 0 | 0 | 1.61 | 4.0 | 5.50 | 1.62 | 4.25 | 5.00 | 1.65 | 3.90 | 5.00 | 1.65 | 4.26 | 5.54 | 1.63 | 4.0 | 5.25 | 1.62 | 4.20 | 5.25 | 1.67 | 4.30 | 5.75 | 1.63 | 4.17 | 5.29 | 1.66 | 2.2 | 1.68 | 2.32 | 1.71 | 2.35 | 1.65 | 2.26 | -1.00 | 2.02 | 1.77 | 2.15 | 1.80 | 2.16 | 1.84 | 2.09 | 1.80 | 1.55 | 4.33 | 6.00 | 1.57 | 4.25 | 5.50 | 1.60 | 4.20 | 5.75 | 1.61 | 4.36 | 5.77 | 1.57 | 4.00 | 6.00 | 1.57 | 4.20 | 5.75 | 1.63 | 4.45 | 6.39 | 1.59 | 4.29 | 5.62 | 1.66 | 2.20 | 1.68 | 2.32 | 1.72 | 2.37 | 1.65 | 2.27 | -1.00 | 2.06 | 1.84 | 2.11 | 1.84 | 2.13 | 1.99 | 2.02 | 1.86 |
| 2020-02-11 Fulham-West Brom | 2020-02-11 17:30:00 | Fulham | West Brom | 2 | 0 | H | 2 | 0 | H | S Hooper | 13 | 10 | 6 | 1 | 13 | 11 | 5 | 2 | 3 | 2 | 0 | 0 | 2.40 | 3.3 | 3.00 | 2.40 | 3.30 | 3.00 | 2.45 | 3.10 | 3.00 | 2.47 | 3.40 | 3.13 | 2.40 | 3.3 | 3.00 | 2.45 | 3.25 | 3.00 | 2.56 | 3.50 | 3.17 | 2.44 | 3.32 | 3.01 | 2.00 | 1.8 | 2.13 | 1.80 | 2.14 | 1.85 | 2.06 | 1.78 | -0.25 | 2.10 | 1.80 | 2.11 | 1.84 | 2.15 | 1.86 | 2.10 | 1.80 | 2.40 | 3.30 | 3.00 | 2.45 | 3.30 | 2.95 | 2.40 | 3.05 | 3.10 | 2.48 | 3.32 | 3.19 | 2.40 | 3.20 | 3.10 | 2.40 | 3.25 | 3.10 | 2.48 | 3.45 | 3.22 | 2.41 | 3.27 | 3.09 | 2.05 | 1.85 | 2.05 | 1.88 | 2.11 | 1.92 | 2.02 | 1.81 | -0.25 | 2.06 | 1.84 | 2.11 | 1.84 | 2.12 | 1.87 | 2.08 | 1.82 |