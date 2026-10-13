import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Retail Sales Dashboard",
    layout="wide"
)

st.title("Retail Sales Analytics Dashboard")
st.caption("Business Intelligence | Sales Performance Analysis")


# ==========================================
# 2. FILE UPLOADER
# ==========================================

uploaded_file = st.file_uploader(
    "Upload Your Retail Sales CSV",
    type=["csv"]
)


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # ======================================
    # 3. DATA VALIDATION
    # ======================================

    required_columns = [
        "Transaction ID",
        "Date",
        "Customer ID",
        "Gender",
        "Age",
        "Product Category",
        "Quantity",
        "Price per Unit",
        "Total Amount"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        st.error(
            f"Missing columns in CSV: {missing_columns}"
        )

        st.stop()

    if df.empty:
        st.warning("Uploaded CSV is empty.")
        st.stop()

    # ======================================
    # 4. DATA PREPROCESSING
    # ======================================

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    numeric_columns = [
        "Age",
        "Quantity",
        "Price per Unit",
        "Total Amount"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df = df.dropna(
        subset=["Date", "Total Amount"]
    )

    if df.empty:
        st.warning("No valid records available.")
        st.stop()

    # ======================================
    # 5. SIDEBAR FILTERS
    # ======================================

    st.sidebar.header("Dashboard Filters")

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    selected_genders = st.sidebar.multiselect(
        "Select Gender",
        options=sorted(
            df["Gender"].dropna().unique().tolist()
        ),
        default=sorted(
            df["Gender"].dropna().unique().tolist()
        )
    )

    selected_categories = st.sidebar.multiselect(
        "Select Product Category",
        options=sorted(
            df["Product Category"]
            .dropna()
            .unique()
            .tolist()
        ),
        default=sorted(
            df["Product Category"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    if df["Age"].notna().any():

        min_age = int(df["Age"].min())
        max_age = int(df["Age"].max())

        if min_age < max_age:

            age_range = st.sidebar.slider(
                "Select Age Range",
                min_value=min_age,
                max_value=max_age,
                value=(min_age, max_age)
            )

        else:
            age_range = (min_age, max_age)

    else:
        age_range = None

    if df["Quantity"].notna().any():

        min_quantity = int(df["Quantity"].min())
        max_quantity = int(df["Quantity"].max())

        if min_quantity < max_quantity:

            quantity_range = st.sidebar.slider(
                "Select Quantity Range",
                min_value=min_quantity,
                max_value=max_quantity,
                value=(min_quantity, max_quantity)
            )

        else:
            quantity_range = (
                min_quantity,
                max_quantity
            )

    else:
        quantity_range = None

    # ======================================
    # 6. APPLY FILTERS
    # ======================================

    filtered_df = df.copy()

    # Date filter

    if len(date_range) == 2:

        start_date, end_date = date_range

        filtered_df = filtered_df[
            (filtered_df["Date"].dt.date >= start_date)
            &
            (filtered_df["Date"].dt.date <= end_date)
        ]

    # Gender filter

    filtered_df = filtered_df[
        filtered_df["Gender"].isin(selected_genders)
    ]

    # Category filter

    filtered_df = filtered_df[
        filtered_df["Product Category"].isin(
            selected_categories
        )
    ]

    # Age filter

    if age_range is not None:

        filtered_df = filtered_df[
            filtered_df["Age"].between(
                age_range[0],
                age_range[1]
            )
        ]

    # Quantity filter

    if quantity_range is not None:

        filtered_df = filtered_df[
            filtered_df["Quantity"].between(
                quantity_range[0],
                quantity_range[1]
            )
        ]

    # ======================================
    # 7. DYNAMIC KPI CARDS
    # ======================================

    st.subheader("Business Performance")

    total_sales = filtered_df["Total Amount"].sum()

    total_transactions = (
        filtered_df["Transaction ID"].nunique()
    )

    total_customers = (
        filtered_df["Customer ID"].nunique()
    )

    total_quantity = filtered_df["Quantity"].sum()

    average_transaction = (
        filtered_df.groupby("Transaction ID")[
            "Total Amount"
        ].sum().mean()
    )

    average_transaction = (
        average_transaction
        if pd.notna(average_transaction)
        else 0
    )

    total_records = len(filtered_df)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Sales",
        f"₹{total_sales:,.2f}"
    )

    col2.metric(
        "Total Transactions",
        f"{total_transactions:,}"
    )

    col3.metric(
        "Unique Customers",
        f"{total_customers:,}"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Total Quantity Sold",
        f"{total_quantity:,.0f}"
    )

    col5.metric(
        "Average Transaction Value",
        f"₹{average_transaction:,.2f}"
    )

    col6.metric(
        "Total Records",
        f"{total_records:,}"
    )

    st.divider()

    # ======================================
    # 8. CHECK FILTERED DATA
    # ======================================

    if filtered_df.empty:

        st.warning(
            "No data available for the selected filters."
        )

        st.stop()

    # ======================================
    # 9. SALES TREND CHART
    # ======================================

    st.subheader("Sales Trend")

    sales_trend = (
    filtered_df
    .groupby(filtered_df["Date"].dt.date)["Total Amount"]
    .sum()
    .reset_index()
)

    sales_trend.columns = ["Date", "Total Sales"]

    fig_trend = px.line(
        sales_trend,
        x="Date",
        y="Total Sales",
        markers=True,
        title="Daily Sales Performance"
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

    # ======================================
    # 10. CATEGORY-WISE SALES
    # ======================================

    st.subheader("Category Performance")

    category_sales = (
        filtered_df.groupby(
            "Product Category",
            as_index=False
        )["Total Amount"]
        .sum()
        .sort_values(
            "Total Amount",
            ascending=False
        )
    )

    fig_category = px.bar(
        category_sales,
        x="Product Category",
        y="Total Amount",
        title="Sales by Product Category",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

    # ======================================
    # 11. GENDER-WISE SALES
    # ======================================

    st.subheader("Gender Analysis")

    gender_sales = (
        filtered_df.groupby(
            "Gender",
            as_index=False
        )["Total Amount"]
        .sum()
    )

    fig_gender = px.pie(
        gender_sales,
        names="Gender",
        values="Total Amount",
        title="Sales Distribution by Gender",
        hole=0.45
    )

    st.plotly_chart(
        fig_gender,
        use_container_width=True
    )

    # ======================================
    # 12. PRODUCT QUANTITY ANALYSIS
    # ======================================

    st.subheader("Product Quantity Analysis")

    quantity_sales = (
        filtered_df.groupby(
            "Product Category",
            as_index=False
        )["Quantity"]
        .sum()
        .sort_values(
            "Quantity",
            ascending=False
        )
    )

    fig_quantity = px.bar(
        quantity_sales,
        x="Product Category",
        y="Quantity",
        title="Quantity Sold by Category"
    )

    st.plotly_chart(
        fig_quantity,
        use_container_width=True
    )

    # ======================================
    # 13. CUSTOMER AGE ANALYSIS
    # ======================================

    st.subheader("Customer Age Analysis")

    age_data = filtered_df.dropna(
        subset=["Age"]
    )

    if not age_data.empty:

        fig_age = px.histogram(
            age_data,
            x="Age",
            nbins=15,
            title="Customer Age Distribution"
        )

        st.plotly_chart(
            fig_age,
            use_container_width=True
        )

    # ======================================
    # 14. DATA TABLE
    # ======================================

    st.subheader("Filtered Transaction Data")

    st.caption(
        f"Showing {len(filtered_df):,} records "
        f"out of {len(df):,} valid records."
    )

    with st.expander("View Filtered Dataset"):

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

    # ======================================
    # 15. DOWNLOAD FILTERED DATA
    # ======================================

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Filtered CSV",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Please upload your Retail Sales CSV "
        "to explore the dashboard."
    )