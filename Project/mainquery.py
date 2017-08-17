def mainquery(DBtable, searchstring):
    """
    This function runs a searchstring query on the database table.

    Input:
        DBtable: The name of the database table to query
        searchstring: The user-supplied string to search for.
    Output:
        df: a DataFrame with all the headlines and metadata that match the
            searchstring.
    """
    from ..Project.utilities import ExtractHeadlines
    import pandas as pd

    queryresult = ExtractHeadlines(DBtable, searchstring)

    df = pd.DataFrame.from_records(queryresult, columns=['Headline',
                                                         'Source',
                                                         'Scrape Timestamp'
                                                         ])
    return df
