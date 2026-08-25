import pandas as pd
import pydeck as pdk


# --------------------------------------------------
# Colors
# --------------------------------------------------

def get_fill_color(row):

    if row["Party"] == "D":
        return [0, 0, 255]

    elif row["Party"] == "R":
        return [255, 0, 0]

    elif row["Party"] == "MIXED":
        return [150, 0, 150]

    return [120, 120, 120]


def get_line_color(row):

    canvassed = str(
        row.get("Canvassed", "")
    ).upper().strip()

    if canvassed == "Y":
        return [0, 255, 0]

    return [255, 255, 255]


# --------------------------------------------------
# Radius
# --------------------------------------------------

def get_radius(party):

    if party == "MIXED":
        return 80

    return 50


# --------------------------------------------------
# Labels
# --------------------------------------------------

def prepare_map_data(df, show_majority):

    if show_majority:
        df["Label"] = df["Street"]
    else:
        df["Label"] = df["Address"]

    df["fill_color"] = df.apply(
        get_fill_color,
        axis=1
    )

    df["line_color"] = df.apply(
        get_line_color,
        axis=1
    )

    df["radius"] = df["Party"].apply(
        get_radius
    )

    return df


# --------------------------------------------------
# View State
# --------------------------------------------------

def create_view_state(df, street_search, gps_location=None):

    if gps_location:
        center_lat = gps_location["latitude"]
        center_lon = gps_location["longitude"]
    else:
        center_lat = df["Latitude"].mean()
        center_lon = df["Longitude"].mean()

    if pd.isna(center_lat) or pd.isna(center_lon):
        center_lat = 42.0
        center_lon = -71.0

    if street_search == "All Streets" and gps_location:
        zoom = 14
    elif street_search == "All Streets":
        zoom = 12
    else:
        zoom = 16

    return pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=zoom,
        pitch=0,
    )


# --------------------------------------------------
# Scatter Layer
# --------------------------------------------------

def create_scatter_layer(df):

    return pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[Longitude, Latitude]",
        get_fill_color="fill_color",
        get_line_color="line_color",
        line_width_min_pixels=2,
        get_radius="radius",
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_min_pixels=3,
        radius_max_pixels=20,
    )


# --------------------------------------------------
# House Number Layer
# --------------------------------------------------

def create_house_number_layer(df):

    df["HouseNumber"] = (
        df["Address"]
        .astype(str)
        .str.extract(r"^(\d+)")
        .fillna("")
    )

    return pdk.Layer(
        "TextLayer",
        data=df,
        get_position="[Longitude, Latitude]",
        get_text="HouseNumber",
        get_size=10,
        get_color=[255, 255, 255],
        get_angle=0,
        get_text_anchor="'middle'",
        get_alignment_baseline="'center'",
        pickable=False,
    )


# --------------------------------------------------
# Tooltip
# --------------------------------------------------

def get_tooltip(show_majority):

    if show_majority:

        return {
            "html": 
                "{Label}, {City}<br>"
                "Party: {Party}<br>"
        }

    return {
        "html": 
            "{Label}, {City}<br>"
            "Party: {Party}<br>"
            "{Name}<br>"
            "Canvassed: {Canvassed}"
    }


# --------------------------------------------------
# Deck
# --------------------------------------------------

def create_deck(
    layers,
    view_state,
    show_majority
):

    return pdk.Deck(
        map_style="road",
        initial_view_state=view_state,
        layers=layers,
        tooltip=get_tooltip(show_majority),
    )


# --------------------------------------------------
# GPS Layers
# --------------------------------------------------

def create_gps_layers(gps_location, radius):

    if not gps_location:
        return []

    # Outer white ring
    outer = pdk.Layer(
        "ScatterplotLayer",
        data=[gps_location],
        get_position="[longitude, latitude]",
        get_fill_color=[255, 255, 255],
        get_radius=radius + 8,
        opacity=0.9,
        stroked=False,
        filled=True,
        pickable=False,
    )

    # Inner green dot
    inner = pdk.Layer(
        "ScatterplotLayer",
        data=[gps_location],
        get_position="[longitude, latitude]",
        get_fill_color=[0, 220, 0],
        get_radius=radius,
        opacity=1.0,
        stroked=False,
        filled=True,
        pickable=False,
    )

    return [outer, inner]
