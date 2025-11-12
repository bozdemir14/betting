---
title: "Base Readers"
---

# Base Readers

The logic for downloading data from the web is implemented in the base classes
that are documented here. The base classes are not intended to be used directly
but rather to be subclassed by the specific readers which implement the logic
to parse the data.

The `BaseRequestsReader` is a wrapper around the requests library
and is used by scrapers that do not require JavaScript to be executed. The
`BaseSeleniumReader` is a wrapper around the selenium library and is
used by scrapers that require JavaScript to be executed.

*class* soccerdata.\_common.BaseRequestsReader(*leagues=None*, *proxy=None*, *no\_cache=False*, *no\_store=False*, *data\_dir=PosixPath('/home/docs/soccerdata/data')*)
:   Base class for readers that use the Python requests module.

    Parameters:
    :   * **leagues** (*str* *|* *list**[**str**]* *|* *None*)
        * **proxy** (*str* *|* *list**[**str**]* *|* *Callable**[**[**]**,* *str**]* *|* *None*)
        * **no\_cache** (*bool*)
        * **no\_store** (*bool*)
        * **data\_dir** (*Path*)

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

*class* soccerdata.\_common.BaseSeleniumReader(*leagues=None*, *proxy=None*, *no\_cache=False*, *no\_store=False*, *data\_dir=PosixPath('/home/docs/soccerdata/data')*, *path\_to\_browser=None*, *headless=True*)
:   Base class for readers that use Selenium.

    Parameters:
    :   * **leagues** (*str* *|* *list**[**str**]* *|* *None*)
        * **proxy** (*str* *|* *list**[**str**]* *|* *Callable**[**[**]**,* *str**]* *|* *None*)
        * **no\_cache** (*bool*)
        * **no\_store** (*bool*)
        * **data\_dir** (*Path*)
        * **path\_to\_browser** (*Path* *|* *None*)
        * **headless** (*bool*)

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