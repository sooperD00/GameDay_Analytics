"""
GameDay Analytics Dashboard
Interactive visualizations of NFL attendance patterns (2000-2019)
Built on dbt mart tables from the GameDay Analytics pipeline.
"""

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- Configuration ---

st.set_page_config(
    page_title="GameDay Analytics",
    page_icon="🏈",
    layout="wide",
)

# Local development: reads from the full pipeline output
# DB_PATH = Path(__file__).parent.parent / "data" / "processed" / "nfl_attendance.db"

# Deployment (Streamlit Cloud): bundled copy since data/processed/ is gitignored
DB_PATH = Path(__file__).parent / "nfl_attendance.db"

@st.cache_data
def load_table(table_name: str) -> pd.DataFrame:
    """Load a mart table from the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


# --- Data ---

win_att = load_table("mart_win_attendance_correlation")
playoff = load_table("mart_playoff_momentum")
venue = load_table("mart_venue_attendance_patterns")


# --- Header ---

st.title("🏈 GameDay Analytics")
st.caption(
    "NFL attendance patterns across 20 seasons of historical data (2000–2019) "
    "and 5 seasons of current data (2020–2024). "
    "Built with Python ETL → SQLite → dbt → Streamlit."
)

st.divider()


# --- Chart 1: Does winning drive attendance? ---

st.header("Does winning drive attendance?")

col1, col2 = st.columns([2, 1])

with col1:
    win_att_plot = win_att.copy()
    win_att_plot["performance_tier"] = pd.cut(
        win_att_plot["wins"],
        bins=[0, 4, 7, 9, 12, 20],
        labels=["Rebuild (0-4)", "Below Avg (5-7)", "Average (8-9)", "Contender (10-12)", "Elite (13+)"],
    )

    fig1 = px.violin(
        win_att_plot,
        x="performance_tier",
        y="avg_weekly_attendance",
        color="performance_tier",
        box=True,
        points="all",
        labels={
            "performance_tier": "Performance Tier",
            "avg_weekly_attendance": "Avg Weekly Attendance",
        },
        color_discrete_sequence=["#d62728", "#ff7f0e", "#bcbd22", "#2ca02c", "#1f77b4"],
        category_orders={
            "performance_tier": [
                "Rebuild (0-4)", "Below Avg (5-7)", "Average (8-9)",
                "Contender (10-12)", "Elite (13+)",
            ]
        },
    )

    fig1.update_traces(opacity=0.7, pointpos=0, jitter=0.4, marker_size=3)
    fig1.update_layout(
        height=500,
        yaxis_tickformat=",",
        showlegend=False,
        margin=dict(t=40),
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### The Counterintuitive Finding")

    tier_stats = (
        win_att_plot.groupby("performance_tier", observed=True)["avg_weekly_attendance"]
        .agg(["mean", "count"])
        .round(0)
    )

    for tier, row in tier_stats.iterrows():
        st.metric(
            label=f"{tier} ({int(row['count'])} seasons)",
            value=f"{row['mean']:,.0f}",
        )

    st.markdown(
        "> **Insight:** Average teams draw comparable or *higher* attendance than "
        "elite teams. Venue capacity ceilings and market size confound raw "
        "numbers — winning alone doesn't fill seats."
    )

    with st.expander("📊 Statistical Detail"):
        from scipy import stats

        tiers = win_att_plot.groupby("performance_tier", observed=True)["avg_weekly_attendance"]
        groups = [group.values for _, group in tiers]
        tier_names = [name for name, _ in tiers]

        # One-way ANOVA
        f_stat, p_value = stats.f_oneway(*groups)
        st.markdown(f"**One-way ANOVA:** F={f_stat:.2f}, p={p_value:.4f}")

        if p_value < 0.05:
            st.markdown("Group means differ significantly — but *where*?")
        else:
            st.markdown("No significant difference across tiers (p ≥ 0.05).")

        # Pairwise Tukey HSD
        from scipy.stats import tukey_hsd
        result = tukey_hsd(*groups)

        st.markdown("**Pairwise Tukey HSD** (p-values):")
        tukey_df = pd.DataFrame(
            result.pvalue,
            index=tier_names,
            columns=tier_names,
        ).round(4)
        st.dataframe(tukey_df, use_container_width=True)

        st.markdown(
            "> Cells ≥ 0.05 mean those two tiers are **not** statistically "
            "distinguishable in attendance. The story holds: performance tier "
            "is a weak predictor of attendance."
        )


st.divider()


# --- Chart 2: Playoff momentum effect ---

st.header("Do playoff teams get an attendance boost?")

col1, col2 = st.columns([2, 1])

with col1:
    # Filter to rows where we have prior season playoff data
    playoff_valid = playoff.dropna(subset=["prior_season_made_playoffs", "attendance_pct_change"]).copy()
    playoff_valid["prior_playoff_status"] = playoff_valid["prior_season_made_playoffs"].map(
        {1: "Made Playoffs", 0: "Missed Playoffs"}
    )

    # Distribution of attendance changes by prior playoff status
    fig2 = px.histogram(
        playoff_valid,
        x="attendance_pct_change",
        color="prior_playoff_status",
        nbins=40,
        barmode="overlay",
        labels={
            "attendance_pct_change": "Year-over-Year Attendance Change (%)",
            "prior_playoff_status": "Prior Season",
            "count": "Number of Team-Seasons",
        },
        color_discrete_map={
            "Made Playoffs": "#2ca02c",
            "Missed Playoffs": "#aaaaaa",
        },
        opacity=0.7,
    )

    fig2.update_layout(
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40),
    )

    # Add vertical lines for group means
    for status, color, dash in [
        ("Made Playoffs", "#2ca02c", "solid"),
        ("Missed Playoffs", "#888888", "dash"),
    ]:
        mean_val = playoff_valid.loc[
            playoff_valid["prior_playoff_status"] == status, "attendance_pct_change"
        ].mean()
        fig2.add_vline(
            x=mean_val,
            line_dash=dash,
            line_color=color,
            line_width=2,
            annotation_text=f"{status}: {mean_val:+.1f}%",
            annotation_position="top",
        )

    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("#### Playoff Bump?")

    for status in ["Made Playoffs", "Missed Playoffs"]:
        subset = playoff_valid[playoff_valid["prior_playoff_status"] == status]
        mean_change = subset["attendance_pct_change"].mean()
        median_change = subset["attendance_pct_change"].median()
        st.metric(
            label=f"After {status} ({len(subset)} seasons)",
            value=f"{mean_change:+.1f}% avg",
            delta=f"{median_change:+.1f}% median",
            delta_color="off",
        )

    st.markdown(
        "> **Insight:** The distributions nearly overlap. Playoff appearances "
        "don't create a meaningful attendance boost. Stadium upgrades, star "
        "signings, and pricing matter more than October glory."
    )


st.divider()


# --- Chart 3: Venue type and attendance stability ---

st.header("Does venue type affect attendance patterns?")

col1, col2 = st.columns([2, 1])

with col1:
    venue_plot = venue.copy()
    venue_plot["avg_attendance"] = venue_plot["avg_attendance"].round(0)

    fig3 = px.scatter(
        venue_plot,
        x="avg_attendance",
        y="attendance_variability_pct",
        color="venue_type",
        size="games_played",
        hover_name="venue_name",
        hover_data={
            "venue_city": True,
            "venue_state": True,
            "games_played": True,
            "avg_attendance": ":,.0f",
            "attendance_variability_pct": ":.1f",
            "venue_type": False,
        },
        labels={
            "avg_attendance": "Avg Attendance",
            "attendance_variability_pct": "Attendance Variability (%)",
            "venue_type": "Venue Type",
            "games_played": "Games Played",
            "venue_city": "City",
            "venue_state": "State",
        },
        color_discrete_map={
            "Indoor": "#1f77b4",
            "Outdoor": "#ff7f0e",
        },
        opacity=0.7,
    )

    fig3.update_layout(
        height=450,
        xaxis_tickformat=",",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40),
    )

    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("#### Weather Factor?")

    for vtype in ["Indoor", "Outdoor"]:
        subset = venue_plot[venue_plot["venue_type"] == vtype]
        avg_var = subset["attendance_variability_pct"].mean()
        avg_att = subset["avg_attendance"].mean()
        st.metric(
            label=f"{vtype} ({len(subset)} venues)",
            value=f"{avg_var:.1f}% variability",
            delta=f"{avg_att:,.0f} avg attendance",
            delta_color="off",
        )

    st.markdown(
        "> **Insight:** Indoor and outdoor venues show similar variability. "
        "Weather doesn't dominate attendance patterns — opponent quality "
        "and market factors matter more."
    )


# --- Footer ---

st.divider()

st.markdown(
    "**Data:** Kaggle NFL Attendance (2000–2019) + ESPN API (2020–2024) · "
    "**Pipeline:** Python ETL → SQLite → dbt → Streamlit · "
    "**Source:** [GitHub](https://github.com/sooperD00/GameDay_Analytics) · "
    "**Author:** [Nicole Rowsey](https://linkedin.com/in/nicole-rowsey)"
)
