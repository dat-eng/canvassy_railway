import pandas as pd
import streamlit as st


# --------------------------------------------------
# Reporting
# --------------------------------------------------

def show_simple_reports(df):

    if "Canvassed" not in df.columns:
        df["Canvassed"] = ""

    if "CanvassedDate" not in df.columns:
        df["CanvassedDate"] = ""

    with st.expander("📊 Canvassing Report", expanded=False):

        # --------------------------------------------------
        # Overall Statistics
        # --------------------------------------------------

        total_houses = len(df)

        visited_houses = (
            df["Canvassed"]
            .astype(str)
            .str.upper()
            .eq("Y")
            .sum()
        )

        percent_visited = (
            visited_houses / total_houses * 100
            if total_houses > 0
            else 0
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Houses",
            f"{total_houses:,}"
        )

        col2.metric(
            "Visited",
            f"{visited_houses:,}"
        )

        col3.metric(
            "Visited %",
            f"{percent_visited:.1f}%"
        )

        st.progress(
            min(
                percent_visited / 100,
                1.0
            )
        )

        # --------------------------------------------------
        # Houses Visited by Date
        # --------------------------------------------------

        visited_by_date = (
            df[
                df["Canvassed"]
                .astype(str)
                .str.upper()
                .eq("Y")
            ]
            .groupby("CanvassedDate")
            .size()
            .reset_index(name="Houses Visited")
        )

        visited_by_date = visited_by_date[
            visited_by_date["CanvassedDate"] != ""
        ]

        if not visited_by_date.empty:

            visited_by_date = visited_by_date.sort_values(
                "CanvassedDate",
                ascending=False
            )

            st.subheader("Houses Visited by Date")

            st.dataframe(
                visited_by_date,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No visited houses by date yet."
            )

        # --------------------------------------------------
        # Street Progress
        # --------------------------------------------------

        street_progress = (
            df.groupby("Street")
            .agg(
                Houses=("Address", "count"),
                Visited=(
                    "Canvassed",
                    lambda x: (
                        x.astype(str)
                        .str.upper()
                        .eq("Y")
                        .sum()
                    ),
                ),
            )
            .reset_index()
        )

        street_progress["Percent"] = (
            street_progress["Visited"]
            / street_progress["Houses"]
            * 100
        ).round().astype(int)

        street_progress["Visited"] = (
            street_progress["Visited"].astype(str)
            + "/"
            + street_progress["Houses"].astype(str)
        )

        street_progress["Percent"] = (
            street_progress["Percent"].astype(str)
            + "%"
        )

        def get_status(percent):

            value = int(percent.rstrip("%"))

            if value == 100:
                return "✅ Completed"

            elif value == 0:
                return "⚪ Not Started"

            else:
                return "🟡 In Progress"

        street_progress["Status"] = (
            street_progress["Percent"]
            .apply(get_status)
        )

        street_progress["SortOrder"] = (
            street_progress["Status"]
            .map(
                {
                    "🟡 In Progress": 0,
                    "⚪ Not Started": 1,
                    "✅ Completed": 2,
                }
            )
        )

        street_progress = street_progress.sort_values(
            ["SortOrder", "Street"],
            ascending=[True, True]
        )

        st.subheader("Street Progress")

        st.caption(
            "Sorted by streets that still need work."
        )

        st.dataframe(
            street_progress[
                [
                    "Status",
                    "Street",
                    "Visited",
                    "Percent",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )