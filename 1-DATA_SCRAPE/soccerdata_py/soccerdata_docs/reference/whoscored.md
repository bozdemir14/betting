---
title: "WhoScored"
---

# WhoScored

*class* soccerdata.WhoScored(*leagues=None*, *seasons=None*, *proxy=None*, *no\_cache=False*, *no\_store=False*, *data\_dir=PosixPath('/home/docs/soccerdata/data/WhoScored')*, *path\_to\_browser=None*, *headless=False*)
:   Provides pd.DataFrames from data available at <http://whoscored.com>.

    Data will be downloaded as necessary and cached locally in
    `~/soccerdata/data/WhoScored`.

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
        * **path\_to\_browser** (*Path**,* *optional*) – Path to the Chrome executable.
        * **headless** (*bool**,* *default: True*) – If True, will run Chrome in headless mode. Setting this to False might
          help to avoid getting blocked. Only supported for Selenium <4.13.

    read\_schedule(*force\_cache=False*)
    :   Retrieve the game schedule for the selected leagues and seasons.

        Parameters:
        :   **force\_cache** (*bool*) – By default no cached data is used for the current season.
            If True, will force the use of cached data anyway.

        Return type:
        :   pd.DataFrame

    read\_missing\_players(*match\_id=None*, *force\_cache=False*)
    :   Retrieve a list of injured and suspended players ahead of each game.

        Parameters:
        :   * **match\_id** (*int* *or* *list* *of* *int**,* *optional*) – Retrieve the missing players for a specific game.
            * **force\_cache** (*bool*) – By default no cached data is used to scrapre the list of available
              games for the current season. If True, will force the use of
              cached data anyway.

        Raises:
        :   **ValueError** – If the given match\_id could not be found in the selected seasons.

        Return type:
        :   pd.DataFrame

    read\_events(*match\_id=None*, *force\_cache=False*, *live=False*, *output\_fmt='events'*, *retry\_missing=True*, *on\_error='raise'*)
    :   Retrieve the the event data for each game in the selected leagues and seasons.

        Parameters:
        :   * **match\_id** (*int* *or* *list* *of* *int**,* *optional*) – Retrieve the event stream for a specific game.
            * **force\_cache** (*bool*) – By default no cached data is used to scrape the list of available
              games for the current season. If True, will force the use of
              cached data anyway.
            * **live** (*bool*) – If True, will not return a cached copy of the event data. This is
              usefull to scrape live data.
            * **output\_fmt** (*str**,* *default: 'events'*) –

              The output format of the returned data. Possible values are:
              :   + ’events’ (default): Returns a dataframe with all events.
                  + ’raw’: Returns the original unformatted WhoScored JSON.
                  + ’spadl’: Returns a dataframe with the SPADL representation
                    of the original events.
                    See <https://socceraction.readthedocs.io/en/latest/documentation/SPADL.html#spadl>
                  + ’atomic-spadl’: Returns a dataframe with the Atomic-SPADL representation
                    of the original events.
                    See <https://socceraction.readthedocs.io/en/latest/documentation/SPADL.html#atomic-spadl>
                  + ’loader’: Returns a socceraction.data.opta.OptaLoader
                    instance, which can be used to retrieve the actual data.
                    See <https://socceraction.readthedocs.io/en/latest/modules/generated/socceraction.data.opta.OptaLoader.html#socceraction.data.opta.OptaLoader>
                  + None: Doesn’t return any data. This is useful to just cache
                    the data without storing the events in memory.
            * **retry\_missing** (*bool*) – If no events were found for a game in a previous attempt, will
              retry to scrape the events
            * **on\_error** (*"raise"* *or* *"skip"**,* *default: "raise"*) – Wheter to raise an exception or to skip the game if an error occurs.

        Raises:
        :   * **ValueError** – If the given match\_id could not be found in the selected seasons.
            * **ConnectionError** – If the match page could not be retrieved.
            * **ImportError** – If the requested output format is ‘spadl’, ‘atomic-spadl’ or
              ‘loader’ but the socceraction package is not installed.

        Return type:
        :   See the description of the `output_fmt` parameter.

    *classmethod* available\_leagues()
    :   Return a list of league IDs available for this source.

        Return type:
        :   list[str]