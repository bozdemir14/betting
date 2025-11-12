---
title: "Utilities"
---

# Utilities

\_common.SeasonCode(*names=None*, *\**, *module=None*, *qualname=None*, *type=None*, *start=1*, *boundary=None*)
:   How to interpret season codes.

    SINGLE\_YEAR
    :   Type:
        :   The season code is a single year, e.g. ‘2021’.

    soccerdata.MULTI\_YEAR
    :   Type:
        :   The season code is a range of years, e.g. ‘2122’.

\_common.make\_game\_id()
:   Return a game id based on date, home and away team.

    Parameters:
    :   **row** (*Series*)

    Return type:
    :   str

\_common.standardize\_colnames(*cols=None*)
:   Convert DataFrame column names to snake case.

    Parameters:
    :   * **df** (*DataFrame*)
        * **cols** (*list**[**str**]* *|* *None*)

    Return type:
    :   *DataFrame*

\_common.get\_proxy()
:   Return a public proxy.

    Return type:
    :   dict[str, str]

\_common.check\_proxy()
:   Check if proxy is working.

    Parameters:
    :   **proxy** (*dict*)

    Return type:
    :   bool