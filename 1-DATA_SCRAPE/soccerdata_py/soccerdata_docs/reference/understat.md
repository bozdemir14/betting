---
title: "Understat"
---

# Understat

*class* soccerdata.Understat(*leagues=None*, *seasons=None*, *proxy=None*, *no\_cache=False*, *no\_store=False*, *data\_dir=PosixPath('/home/docs/soccerdata/data/Understat')*)
:   Provides pd.DataFrames from data at <https://understat.com>.

    Data will be downloaded as necessary and cached locally in
    `~/soccerdata/data/Understat`.

    Parameters:
    :   * **proxy** (*'tor'* *or* *or dict* *or* *list**(**dict**) or* *callable**,* *optional*) –

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
        * **leagues** (*str* *|* *list**[**str**]* *|* *None*)
        * **seasons** (*str* *|* *int* *|* *Iterable**[**str* *|* *int**]* *|* *None*)

    *property* seasons*: list[str]*
    :   Return a list of selected seasons.

    read\_leagues()
    :   Retrieve the selected leagues from the datasource.

        Return type:
        :   pd.DataFrame

    read\_seasons()
    :   Retrieve the selected seasons from the datasource.

        Return type:
        :   pd.DataFrame

    read\_schedule(*include\_matches\_without\_data=True*, *force\_cache=False*)
    :   Retrieve the matches for the selected leagues and seasons.

        Parameters:
        :   * **include\_matches\_without\_data** (*bool*) – By default matches with and without data are returned.
              If False, will only return matches with data.
            * **force\_cache** (*bool*) – By default no cached data is used for the current season.
              If True, will force the use of cached data anyway.

        Return type:
        :   pd.DataFrame

    read\_team\_match\_stats(*force\_cache=False*)
    :   Retrieve the team match stats for the selected leagues and seasons.

        Parameters:
        :   **force\_cache** (*bool*) – By default no cached data is used for the current season.
            If True, will force the use of cached data anyway.

        Return type:
        :   pd.DataFrame

    read\_player\_season\_stats(*force\_cache=False*)
    :   Retrieve the player season stats for the selected leagues and seasons.

        Parameters:
        :   **force\_cache** (*bool*) – By default no cached data is used for the current season.
            If True, will force the use of cached data anyway.

        Return type:
        :   pd.DataFrame

    read\_player\_match\_stats(*match\_id=None*)
    :   Retrieve the player match stats for the selected leagues and seasons.

        Parameters:
        :   **match\_id** (*int* *or* *list* *of* *int**,* *optional*) – Retrieve the player match stats for a specific match.

        Raises:
        :   **ValueError** – If the given match\_id could not be found in the selected seasons.

        Return type:
        :   pd.DataFrame

    read\_shot\_events(*match\_id=None*)
    :   Retrieve the shot events for the selected matches or the selected leagues and seasons.

        Parameters:
        :   **match\_id** (*int* *or* *list* *of* *int**,* *optional*) – Retrieve the shot events for a specific match.

        Raises:
        :   **ValueError** – If the given match\_id could not be found in the selected seasons.

        Return type:
        :   pd.DataFrame

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