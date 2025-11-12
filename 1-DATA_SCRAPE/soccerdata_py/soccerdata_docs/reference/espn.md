---
title: "ESPN"
---

# ESPN

*class* soccerdata.ESPN(*leagues=None*, *seasons=None*, *proxy=None*, *no\_cache=False*, *no\_store=False*, *data\_dir=PosixPath('/home/docs/soccerdata/data/ESPN')*)
:   Provides pd.DataFrames from JSON api available at <http://site.api.espn.com>.

    Data will be downloaded as necessary and cached locally in
    `~/soccerdata/data/ESPN`.

    Parameters:
    :   * **leagues** (*string* *or* *iterable**,* *optional*) – IDs of leagues to include.
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

    *property* seasons*: list[str]*
    :   Return a list of selected seasons.

    read\_schedule(*force\_cache=False*)
    :   Retrieve the game schedule for the selected leagues and seasons.

        Parameters:
        :   **force\_cache** (*bool*) – By default no cached data is used for the current season.
            If True, will force the use of cached data anyway.

        Return type:
        :   pd.DataFrame

    read\_matchsheet(*match\_id=None*)
    :   Retrieve match sheets for the selected leagues and seasons.

        Parameters:
        :   **match\_id** (*int* *or* *list* *of* *int**,* *optional*) – Retrieve the match sheet for a specific game.

        Raises:
        :   **ValueError** – If no games with the given IDs were found for the selected seasons and leagues.

        Return type:
        :   pd.DataFrame.

    read\_lineup(*match\_id=None*)
    :   Retrieve lineups for the selected leagues and seasons.

        Parameters:
        :   **match\_id** (*int* *or* *list* *of* *int**,* *optional*) – Retrieve the lineup for a specific game.

        Raises:
        :   **ValueError** – If no games with the given IDs were found for the selected seasons and leagues.

        Return type:
        :   pd.DataFrame.

    *classmethod* available\_leagues()
    :   Return a list of league IDs available for this source.

        Return type:
        :   list[str]

    get(*url*, *filepath=None*, *max\_age=None*, *no\_cache=False*, *var=None*)
    :   Load data from url.

        By default, the source of url is downloaded and saved to filepath.
        If filepath exists, the url is not visited and the cached data is
        returned.

        Parameters:
        :   * **url** (*str*) – URL to download.
            * **filepath** (*Path**,* *optional*) – Path to save downloaded file. If None, downloaded data is not cached.
            * **max\_age** (*int for age in days**, or* *timedelta object*) – The max. age of locally cached file before re-download.
            * **no\_cache** (*bool*) – If True, will not use cached data. Overrides the class property.
            * **var** (*str* *or* *list* *of* *str**,* *optional*) – Return a JavaScript variable instead of the page source.

        Raises:
        :   **TypeError** – If max\_age is not an integer or timedelta object.

        Returns:
        :   File-like object of downloaded data.

        Return type:
        :   io.BufferedIOBase

    *property* leagues*: list[str]*
    :   Return a list of selected leagues.