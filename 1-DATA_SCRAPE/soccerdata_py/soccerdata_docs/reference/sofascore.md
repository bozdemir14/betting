---
title: "Sofascore"
---

# Sofascore

*class* soccerdata.Sofascore(*leagues=None*, *seasons=None*, *proxy=None*, *no\_cache=False*, *no\_store=False*, *data\_dir=PosixPath('/home/docs/soccerdata/data/Sofascore')*)
:   Provides pd.DataFrames from data available at <http://www.sofascore.com>.

    Data will be downloaded as necessary and cached locally in
    `~/soccerdata/data/Sofascore`.

    Parameters:
    :   * **leagues** (*string* *or* *iterable**,* *optional*) – IDs of Leagues to include.
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

    read\_leagues()
    :   Retrieve the selected leagues from the datasource.

        Return type:
        :   pd.DataFrame

    read\_seasons()
    :   Retrieve the selected seasons for the selected leagues.

        Return type:
        :   pd.DataFrame

    read\_league\_table(*force\_cache=False*)
    :   Retrieve the league table for the selected leagues.

        Parameters:
        :   **force\_cache** (*bool*) – By default no cached data is used for the current season.
            If True, will force the use of cached data anyway.

        Return type:
        :   pd.DataFrame

    read\_schedule(*force\_cache=False*)
    :   Retrieve the game schedule for the selected leagues and seasons.

        Parameters:
        :   **force\_cache** (*bool*) – By default no cached data is used for the current season.
            If True, will force the use of cached data anyway.

        Return type:
        :   pd.DataFrame