import pandas as pd
import streamlit as st
import pydeck as pdk
from streamlit_js_eval import streamlit_js_eval

from utils.auth import authenticate
from utils.data import (
    load_data,
    prepare_data,
    get_street_options,
    filter_street,
    apply_majority_mode,
    save_house_details,
)
from utils.gps import get_gps_location
from utils.map import (
    prepare_map_data,
    create_view_state,
    create_scatter_layer,
    create_house_number_layer,
    create_deck,
    create_gps_layers,
)
from utils.reports import show_simple_reports
from utils.ui import (
    show_street_selector,
    show_house_panel,
)

# --------------------------------------------------
# Authentication
# --------------------------------------------------

authenticate()

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(layout="wide")

st.title("🗳️ Canvassy")

show_majority = st.checkbox("Show Majority Areas Only", value=False)

show_location = st.checkbox("📍 Show My Location", value=True)

gps_location = get_gps_location(show_location)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_data()
df = prepare_data(df)
show_simple_reports(df)

if df.empty:
    st.warning("No data available")
    st.stop()

# --------------------------------------------------
# Street Name
# --------------------------------------------------

street_options = get_street_options(df)
street_search = show_street_selector(
    street_options
)

# --------------------------------------------------
# Street Search Filter
# --------------------------------------------------

df = filter_street(df, street_search)

# --------------------------------------------------
# House Details
# --------------------------------------------------

if not show_majority:

    house_df = (
        df[
            [
                "Address",
                "Canvassed",
                "Result",
                "Notes",
            ]
        ]
        .drop_duplicates()
        .sort_values("Address")
    )

    house_df["Display"] = house_df.apply(
        lambda r: (
            f"✓ {r['Address']}"
            if str(r["Canvassed"]).upper() == "Y"
            else r["Address"]
        ),
        axis=1,
    )

    (
        selected_house,
        canvassed,
        result,
        notes,
        save_pressed,
    ) = show_house_panel(
        house_df
    )

    if selected_house and save_pressed:

        save_house_details(
            selected_house,
            canvassed,
            result,
            notes,
        )

        st.success(
            f"{selected_house} saved"
        )

        st.rerun()

# --------------------------------------------------
# Majority Mode
# --------------------------------------------------

if show_majority:
    df = apply_majority_mode(df)

# --------------------------------------------------
# Safety Cleanup
# --------------------------------------------------

df["Latitude"] = pd.to_numeric(
    df["Latitude"],
    errors="coerce"
)

df["Longitude"] = pd.to_numeric(
    df["Longitude"],
    errors="coerce"
)

df = df.dropna(
    subset=["Latitude", "Longitude"]
).copy()

if df.empty:
    st.warning("No matching streets found")
    st.stop()

# --------------------------------------------------
# Map Labels, colors and radius
# --------------------------------------------------

df = prepare_map_data(df, show_majority)

# --------------------------------------------------
# View State
# --------------------------------------------------

view_state = create_view_state(df, street_search, gps_location)

# --------------------------------------------------
# Scatterplot Layer
# --------------------------------------------------

scatter_layer = create_scatter_layer(df)

# --------------------------------------------------
# Layers
# --------------------------------------------------

layers = [scatter_layer]

gps_radius = 30 if street_search == "All Streets" else 10

gps_layer = create_gps_layers(
    gps_location,
    gps_radius
)
if gps_layer:
    layers.append(gps_layer)

# --------------------------------------------------
# House Numbers in Normal Mode
# --------------------------------------------------

if not show_majority:
    layers.append(create_house_number_layer(df))

# --------------------------------------------------
# Tooltip & deck
# --------------------------------------------------

deck = create_deck(
    layers,
    view_state,
    show_majority
)

# --------------------------------------------------
# Render Map
# --------------------------------------------------

st.pydeck_chart(deck, use_container_width=True)