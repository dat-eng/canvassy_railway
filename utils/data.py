import pandas as pd
import streamlit as st
from datetime import date
from pathlib import Path

from utils.storage import initialize_data_file


# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():
    data_file = initialize_data_file()
    return pd.read_csv(data_file)


# --------------------------------------------------
# Normalize Party
# --------------------------------------------------

def normalize_party(p):

    p = str(p).upper().strip()

    if p.startswith("DEM"):
        return "D"

    elif p.startswith("REP"):
        return "R"

    elif p.startswith("UND"):
        return "U"

    else:
        return "U"


# --------------------------------------------------
# Resolve Party
# --------------------------------------------------

def resolve_party(series):

    parties = set(series)

    if "D" in parties:
        return "D"

    elif "R" in parties:
        return "R"

    else:
        return "U"


# --------------------------------------------------
# Prepare Data
# --------------------------------------------------

def prepare_data(df):

    df = df.copy()

    if "Canvassed" not in df.columns:
        df["Canvassed"] = ""

    if "Result" not in df.columns:
        df["Result"] = ""

    if "Notes" not in df.columns:
        df["Notes"] = ""

    if "CanvassedDate" not in df.columns:
        df["CanvassedDate"] = ""

    df = df.dropna(
        subset=["Latitude", "Longitude"]
    )

    df["Party"] = df["Party"].apply(
        normalize_party
    )

    df = (
        df.groupby("Address", as_index=False)
        .agg(
            {
                "Latitude": "first",
                "Longitude": "first",
                "City": "first",
                "Party": resolve_party,
                "Name": lambda x: ", ".join(x.astype(str)),
                "Canvassed": "first",
                "Result": "first",
                "Notes": "first",
                "CanvassedDate": "first",
            }
        )
    )

    df["Street"] = df["Address"].str.replace(
        r"^\d+\s+",
        "",
        regex=True,
    )

    return df


# --------------------------------------------------
# Street Options
# --------------------------------------------------

def get_street_options(df):

    return (
        ["All Streets"]
        + sorted(
            df["Street"].dropna().unique()
        )
    )


# --------------------------------------------------
# Filter Street
# --------------------------------------------------

def filter_street(df, street_search):

    if street_search != "All Streets":

        df = df[
            df["Street"] == street_search
        ]

    return df


# --------------------------------------------------
# Majority Mode
# --------------------------------------------------

def apply_majority_mode(df):

    def get_majority(series):

        counts = series.value_counts()

        d = counts.get("D", 0)
        r = counts.get("R", 0)

        if d > r:
            return "D"

        elif r > d:
            return "R"

        else:
            return "MIXED"

    df = (
        df.groupby("Street")
        .agg(
            {
                "Latitude": "mean",
                "Longitude": "mean",
                "City": "first",
                "Party": get_majority,
            }
        )
        .reset_index()
    )

    return df


# --------------------------------------------------
# Get House Details
# --------------------------------------------------

def get_house_details(address):

    full_df = load_data()

    if "Canvassed" not in full_df.columns:
        full_df["Canvassed"] = ""

    if "Result" not in full_df.columns:
        full_df["Result"] = ""

    if "Notes" not in full_df.columns:
        full_df["Notes"] = ""

    row = full_df[
        full_df["Address"] == address
    ]

    if row.empty:

        return (
            False,
            "",
            ""
        )

    return (
        str(row.iloc[0]["Canvassed"]).upper() == "Y",
        str(row.iloc[0]["Result"]),
        str(row.iloc[0]["Notes"]),
    )


# --------------------------------------------------
# Save House Details
# --------------------------------------------------

def save_house_details(
    address,
    canvassed,
    result,
    notes,
):

    full_df = load_data()

    for col in ["Canvassed", "Result", "Notes", "CanvassedDate"]:
        if col not in full_df.columns:
            full_df[col] = ""

    full_df.loc[
        full_df["Address"] == address,
        "Canvassed"
    ] = "Y" if canvassed else ""

    full_df.loc[
        full_df["Address"] == address,
        "Result"
    ] = result

    full_df.loc[
        full_df["Address"] == address,
        "Notes"
    ] = notes

    if canvassed:
        full_df.loc[
            full_df["Address"] == address,
            "CanvassedDate"
        ] = date.today().isoformat()
    else:
        full_df.loc[
            full_df["Address"] == address,
            "CanvassedDate"
        ] = ""

    data_file = initialize_data_file()
    temp_file = Path(f"{data_file}.tmp")

    full_df.to_csv(
        temp_file,
        index=False
    )

    temp_file.replace(data_file)

    st.cache_data.clear()