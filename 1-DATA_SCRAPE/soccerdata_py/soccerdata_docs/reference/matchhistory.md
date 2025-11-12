---
title: "MatchHistory"
---

# MatchHistory

*class* soccerdata.MatchHistory(*leagues=None*, *seasons=None*, *proxy=None*, *no\_cache=False*, *no\_store=False*, *data\_dir=PosixPath('/home/docs/soccerdata/data/MatchHistory')*)
:   Provides pd.DataFrames from CSV files available at <http://www.football-data.co.uk/data.php>.

    Data will be downloaded as necessary and cached locally in
    `~/soccerdata/data/MatchHistory`.

    Parameters:
    :   * **leagues** (*string* *or* *iterable*) – IDs of leagues to include.
        * **seasons** (*string**,* *int* *or* *list*) – Seasons to include. Supports multiple formats.
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
        * **data\_dir** (*Path**,* *optional*) – Path to directory where data will be cached.

    *property* seasons*: list[str]*
    :   Return a list of selected seasons.

    read\_games()
    :   Retrieve game history for the selected leagues and seasons.

        Column names are explained here: <http://www.football-data.co.uk/notes.txt>

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