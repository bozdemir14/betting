---
title: "Club Elo"
---

# Club Elo

*class* soccerdata.ClubElo(*proxy=None*, *no\_cache=False*, *no\_store=False*, *data\_dir=PosixPath('/home/docs/soccerdata/data/ClubElo')*)
:   Provides pd.DataFrames from CSV API at <http://api.clubelo.com>.

    Data will be downloaded as necessary and cached locally in
    `~/soccerdata/data/ClubElo`.

    Since the source does not provide league names, this class will not filter
    by league. League names will be inserted from the other sources where
    available. Leagues that are only covered by clubelo.com will have NaN
    values.

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

    read\_by\_date(*date=None*)
    :   Retrieve ELO scores for all teams at specified date.

        Elo scores are available as early as 1939. Values before 1960 should
        be considered provisional.

        Parameters:
        :   **date** (*datetime object* *or* *string like 'YYYY-MM-DD'*) – Date for which to retrieve ELO scores. If no date is specified,
            get today’s scores.

        Raises:
        :   * **TypeError** – If date is not a date string or datetime object.
            * **ValueError** – If data is an invalid date string.

        Return type:
        :   pd.DataFrame

    read\_team\_history(*team*, *max\_age=1*)
    :   Retrieve full ELO history for one club.

        For the exact spelling of a club’s name, check the result of
        [`read_by_date()`](clubelo.md#soccerdata.ClubElo.read_by_date "soccerdata.ClubElo.read_by_date") or [clubelo.com](http://clubelo.com/Ranking). You can also use alternative team
        names specified in teamname\_replacements.json. Values before 1960
        should be considered provisional.

        Parameters:
        :   * **team** (*str*) – The club’s name.
            * **max\_age** (*int for age in days**, or* *timedelta object*) – The max. age of locally cached file before re-download.

        Raises:
        :   * **TypeError** – If max\_age is not an integer or timedelta object.
            * **ValueError** – If no ratings for the given team are available.

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

    *property* seasons*: list[str]*
    :   Return a list of selected seasons.