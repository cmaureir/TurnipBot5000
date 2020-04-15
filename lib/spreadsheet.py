import re
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
    column_names = ["day"] + [re.sub("\ week\ \d+", "", i) for i in l[0][1:]]
    df = pd.DataFrame.from_records(l, columns=column_names)[:-2]

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

def get_fossils(credentials):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(credentials, scopes=scope)
    gc = gspread.authorize(credentials)

    wks = gc.open("Turnip price tracker").worksheet("Fossils")

    l = wks.get_all_values()
    column_names = ["name1", "name2"] + [re.sub("\ week\ \d+", "", i).lower().replace("á", "a") for i in l[0][2:]]
    df = pd.DataFrame.from_records(l, columns=column_names)[1:-2]

    empty_columns = [i for i, name in enumerate(df.columns) if name == ""]

    df = df.drop(df.columns[empty_columns], axis=1)
    df["name"] = df["name1"] + " " +  df["name2"]
    df["name"] = df["name"].str.strip()
    df = df.drop(["name1", "name2"], axis=1)

    d_missing = {i: None for i in df.columns if i != "name"}
    d_repeated = {i: None for i in df.columns if i != "name"}
    for key, value in d_missing.items():
        d_missing[key] = list(df["name"][df[key].str.lower() != "x"])
        d_repeated[key] = list(df["name"][df[key].str.lower() == "e"])
        d_missing[key] = [i for i in d_missing[key] if i not in d_repeated[key]]

    return d_missing, d_repeated, [i for i in df.columns if i != "name"]
