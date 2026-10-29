"""
GameDay Analytics Dashboard
Interactive visualizations of NFL attendance patterns (2000-2024)
Built on dbt mart tables from the GameDay Analytics pipeline.

Each insight sentence is built from the numbers on the page, so the text
can't drift away from the charts when the data changes.
"""

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from scipy import stats

# --- Configuration ---

st.set_page_config(
    page_title="GameDay Analytics",
    page_icon="🏈",
    layout="wide",
)

# The pipeline's last step (src/etl/export_dashboard_db.py) copies the dbt marts
# into this file, so a local run and Streamlit Cloud read the same database.
DB_PATH = Path(__file__).parent / "nfl_attendance.db"

@st.cache_data
def load_table(table_name: str) -> pd.DataFrame:
    """Load a mart table from the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


def within_team_effect(df: pd.DataFrame) -> dict:
    """Extra home fans per extra win, comparing each franchise's seasons with its own average.

    Subtracting each franchise's average takes out what never changes for a team
    (stadium size, market), so what's left is how a team's crowd moves with its
    record. Also returns the share of the attendance spread that is between teams.
    """
    by_team = df.groupby("franchise_id")
    attendance = df["avg_home_attendance"] - by_team["avg_home_attendance"].transform("mean")
    wins = df["wins"] - by_team["wins"].transform("mean")

    slope = (wins * attendance).sum() / (wins**2).sum()
    residuals = attendance - slope * wins
    dof = len(df) - df["franchise_id"].nunique() - 1  # one mean per franchise, plus the slope
    std_err = ((residuals**2).sum() / dof / (wins**2).sum()) ** 0.5
    p_value = 2 * stats.t.sf(abs(slope / std_err), dof)

    spread = ((df["avg_home_attendance"] - df["avg_home_attendance"].mean()) ** 2).sum()
    between_share = 1 - (attendance**2).sum() / spread
    return {"slope": slope, "p": p_value, "between_share": between_share}


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
        include_lowest=True,  # keeps the 0-16 seasons (2008 Lions, 2017 Browns) in the first bin
    )

    fig1 = px.violin(
        win_att_plot,
        x="performance_tier",
        y="avg_home_attendance",
        color="performance_tier",
        box=True,
        points="all",
        labels={
            "performance_tier": "Performance Tier",
            "avg_home_attendance": "Avg Home Attendance",
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

    st.plotly_chart(fig1, width="stretch")

with col2:
    within = within_team_effect(win_att_plot)
    real_effect = within["p"] < 0.05
    st.markdown("#### A Real Effect, Not the Main One" if real_effect else "#### No Clear Effect")

    tier_stats = (
        win_att_plot.groupby("performance_tier", observed=True)["avg_home_attendance"]
        .agg(["mean", "count"])
        .round(0)
    )

    for tier, row in tier_stats.iterrows():
        st.metric(
            label=f"{tier} ({int(row['count'])} seasons)",
            value=f"{row['mean']:,.0f}",
        )

    r = win_att_plot["win_percentage"].corr(win_att_plot["avg_home_attendance"])
    p_text = "p < 0.001" if within["p"] < 0.001 else f"p = {within['p']:.3f}"
    if real_effect:
        verdict = "Winning has a real effect, but not the main one"
        why = ", so it isn't just that winning teams have bigger stadiums"
        size = "Still, wins explain only"
    else:
        verdict = "Winning shows no clear effect"
        why = ""
        size = "Wins explain"
    st.markdown(
        f"> **Insight:** {verdict}. Comparing each team's good seasons with its own bad ones, "
        f"every extra win goes with about {within['slope']:,.0f} more fans per home game "
        f"({p_text}){why}. {size} about {r**2:.0%} of the spread in home crowds, "
        f"and {within['between_share']:.0%} of it comes down to which team it is "
        "(stadium size, market)."
    )

    with st.expander("📊 Statistical Detail"):
        tiers = win_att_plot.groupby("performance_tier", observed=True)["avg_home_attendance"]
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
        result = stats.tukey_hsd(*groups)

        st.markdown("**Pairwise Tukey HSD** (p-values):")
        tukey_df = pd.DataFrame(
            result.pvalue,
            index=tier_names,
            columns=tier_names,
        ).round(4)
        st.dataframe(tukey_df, width="stretch")

        n_tiers = len(tier_names)
        n_pairs = n_tiers * (n_tiers - 1) // 2
        n_differ = sum(
            result.pvalue[i][j] < 0.05 for i in range(n_tiers) for j in range(i + 1, n_tiers)
        )
        st.markdown(
            "> Cells ≥ 0.05 mean those two tiers can't be told apart. "
            f"{n_differ} of {n_pairs} tier pairs differ at p < 0.05. Tukey adjusts for making "
            f"all {n_pairs} comparisons at once, so each cell is a strict test: the ANOVA above "
            "answers whether the tiers differ at all, and this table shows where."
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

    st.plotly_chart(fig2, width="stretch")

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

    made = playoff_valid.loc[playoff_valid["prior_playoff_status"] == "Made Playoffs", "attendance_pct_change"]
    missed = playoff_valid.loc[playoff_valid["prior_playoff_status"] == "Missed Playoffs", "attendance_pct_change"]
    welch = stats.ttest_ind(made, missed, equal_var=False)
    verdict = (
        "a real bump, if a small one"
        if welch.pvalue < 0.05
        else "too small to tell apart from noise, so October glory doesn't sell next year's tickets on its own"
    )
    st.markdown(
        f"> **Insight:** After a playoff season, home attendance changes {made.mean():+.1f}% "
        f"on average, against {missed.mean():+.1f}% after a missed one: {verdict} "
        f"(Welch t-test, p = {welch.pvalue:.2f})."
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

    st.plotly_chart(fig3, width="stretch")

with col2:
    st.markdown("#### Weather Factor?")

    variability = {}
    for vtype in ["Indoor", "Outdoor"]:
        subset = venue_plot[venue_plot["venue_type"] == vtype]
        variability[vtype] = subset["attendance_variability_pct"].mean()
        avg_att = subset["avg_attendance"].mean()
        st.metric(
            label=f"{vtype} ({len(subset)} venues)",
            value=f"{variability[vtype]:.1f}% variability",
            delta=f"{avg_att:,.0f} avg attendance",
            delta_color="off",
        )

    steadier, swingier = sorted(variability, key=variability.get)
    st.markdown(
        f"> **Insight:** {swingier} stadiums swing more from game to game than "
        f"{steadier.lower()} ones ({variability[swingier]:.1f}% vs "
        f"{variability[steadier]:.1f}% of the average crowd, lowest to highest). "
        "Regular-season games from 2021 on: 2020's COVID-limited crowds would "
        "swamp any weather signal. Game-day weather data would test the rest."
    )


# --- Footer ---

st.divider()

st.markdown(
    "**Data:** Kaggle NFL Attendance (2000–2019) + ESPN API (2020–2024) · "
    "**Pipeline:** Python ETL → SQLite → dbt → Streamlit · "
    "**Source:** [GitHub](https://github.com/sooperD00/GameDay_Analytics) · "
    "**Author:** [Nicole Rowsey](https://linkedin.com/in/nicole-rowsey)"
)
