import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# DARK THEME STYLING
# ----------------------------------------------------------------------------
st.markdown("""
<style>
    :root {
        --bg-main: #0e1117;
        --bg-card: #161b22;
        --bg-card-hover: #1c2330;
        --accent: #7c5cff;
        --accent2: #22d3ee;
        --accent3: #f472b6;
        --text-main: #e6edf3;
        --text-sub: #8b949e;
        --border: #2a3140;
    }

    .stApp {
        background: radial-gradient(circle at 10% 0%, #161c2c 0%, #0b0e14 55%, #090b10 100%);
        color: var(--text-main);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #11151f 0%, #0b0e15 100%);
        border-right: 1px solid var(--border);
    }

    h1, h2, h3, h4 {
        color: var(--text-main) !important;
        font-family: 'Segoe UI', sans-serif;
    }

    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #7c5cff, #22d3ee, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    .sub-title {
        color: var(--text-sub);
        font-size: 1rem;
        margin-top: -8px;
        margin-bottom: 25px;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161b22, #1a2130);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px 20px 10px 20px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.35);
        transition: 0.25s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: var(--accent);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(124,92,255,0.25);
    }
    div[data-testid="stMetricLabel"] {
        color: var(--text-sub) !important;
    }
    div[data-testid="stMetricValue"] {
        color: var(--accent2) !important;
        font-weight: 700 !important;
    }

    /* Divider glow line */
    .glow-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, #7c5cff, #22d3ee, #f472b6, transparent);
        border: none;
        margin: 10px 0 25px 0;
        opacity: 0.7;
    }

    /* Chart containers */
    .chart-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 10px 12px 0px 12px;
        margin-bottom: 18px;
    }

    /* Multiselect & selectbox tags */
    span[data-baseweb="tag"] {
        background-color: var(--accent) !important;
    }

    .stDataFrame {
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

PLOTLY_TEMPLATE = "plotly_dark"
COLOR_SEQ = ["#7c5cff", "#22d3ee", "#f472b6", "#facc15", "#34d399", "#fb923c"]
GRADE_COLORS = {"A": "#34d399", "B": "#22d3ee", "C": "#facc15", "D": "#fb923c", "F": "#f87171"}


# ----------------------------------------------------------------------------
# DATA LOADING
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("student_performance.csv")
    bins = [0, 5, 10, 15, 20, 25, 30, 100]
    labels = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30+"]
    df["study_hours_bucket"] = pd.cut(df["weekly_self_study_hours"], bins=bins, labels=labels, right=False)
    att_bins = [0, 60, 70, 80, 90, 100.1]
    att_labels = ["<60%", "60-70%", "70-80%", "80-90%", "90-100%"]
    df["attendance_bucket"] = pd.cut(df["attendance_percentage"], bins=att_bins, labels=att_labels, right=False)
    return df

df = load_data()

# ----------------------------------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------------------------------
st.sidebar.markdown("## 🎛️ Filters")
st.sidebar.markdown("Use these to slice the dataset")

grades_all = sorted(df["grade"].unique().tolist())
grade_sel = st.sidebar.multiselect("Grade", grades_all, default=grades_all)

study_min, study_max = float(df["weekly_self_study_hours"].min()), float(df["weekly_self_study_hours"].max())
study_range = st.sidebar.slider("Weekly Self-Study Hours", study_min, study_max, (study_min, study_max))

att_min, att_max = float(df["attendance_percentage"].min()), float(df["attendance_percentage"].max())
att_range = st.sidebar.slider("Attendance %", att_min, att_max, (att_min, att_max))

part_min, part_max = float(df["class_participation"].min()), float(df["class_participation"].max())
part_range = st.sidebar.slider("Class Participation", part_min, part_max, (part_min, part_max))

score_min, score_max = float(df["total_score"].min()), float(df["total_score"].max())
score_range = st.sidebar.slider("Total Score", score_min, score_max, (score_min, score_max))

st.sidebar.markdown("---")
sample_note = st.sidebar.checkbox("⚡ Speed mode (sample 50k rows for charts)", value=True,
                                   help="Dataset has 1M rows. Sampling keeps charts fast; KPIs still use full filtered data.")

# ----------------------------------------------------------------------------
# APPLY FILTERS
# ----------------------------------------------------------------------------
mask = (
    df["grade"].isin(grade_sel)
    & df["weekly_self_study_hours"].between(*study_range)
    & df["attendance_percentage"].between(*att_range)
    & df["class_participation"].between(*part_range)
    & df["total_score"].between(*score_range)
)
fdf = df[mask]

chart_df = fdf.sample(n=50000, random_state=42) if (sample_note and len(fdf) > 50000) else fdf

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown('<div class="main-title">🎓 Student Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Interactive analytics over {len(df):,} student records — filtered: {len(fdf):,} records</div>', unsafe_allow_html=True)
st.markdown('<hr class="glow-line">', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# KPI ROW
# ----------------------------------------------------------------------------
if len(fdf) == 0:
    st.warning("No records match the selected filters. Try widening the ranges.")
    st.stop()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("👥 Students", f"{len(fdf):,}")
k2.metric("📊 Avg Score", f"{fdf['total_score'].mean():.1f}")
k3.metric("📚 Avg Study Hrs/wk", f"{fdf['weekly_self_study_hours'].mean():.1f}")
k4.metric("🗓️ Avg Attendance", f"{fdf['attendance_percentage'].mean():.1f}%")
k5.metric("🙋 Avg Participation", f"{fdf['class_participation'].mean():.1f}")

st.markdown('<hr class="glow-line">', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# ROW 1: Grade Distribution + Score Distribution
# ----------------------------------------------------------------------------
c1, c2 = st.columns([1, 1.3])

with c1:
    st.markdown("#### 🏅 Grade Distribution")
    grade_counts = fdf["grade"].value_counts().reindex(["A", "B", "C", "D", "F"]).dropna().reset_index()
    grade_counts.columns = ["grade", "count"]
    fig = px.pie(
        grade_counts, names="grade", values="count", hole=0.55,
        color="grade", color_discrete_map=GRADE_COLORS, template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textinfo="percent+label", textfont_size=13)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.1), margin=dict(t=10, b=10, l=10, r=10), height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("#### 📈 Total Score Distribution")
    fig = px.histogram(
        chart_df, x="total_score", nbins=40, color_discrete_sequence=[COLOR_SEQ[0]],
        template=PLOTLY_TEMPLATE,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        bargap=0.05, margin=dict(t=10, b=10, l=10, r=10), height=380,
        xaxis_title="Total Score", yaxis_title="Count",
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# ROW 2: Study hours vs Score (scatter) + Attendance vs Score
# ----------------------------------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    st.markdown("#### 📖 Study Hours vs Total Score")
    fig = px.scatter(
        chart_df, x="weekly_self_study_hours", y="total_score", color="grade",
        color_discrete_map=GRADE_COLORS, opacity=0.5, template=PLOTLY_TEMPLATE,
        labels={"weekly_self_study_hours": "Weekly Study Hours", "total_score": "Total Score"},
    )
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10), height=380,
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.markdown("#### 🗓️ Attendance vs Total Score")
    fig = px.scatter(
        chart_df, x="attendance_percentage", y="total_score", color="grade",
        color_discrete_map=GRADE_COLORS, opacity=0.5, template=PLOTLY_TEMPLATE,
        labels={"attendance_percentage": "Attendance %", "total_score": "Total Score"},
    )
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10), height=380,
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# ROW 3: Avg score by study bucket (bar) + Avg score by attendance bucket (bar)
# ----------------------------------------------------------------------------
c5, c6 = st.columns(2)

with c5:
    st.markdown("#### 📚 Avg Score by Study-Hours Group")
    grp = fdf.groupby("study_hours_bucket", observed=True)["total_score"].mean().reset_index()
    fig = px.bar(
        grp, x="study_hours_bucket", y="total_score", color="total_score",
        color_continuous_scale=["#22d3ee", "#7c5cff", "#f472b6"], template=PLOTLY_TEMPLATE,
        labels={"study_hours_bucket": "Weekly Study Hours", "total_score": "Avg Score"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10), height=380, coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)

with c6:
    st.markdown("#### 🗓️ Avg Score by Attendance Group")
    grp = fdf.groupby("attendance_bucket", observed=True)["total_score"].mean().reset_index()
    fig = px.bar(
        grp, x="attendance_bucket", y="total_score", color="total_score",
        color_continuous_scale=["#f472b6", "#7c5cff", "#22d3ee"], template=PLOTLY_TEMPLATE,
        labels={"attendance_bucket": "Attendance %", "total_score": "Avg Score"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10), height=380, coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# ROW 4: Correlation heatmap + Participation vs Score box
# ----------------------------------------------------------------------------
c7, c8 = st.columns([1, 1.3])

with c7:
    st.markdown("#### 🔥 Correlation Heatmap")
    num_cols = ["weekly_self_study_hours", "attendance_percentage", "class_participation", "total_score"]
    corr = fdf[num_cols].corr()
    fig = px.imshow(
        corr, text_auto=".2f", color_continuous_scale=["#0e1117", "#7c5cff", "#22d3ee"],
        template=PLOTLY_TEMPLATE, aspect="auto",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10), height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

with c8:
    st.markdown("#### 🙋 Score Spread by Grade")
    fig = px.box(
        chart_df, x="grade", y="total_score", color="grade",
        color_discrete_map=GRADE_COLORS, template=PLOTLY_TEMPLATE,
        category_orders={"grade": ["A", "B", "C", "D", "F"]},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10), height=380, showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# DATA TABLE
# ----------------------------------------------------------------------------
st.markdown('<hr class="glow-line">', unsafe_allow_html=True)
st.markdown("#### 🗂️ Filtered Data Preview")
st.dataframe(
    fdf.drop(columns=["study_hours_bucket", "attendance_bucket"]).head(500),
    use_container_width=True, height=320,
)

csv = fdf.drop(columns=["study_hours_bucket", "attendance_bucket"]).to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Data (CSV)", csv, "filtered_student_data.csv", "text/csv")

st.markdown(
    '<div style="text-align:center; color:#8b949e; margin-top:30px; font-size:0.85rem;">'
    'Built with ❤️ using Streamlit + Plotly</div>',
    unsafe_allow_html=True,
)
