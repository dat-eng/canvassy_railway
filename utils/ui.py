import streamlit as st

from utils.constants import RESULT_OPTIONS
from utils.data import get_house_details


# --------------------------------------------------
# Street Selector
# --------------------------------------------------

# def show_street_selector(street_options):

#     return st.selectbox(
#         "Select Street",
#         street_options
#     )


def reset_street_selector():
    st.session_state.selected_street_widget = None
    st.session_state.street_search = "All Streets"


def show_street_selector(street_options):

    street_list = [
        street
        for street in street_options
        if street != "All Streets"
    ]

    if "street_search" not in st.session_state:
        st.session_state.street_search = "All Streets"

    if "selected_street_widget" not in st.session_state:
        st.session_state.selected_street_widget = None

    col1, col2 = st.columns([6, 1])

    with col1:
        selected_street = st.selectbox(
            "Select Street",
            street_list,
            index=None,
            placeholder="All Streets",
            key="selected_street_widget",
        )

    with col2:
        st.write("")
        st.write("")
        st.button(
            "🌎 All Streets",
            on_click=reset_street_selector,
        )

    if selected_street:
        st.session_state.street_search = selected_street

    return st.session_state.street_search

# --------------------------------------------------
# House Selector
# --------------------------------------------------

def show_house_selector(house_df):

    return st.selectbox(
        "Mark House As Canvassed",
        [""] + house_df["Display"].tolist()
    )


# --------------------------------------------------
# House Panel
# --------------------------------------------------

def show_house_panel(house_df):

    selected_display = st.selectbox(
        "House",
        [""] + house_df["Display"].tolist()
    )

    if not selected_display:
        return (
            None,
            False,
            "",
            "",
            False,
        )

    selected_house = house_df.loc[
        house_df["Display"] == selected_display,
        "Address"
    ].iloc[0]

    canvassed, result, notes = get_house_details(selected_house)

    with st.expander("🏠 House Details", expanded=False):
        with st.form("house_panel"):
            canvassed = st.checkbox(
                "Visited",
                value=canvassed
            )

            result = st.selectbox(
                "Result",
                RESULT_OPTIONS,
                index=(
                    RESULT_OPTIONS.index(result)
                    if result in RESULT_OPTIONS
                    else 0
                )
            )

            notes = st.text_area(
                "Notes",
                value=notes,
                height=60
            )

            save_pressed = st.form_submit_button("💾 Save")

    return (
        selected_house,
        canvassed,
        result,
        notes,
        save_pressed,
    )