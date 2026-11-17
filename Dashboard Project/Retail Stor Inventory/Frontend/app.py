import streamlit as st
import pandas as pd
import requests


# ========================================
# 1. PAGE CONFIG
# ========================================
st.set_page_config(
    page_title="Shivnetra Industries Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ========================================
# 2. CUSTOM CSS
# ========================================
st.markdown("""
    <style>

    /* Main Background */
    .stApp {
        background-color: #0A0F1C;
    }

    /* KPI Cards Styling */
    .kpi-card {
        background-color: #111827;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #1f2937;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    /* Mouse Hover Effect */
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }

    .kpi-label {
        font-size: 15px;
        color: #9ca3af;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #3b82f6;
    }

    </style>
""", unsafe_allow_html=True)


# ========================================
# 3. PAGE TITLE
# ========================================
st.title("Shivnetra Industries: Retail Operations Dashboard")
st.markdown("---")


# ========================================
# 4. FETCH DATA WITH CACHE
# ========================================
@st.cache_data(ttl=60)
def get_data():
    response = requests.get(
        "http://127.0.0.1:8000/api/get_retail_data"
    )
    return pd.DataFrame(response.json())


df = get_data()


# ========================================
# 5. DATE FORMAT FIX
# ========================================
df['Date'] = pd.to_datetime(
    df['Date'],
    dayfirst=True,
    format='mixed'
)


# ========================================
# 6. RESET BUTTON LOGIC
# ========================================
def reset_filters():
    for key in [
        'date_picker',
        'region_picker',
        'cat_picker',
        'weather_picker',
        'holiday_picker'
    ]:
        if key in st.session_state:
            del st.session_state[key]


# ========================================
# 7. SIDEBAR UI & SLICERS
# ========================================
st.sidebar.markdown(
    "<h2 style='text-align: center; color: white;'>🎯 Filters</h2>",
    unsafe_allow_html=True
)

st.sidebar.button(
    "🔄 Reset All Filters",
    on_click=reset_filters,
    key="reset_btn_shivnetra_123"
)

st.sidebar.markdown("---")


# ========================================
# 8. DATE FILTER
# ========================================
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

date_range = st.sidebar.date_input(
    "📅 Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date,
    key='date_picker'
)


# ========================================
# 9. REGION FILTER
# ========================================
all_regions = [
    "All"
] + df['Region'].dropna().unique().tolist()

sel_regions = st.sidebar.selectbox(
    "📍 Region",
    all_regions,
    index=0,
    key='region_picker'
)


# ========================================
# 10. CATEGORY FILTER
# ========================================
all_categories = [
    "All"
] + df['Category'].dropna().unique().tolist()

sel_categories = st.sidebar.selectbox(
    "🛒 Category",
    all_categories,
    index=0,
    key='cat_picker'
)


# ========================================
# 11. WEATHER FILTER
# ========================================
all_weather = [
    "All"
] + df['Weather Condition'].dropna().unique().tolist()

sel_weather = st.sidebar.selectbox(
    "🌤️ Weather Condition",
    all_weather,
    index=0,
    key='weather_picker'
)


# ========================================
# 12. HOLIDAY / PROMOTION FILTER
# ========================================
all_holidays = [
    "All"
] + df['Holiday/Promotion'].astype(str).unique().tolist()

sel_holiday = st.sidebar.selectbox(
    "🎁 Holiday / Promotion",
    all_holidays,
    index=0,
    key='holiday_picker'
)


# ========================================
# 13. DATE RANGE LOGIC
# ========================================
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date


# ========================================
# 14. DYNAMIC DATA FILTERING
# ========================================

# Date filter
mask = (
    (df['Date'].dt.date >= start_date) &
    (df['Date'].dt.date <= end_date)
)


# Region filter
if sel_regions != "All":
    mask = mask & (
        df['Region'] == sel_regions
    )


# Category filter
if sel_categories != "All":
    mask = mask & (
        df['Category'] == sel_categories
    )


# Weather filter
if sel_weather != "All":
    mask = mask & (
        df['Weather Condition'] == sel_weather
    )


# Holiday / Promotion filter
if sel_holiday != "All":
    mask = mask & (
        df['Holiday/Promotion'].astype(str) == sel_holiday
    )


# Final filtered data
filtered_df = df[mask].copy()


# ========================================
# 15. KPI CALCULATIONS
# ========================================

tot_rev = f"₹{filtered_df['Total Revenue'].sum():,.0f}"

tot_units = f"{filtered_df['Units Sold'].sum():,.0f}"

avg_demand = f"{filtered_df['Demand Forecast'].mean():,.0f}"

curr_inv = f"{filtered_df['Inventory Level'].sum():,.0f}"

avg_disc = f"{filtered_df['Discount'].mean():.2f}%"

comp_price = f"₹{filtered_df['Competitor Pricing'].mean():,.2f}"


# ========================================
# 16. KPI CARDS
# ========================================

col1, col2, col3, col4, col5, col6 = st.columns(6)


kpis = [
    ("Total Revenue", tot_rev),
    ("Total Unit Sold", tot_units),
    ("Avg Demand Forecast", avg_demand),
    ("Current Inventory", curr_inv),
    ("Avg Discount Given", avg_disc),
    ("Competitor Avg Price", comp_price)
]


cols = [
    col1,
    col2,
    col3,
    col4,
    col5,
    col6
]


for col, (label, value) in zip(cols, kpis):

    with col:

        st.markdown(
            f'''
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )





# ========================================
# 17. CHARTS LAYOUT & CONFIG
# ========================================
st.markdown("<br>", unsafe_allow_html=True)


chart_config = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#9ca3af'},
    'margin': dict(t=40, b=40, l=20, r=20)
}

# 2 Charts In 1 Row
r1c1, r1c2 = st.columns(2)
st.markdown("<br>", unsafe_allow_html=True)
r2c1, r2c2 = st.columns(2)
st.markdown("<br>", unsafe_allow_html=True)
r3c1, r3c2 = st.columns(2)

# ========================================
# 18. RENDER 6 PLOTLY CHARTS
# ========================================
if not filtered_df.empty:
    import plotly.express as px

    # 1. Chart (Row 1, Left): Revenue by Region
    with r1c1:
        rev_by_region = filtered_df.groupby('Region')['Total Revenue'].sum().reset_index()
        fig1 = px.bar(rev_by_region, x='Region', y='Total Revenue', title='💰 Total Revenue by Region', color_discrete_sequence=['#3b82f6'])
        fig1.update_layout(**chart_config)
        st.plotly_chart(fig1, use_container_width=True)

    # 2. Chart (Row 1, Right): Units Sold by Category
    with r1c2:
        units_by_cat = filtered_df.groupby('Category')['Units Sold'].sum().reset_index()
        fig2 = px.pie(units_by_cat, names='Category', values='Units Sold', title='📦 Units Sold by Category', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        fig2.update_layout(**chart_config)
        st.plotly_chart(fig2, use_container_width=True)

    # 3. Chart (Row 2, Left): Demand vs Inventory Level
    with r2c1:
        # Scatter plot 
        sample_df = filtered_df.head(2000) if len(filtered_df) > 2000 else filtered_df
        fig3 = px.scatter(sample_df, x='Inventory Level', y='Demand Forecast', color='Region', title='📈 Demand vs Inventory Level', opacity=0.7)
        fig3.update_layout(**chart_config)
        st.plotly_chart(fig3, use_container_width=True)

    # 4. Chart (Row 2, Right): Revenue over Time
    with r2c2:
        rev_over_time = filtered_df.groupby(filtered_df['Date'].dt.date)['Total Revenue'].sum().reset_index()
        fig4 = px.line(rev_over_time, x='Date', y='Total Revenue', title='📅 Revenue Trend (Timeline)', color_discrete_sequence=['#10b981'])
        fig4.update_layout(**chart_config)
        st.plotly_chart(fig4, use_container_width=True)

    # 5. Chart (Row 3, Left): Price vs Competitor Price
    with r3c1:
        price_comp = filtered_df.groupby('Category')[['Price', 'Competitor Pricing']].mean().reset_index()
        fig5 = px.bar(price_comp, x='Category', y=['Price', 'Competitor Pricing'], barmode='group', title='⚖️ Our Avg Price vs Competitor Pricing', color_discrete_sequence=['#3b82f6', '#ef4444'])
        fig5.update_layout(**chart_config)
        st.plotly_chart(fig5, use_container_width=True)

    # 6. Chart (Row 3, Right): Units Sold by Weather
    with r3c2:
        weather_impact = filtered_df.groupby('Weather Condition')['Units Sold'].sum().reset_index()
        fig6 = px.bar(weather_impact, x='Weather Condition', y='Units Sold', title='🌦️ Units Sold by Weather Condition', color_discrete_sequence=['#8b5cf6'])
        fig6.update_layout(**chart_config)
        st.plotly_chart(fig6, use_container_width=True)

else:
    st.warning("⚠️ No data available to display charts for the selected filters.")