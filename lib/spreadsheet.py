import pandas as pd
import numpy as np
import gspread
from google.oauth2.service_account import Credentials

def get_data(credentials):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(credentials, scopes=scope)
    gc = gspread.authorize(credentials)

    # This uses the filename on Google Drive,
    # and by default we use the 'sheet1', if any of those
    # things changes names, we need to update this
    wks = gc.open("Turnip price tracker").sheet1

    l = wks.get_all_values()
    df = pd.DataFrame.from_records(l)[:-2]

    # Hardcoding columns, since we got two columns in the middle with '$$$$' instead of real names
    # Painful...
    # Add more names here if more people joins
    df.columns = ["day", "Kai", "Diane", "Jen", "Nick", "Helen", "Lara", "lol2", "Miguel", "lol3",
                  "Maria Jose", "Cristian"]

    # Removing the useless columns...
    df = df.drop(["lol2", "lol3"], axis=1)

    # Removing the lines without a day
    df = df[df.day != ""]

    # Selecting only the rows where at least one person added a price
    df = df[(df[list(df.columns)[1:]] != "").any(axis=1)]

    return df

def format_message(d):
    # Get day cell content, and removing it for the sorting
    day = list(d["day"].values())[0]
    del d["day"]

    # Adding NaN for empty values
    d_parsed = {}
    for k, v in d.items():
        try:
            d_parsed[k] = int(list(v.values())[0])
        except ValueError:
            d_parsed[k] = np.nan

    # Order prices
    d_sorted = {k: v for k, v in sorted(d_parsed.items(),
                                        key=lambda i: -1 if i[1] is np.nan else i[1], reverse=True)}

    # Format in Markdown
    s = "```\n"
    s += f"Day: {day}\n"
    for key, value in d_sorted.items():
        if value is np.nan:
            s += f"{key:12}    ?\n"
        else:
            s += f"{key:12} {value:4}\n"
    s += "```\n"
    return s


def get_last(credentials):
    df = get_data(credentials)
    d = df.tail(1).to_dict()
    return format_message(d)

def get_prev(credentials):
    df = get_data(credentials)
    d = df.tail(2).head(1).to_dict()
    return format_message(d)
