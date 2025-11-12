---
title: "FBref"
---

# FBref

*class* soccerdata.FBref(*leagues=None*, *seasons=None*, *proxy=None*, *no\_cache=False*, *no\_store=False*, *data\_dir=PosixPath('/home/docs/soccerdata/data/FBref')*)
:   Provides pd.DataFrames from data at <http://fbref.com>.

    Data will be downloaded as necessary and cached locally in
    `~/soccerdata/data/FBref`.

    Parameters:
    :   * **leagues** (*string* *or* *iterable**,* *optional*) – IDs of leagues to include. For efficiently reading data from the Top-5
          European leagues, use “Big 5 European Leagues Combined”.
        * **seasons** (*string**,* *int* *or* *list**,* *optional*) – Seasons to include. Supports multiple formats.
          Examples: ‘16-17’; 2016; ‘2016-17’; [14, 15, 16]
        * **proxy** (*'tor'* *or* *or dict* *or* *list**(**dict**) or* *callable**,* *optional*) –

          Use a proxy to hide your IP address. Valid options are:
          :   + ”tor”: Uses the Tor network. Tor should be running in
                the background on port 9050.
              + str: The address of the proxy server to use.
              + list(str): A list of proxies to choose from. A different proxy will
                be selected from this list after failed requests, allowing rotating
                proxies.
              + callable: A function that returns a valid proxy. This function will
                be called after failed requests, allowing rotating proxies.
        * **no\_cache** (*bool*) – If True, will not use cached data.
        * **no\_store** (*bool*) – If True, will not store downloaded data.
        * **data\_dir** (*Path*) – Path to directory where data will be cached.

    read\_leagues(*split\_up\_big5=False*)
    :   Retrieve selected leagues from the datasource.

        Parameters:
        :   **split\_up\_big5** (*bool*) – If True, it will load the “Big 5 European Leagues Combined” instead of
            each league individually.

        Return type:
        :   pd.DataFrame

    read\_seasons(*split\_up\_big5=False*)
    :   Retrieve the selected seasons for the selected leagues.

        Parameters:
        :   **split\_up\_big5** (*bool*) – If True, it will load the “Big 5 European Leagues Combined” instead of
            each league individually.

        Return type:
        :   pd.DataFrame

    read\_team\_season\_stats(*stat\_type='standard'*, *opponent\_stats=False*)
    :   Retrieve aggregated season stats for all teams in the selected leagues and seasons.

        The following stat types are available:
        :   * ‘standard’
            * ‘keeper’
            * ‘keeper\_adv’
            * ‘shooting’
            * ‘passing’
            * ‘passing\_types’
            * ‘goal\_shot\_creation’
            * ‘defense’
            * ‘possession’
            * ‘playing\_time’
            * ‘misc’

        Parameters:
        :   * **stat\_type** (*str*) – Type of stats to retrieve.
            * **opponent\_stats** (*bool*) – If True, will retrieve opponent stats.

        Raises:
        :   **ValueError** – If `stat_type` is not valid.

        Return type:
        :   pd.DataFrame

    read\_team\_match\_stats(*stat\_type='schedule'*, *opponent\_stats=False*, *team=None*, *force\_cache=False*)
    :   Retrieve the match logs for all teams in the selected leagues and seasons.

        The following stat types are available:
        :   * ‘schedule’
            * ‘keeper’
            * ‘shooting’
            * ‘passing’
            * ‘passing\_types’
            * ‘goal\_shot\_creation’
            * ‘defense’
            * ‘possession’
            * ‘misc’

        Parameters:
        :   * **stat\_type** (*str*) – Type of stats to retrieve.
            * **opponent\_stats** (*bool*) – If True, will retrieve opponent stats.
            * **team** (*str* *or* *list* *of* *str**,* *optional*) – Team(s) to retrieve. If None, will retrieve all teams.
            * **force\_cache** (*bool*) – By default no cached data is used for the current season.
              If True, will force the use of cached data anyway.

        Raises:
        :   **ValueError** – If `stat_type` is not valid.

        Return type:
        :   pd.DataFrame

    read\_player\_season\_stats(*stat\_type='standard'*)
    :   Retrieve players from the datasource for the selected leagues and seasons.

        The following stat types are available:
        :   * ‘standard’
            * ‘shooting’
            * ‘passing’
            * ‘passing\_types’
            * ‘goal\_shot\_creation’
            * ‘defense’
            * ‘possession’
            * ‘playing\_time’
            * ‘misc’
            * ‘keeper’
            * ‘keeper\_adv’

        Parameters:
        :   **stat\_type** (*str*) – Type of stats to retrieve.

        Raises:
        :   **TypeError** – If `stat_type` is not valid.

        Return type:
        :   pd.DataFrame

    read\_schedule(*force\_cache=False*)
    :   Retrieve the game schedule for the selected leagues and seasons.

        Parameters:
        :   **force\_cache** (*bool*) – By default no cached data is used for the current season.
            If True, will force the use of cached data anyway.

        Return type:
        :   pd.DataFrame

    read\_player\_match\_stats(*stat\_type='summary'*, *match\_id=None*, *force\_cache=False*)
    :   Retrieve the match stats for the selected leagues and seasons.

        The following stat types are available:
        :   * ‘summary’
            * ‘keepers’
            * ‘passing’
            * ‘passing\_types’
            * ‘defense’
            * ‘possession’
            * ‘misc’

        Parameters:
        :   * **stat\_type** (*str*) – Type of stats to retrieve.
            * **match\_id** (*int* *or* *list* *of* *int**,* *optional*) – Retrieve the event stream for a specific game.
            * **force\_cache** (*bool*) – By default no cached data is used to scrape the list of available
              games for the current season. If True, will force the use of
              cached data anyway.

        Raises:
        :   * **ValueError** – If no games with the given IDs were found for the selected seasons and leagues.
            * **TypeError** – If `stat_type` is not valid.

        Return type:
        :   pd.DataFrame

    read\_lineup(*match\_id=None*, *force\_cache=False*)
    :   Retrieve lineups for the selected leagues and seasons.

        Parameters:
        :   * **match\_id** (*int* *or* *list* *of* *int**,* *optional*) – Retrieve the lineup for a specific game.
            * **force\_cache** (*bool*) – By default no cached data is used to scrape the list of available
              games for the current season. If True, will force the use of
              cached data anyway.

        Raises:
        :   **ValueError** – If no games with the given IDs were found for the selected seasons and leagues.

        Return type:
        :   pd.DataFrame.

    read\_events(*match\_id=None*, *force\_cache=False*)
    :   Retrieve match events for the selected seasons or selected matches.

        The data returned includes the timing of goals, cards and substitutions.
        Also includes the players who are involved in the event.

        Parameters:
        :   * **match\_id** (*int* *or* *list* *of* *int**,* *optional*) – Retrieve the events for a specific game.
            * **force\_cache** (*bool*) – By default no cached data is used to scrape the list of available
              games for the current season. If True, will force the use of
              cached data anyway.

        Raises:
        :   **ValueError** – If no games with the given IDs were found for the selected seasons and leagues.

        Return type:
        :   pd.DataFrame.

    read\_shot\_events(*match\_id=None*, *force\_cache=False*)
    :   Retrieve shooting data for the selected seasons or selected matches.

        The data returned includes who took the shot, when, with which body
        part and from how far away. Additionally, the player creating the
        chance and also the creation before this are included in the data.

        Parameters:
        :   * **match\_id** (*int* *or* *list* *of* *int**,* *optional*) – Retrieve the shots for a specific game.
            * **force\_cache** (*bool*) – By default no cached data is used to scrape the list of available
              games for the current season. If True, will force the use of
              cached data anyway.

        Raises:
        :   **ValueError** – If no games with the given IDs were found for the selected seasons and leagues.

        Return type:
        :   pd.DataFrame.

    *classmethod* available\_leagues()
    :   Return a list of league IDs available for this source.

        Return type:
        :   list[str]