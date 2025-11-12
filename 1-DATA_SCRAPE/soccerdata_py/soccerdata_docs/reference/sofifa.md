---
title: "SoFIFA"
---

# SoFIFA

*class* soccerdata.SoFIFA(*leagues=None*, *versions='latest'*, *proxy=None*, *no\_cache=False*, *no\_store=False*, *data\_dir=PosixPath('/home/docs/soccerdata/data/SoFIFA')*)
:   Provides pd.DataFrames from data at <http://sofifa.com>.

    Data will be downloaded as necessary and cached locally in
    `~/soccerdata/data/SoFIFA`.

    Parameters:
    :   * **leagues** (*string* *or* *iterable**,* *optional*) – IDs of leagues to include.
        * **versions** (*string**,* *int* *or* *list* *of* *int**,* *optional*) – FIFA releases to include. Should be specified by their ID used in the URL
          (e.g., 230034). Alternatively, the string “all” can be used to include all
          versions and “latest” to include the latest version only. Defaults to
          “latest”.
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

    read\_leagues()
    :   Retrieve selected leagues from the datasource.

        Return type:
        :   pd.DataFrame

    read\_versions(*max\_age=1*)
    :   Retrieve available FIFA releases and rating updates.

        Parameters:
        :   **max\_age** (*int for age in days**, or* *timedelta object*) – The max. age of the locally cached release history before a new
            version is downloaded.

        Raises:
        :   **TypeError** – If max\_age is not an integer or timedelta object.

        Return type:
        :   pd.DataFrame

    read\_teams()
    :   Retrieve all teams for the selected leagues.

        Return type:
        :   pd.DataFrame

    read\_players(*team=None*)
    :   Retrieve all players for the selected leagues.

        Parameters:
        :   **team** (*str* *or* *list* *of* *str**,* *optional*) – Team(s) to retrieve. If None, will retrieve all teams.

        Raises:
        :   **ValueError** – If no data is found for the given team(s) in the selected leagues.

        Return type:
        :   pd.DataFrame

    *classmethod* available\_leagues()
    :   Return a list of league IDs available for this source.

        Return type:
        :   list[str]

    read\_team\_ratings()
    :   Retrieve ratings for all teams in the selected leagues.

        Return type:
        :   pd.DataFrame

    read\_player\_ratings(*team=None*, *player=None*)
    :   Retrieve ratings for players.

        Parameters:
        :   * **team** (*str* *or* *list* *of* *str**,* *optional*) – Team(s) to retrieve. If None, will retrieve all teams.
            * **player** (*int* *or* *list* *of* *int**,* *optional*) – Player(s) to retrieve. If None, will retrieve all players.

        Return type:
        :   pd.DataFrame