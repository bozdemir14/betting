---
title: "SoFIFA"
---

This page was generated from
[doc/datasources/SoFIFA.ipynb](https://github.com/probberechts/soccerdata/blob/1.8.7/doc/datasources/SoFIFA.ipynb).  
You can [download the notebook](SoFIFA.ipynb),

```
[3]:
```

```
import soccerdata as sd
```

# SoFIFA

```
[4]:
```

```
sofifa = sd.SoFIFA(leagues="ENG-Premier League", versions="latest")
print(sofifa.__doc__)
```

```
Provides pd.DataFrames from data at http://sofifa.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/SoFIFA``.

    Parameters
    ----------
    leagues : string or iterable, optional
        IDs of leagues to include.
    versions : string, int or list of int, optional
        FIFA releases to include. Should be specified by their ID used in the URL
        (e.g., 230034). Alternatively, the string "all" can be used to include all
        versions and "latest" to include the latest version only. Defaults to
        "latest".
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

## EA Sports FIFA team ratings

```
[5]:
```

```
team_ratings = sofifa.read_team_ratings()
team_ratings.head()
```

```
[5]:
```

|  |  | overall | attack | midfield | defence | transfer\_budget | players | fifa\_edition | update |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| league | team |  |  |  |  |  |  |  |  |
| ENG-Premier League | AFC Bournemouth | 74 | 75 | 73 | 73 | €0 | 29 | FIFA 23 | May 26, 2023 |
| Arsenal | 82 | 82 | 84 | 81 | €0 | 32 | FIFA 23 | May 26, 2023 |
| Aston Villa | 79 | 79 | 77 | 79 | €0 | 32 | FIFA 23 | May 26, 2023 |
| Brentford | 75 | 74 | 75 | 76 | €0 | 31 | FIFA 23 | May 26, 2023 |
| Brighton & Hove Albion | 77 | 75 | 77 | 78 | €0 | 28 | FIFA 23 | May 26, 2023 |

## EA Sports FIFA player ratings

```
[6]:
```

```
player_ratings = sofifa.read_player_ratings(team="Arsenal")
player_ratings.head()
```

```
[6]:
```

|  | fifa\_edition | update | overallrating | potential | crossing | finishing | headingaccuracy | shortpassing | volleys | dribbling | curve | fk\_accuracy | longpassing | ballcontrol | acceleration | sprintspeed | agility | reactions | balance | shotpower | jumping | stamina | strength | longshots | aggression | interceptions | positioning | vision | penalties | composure | defensiveawareness | standingtackle | slidingtackle | gk\_diving | gk\_handling | gk\_kicking | gk\_positioning | gk\_reflexes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| player |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Aaron Ramsdale | FIFA 23 | May 26, 2023 | 83 | 86 | 15 | 14 | 15 | 56 | 16 | 18 | 17 | 16 | 57 | 36 | 47 | 50 | 53 | 82 | 49 | 65 | 66 | 35 | 59 | 15 | 35 | 24 | 18 | 65 | 25 | 65 | 20 | 16 | 15 | 84 | 79 | 87 | 79 | 86 |
| Ainsley Maitland-Niles | FIFA 23 | May 26, 2023 | 73 | 75 | 67 | 58 | 54 | 74 | 44 | 71 | 64 | 50 | 66 | 73 | 79 | 77 | 79 | 70 | 69 | 67 | 66 | 69 | 67 | 62 | 65 | 70 | 69 | 67 | 69 | 70 | 66 | 74 | 72 | 15 | 9 | 7 | 10 | 13 |
| Albert-Mboyo Sambi Lokonga | FIFA 23 | May 26, 2023 | 75 | 82 | 68 | 53 | 61 | 79 | 58 | 78 | 71 | 68 | 77 | 81 | 63 | 69 | 78 | 72 | 68 | 68 | 71 | 77 | 63 | 63 | 72 | 77 | 65 | 75 | 41 | 80 | 64 | 73 | 68 | 14 | 7 | 6 | 13 | 9 |
| Amario Cozier-Duberry | FIFA 23 | May 26, 2023 | 59 | 77 | 58 | 57 | 38 | 55 | 60 | 60 | 53 | 41 | 44 | 58 | 72 | 69 | 73 | 50 | 68 | 56 | 44 | 55 | 45 | 45 | 55 | 27 | 59 | 56 | 55 | 55 | 28 | 28 | 24 | 11 | 12 | 9 | 13 | 7 |
| Arthur Okonkwo | FIFA 23 | May 26, 2023 | 66 | 75 | 10 | 6 | 12 | 33 | 7 | 9 | 12 | 20 | 20 | 17 | 44 | 44 | 40 | 63 | 31 | 47 | 50 | 29 | 50 | 7 | 20 | 11 | 6 | 35 | 19 | 30 | 13 | 13 | 12 | 64 | 65 | 63 | 67 | 66 |

```
[7]:
```

```
sofifa.read_teams()
```

```
[7]:
```

|  | team | league | fifa\_edition | update |
| --- | --- | --- | --- | --- |
| team\_id |  |  |  |  |
| 10 | Manchester City | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 9 | Liverpool | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 1 | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 5 | Chelsea | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 11 | Manchester United | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 18 | Tottenham Hotspur | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 13 | Newcastle United | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 2 | Aston Villa | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 19 | West Ham United | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 95 | Leicester City | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 110 | Wolverhampton Wanderers | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 14 | Nottingham Forest | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 1808 | Brighton & Hove Albion | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 7 | Everton | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 1799 | Crystal Palace | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 144 | Fulham | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 8 | Leeds United | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 17 | Southampton | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 1925 | Brentford | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 1943 | AFC Bournemouth | ENG-Premier League | FIFA 23 | May 26, 2023 |

```
[8]:
```

```
sofifa.read_players(team="Arsenal")
```

```
[8]:
```

|  | player | team | league | fifa\_edition | update |
| --- | --- | --- | --- | --- | --- |
| player\_id |  |  |  |  |  |
| 233934 | Aaron Ramsdale | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 231936 | Benjamin White | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 243715 | William Saliba | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 232580 | Gabriel dos S. Magalhães | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 227813 | Oleksandr Zinchenko | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 205498 | Luiz Frello Filho Jorge | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 222665 | Martin Ødegaard | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 199503 | Granit Xhaka | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 246669 | Bukayo Saka | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 230666 | Gabriel Fernando de Jesus | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 251566 | Gabriel Teodoro Martinelli Silva | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 207421 | Leandro Trossard | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 236988 | Eddie Nketiah | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 209989 | Thomas Partey | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 256958 | Fábio Daniel Ferreira Vieira | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 226491 | Kieran Tierney | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 265693 | Jakub Kiwior | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 233267 | Matt Turner | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 228295 | Rob Holding | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 240273 | Emile Smith Rowe | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 231448 | Reiss Nelson | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 211454 | Mohamed Elneny | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 232938 | Takehiro Tomiyasu | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 247731 | Matthew Smith | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 248732 | Karl Hein | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 259403 | Joel Ideho | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 260141 | Cătălin Cîrjan | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 259095 | George Lewis | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 271743 | Amario Cozier-Duberry | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 271808 | Lino Sousa | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 259097 | Salah-Eddine Oulad M'Hand | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 274387 | Reuell Walters | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 270390 | Marcus Vincius Oliveira Alencar | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 260653 | Brooke Norton-Cuffy | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 260144 | Charlie Patino | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 251530 | Nuno Albertino Varela Tavares | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 247463 | Folarin Balogun | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 246671 | Arthur Okonkwo | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 241928 | Albert Sambi Lokonga | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 235755 | Auston Trusty | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 226110 | Nicolas Pépé | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 225782 | Ainsley Maitland-Niles | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 222562 | Rúnar Alex Rúnarsson | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 206654 | Pablo Marí Villar | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |
| 201118 | Cédric Ricardo Alves Soares | Arsenal | ENG-Premier League | FIFA 23 | May 26, 2023 |