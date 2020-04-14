import csv
import pandas as pd
from emoji import emojize

def format_similar_names(similar_names, category):
    result, s = similar_names
    if category == "fish":
        s = f"{emojize(':fish:')} for '{s}'\n"
    elif category == "bug":
        s = f"{emojize(':bug:')} for '{s}'\n"
    else:
        s = ""

    len_result = len(result)
    if len_result  == 0:
        return "No results"
    else:
        i = 0
        for k, v in result.items():
            s += f"{k}: {v}\n"
            s = s.replace(r"-", r"\-").replace("\\\\", "\\")
            # Display only 4 similar names, otherwise in some cases
            # we can get the whole list
            if i >= 3:
                break
            i += 1
        return s

def format_info(info):
    row, (similar_names, keyword) = info
    try:
        if row.empty:
            raise ValueError()
        else:
            s = ""
            for k, v in row.iteritems():
                s += f"{k}: {v}\n"
                s = s.replace(r"-", r"\-").replace("\\\\", "\\")
            s += "\n"
            return s
    except (AttributeError, ValueError):
        s = ""
        s += f"No results for: '{keyword}'\n"
        if similar_names:
            s += "\nDid you mean?\n"
            s += "\n".join(list(similar_names.keys())[:3])
            s = s.replace(r"-", r"\-")
        else:
            s += "\nNo similar names where found"
        return s

def get_similar_names(s, category):
    df = pd.read_csv(f"data/{category}_prices.csv",
                     sep=";", quoting=csv.QUOTE_ALL, encoding="utf-8")

    # Getting combinations Name/Price for the Names that contain the used word
    result = {i.strip():p for i, p in zip(list(df.Name), list(df.Price)) if s.lower() in i.lower()}
    return result, s

def get_info(s, category):
    s_lower = s.strip().lower()
    df = pd.read_csv(f"data/{category}_prices.csv",
                     sep=";", quoting=csv.QUOTE_ALL, encoding="utf-8")

    # Getting the information, exactly with the used word
    for idx, row in df.iterrows():
        if s_lower == row["Name"].lower():
            return row, (None, None)

    return None, get_similar_names(s, category)
