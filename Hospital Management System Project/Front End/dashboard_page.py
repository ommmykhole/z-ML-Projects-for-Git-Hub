import streamlit as st
import pandas as pd
import requests
import datetime
import plotly.graph_objects as go

# ==========================================
# 1. API Fetch Function
# ==========================================
def fetch_appointments_data():
    try:
        response = requests.get("http://localhost:8000/appointments/?limit=10000")
        response.raise_for_status()
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            if not df.empty:
                df["appointment_date"] = pd.to_datetime(df["appointment_date"]).dt.date
            return df
        return pd.DataFrame()
    except Exception as e: 
        st.error(f"Error fetching appointments data: {e}")
        return pd.DataFrame()

# ==========================================
# 2. Main Dashboard Function
# ==========================================
def show_dashboard():
    st.title("📊 Hospital Management Dashboard")
    st.markdown("---")

    # Fetch Data
    raw_df = fetch_appointments_data()
    if raw_df.empty:
        st.warning("No Appointment data available.")
        return

    try:
        patients_df = pd.DataFrame(requests.get("http://localhost:8000/patients/?limit=10000").json())
    except:
        patients_df = pd.DataFrame()
        
    try:
        doctors_df = pd.DataFrame(requests.get("http://localhost:8000/doctors/?limit=10000").json())
    except:
        doctors_df = pd.DataFrame()
        
    try:
        billing_df = pd.DataFrame(requests.get("http://localhost:8000/billing/?limit=10000").json())
    except:
        billing_df = pd.DataFrame()

    # ==========================================
    # Step 1: Dynamic Filters & Reset Button
    # ==========================================
    st.markdown("#### 🎯 Dashboard Filters")
    if st.button("🔄 Reset All Filters"):
        st.session_state.clear()
        st.rerun()

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=30)
        selected_dates = st.date_input("Select Date Range", (start_date, today), key="date_filter")
         
    with filter_col2:
        doctor_list = ["All Doctors"] + list(raw_df['doctor_id'].unique())
        selected_doctor = st.selectbox("Select Doctor", doctor_list, key="doc_filter")
         
    with filter_col3:
        status_list = ["All"] + list(raw_df['status'].unique())
        selected_status = st.selectbox("Appointment Status", status_list, key="status_filter")

    # ==========================================
    # Step 2: Apply Filters (Masking)
    # ==========================================
    filtered_df = raw_df.copy()

    if len(selected_dates) == 2:
        start, end = selected_dates
        filtered_df = filtered_df[(filtered_df['appointment_date'] >= start) & 
                                  (filtered_df['appointment_date'] <= end)]

    if selected_doctor != "All Doctors":
        filtered_df = filtered_df[filtered_df['doctor_id'] == selected_doctor]

    if selected_status != "All":
        filtered_df = filtered_df[filtered_df['status'] == selected_status]

    st.markdown("---")

    # ==========================================
    # Step 3: Key Performance Indicators (KPIs)
    # ==========================================
    st.subheader("🏥 Key Performance Indicators")
    st.markdown("""
    <style>
    .kpi-card { background-color: #262730; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.2); border-bottom: 4px solid #00c0f2; transition: transform 0.3s; }
    .kpi-card:hover { transform: translateY(-5px); }
    .kpi-title { font-size: 14px; color: #fafafa; margin-bottom: 5px; font-weight: 500; white-space: nowrap; }
    .kpi-value { font-size: 22px; font-weight: bold; color: #00c0f2; }
    </style>
    """, unsafe_allow_html=True)

    total_appts = len(filtered_df)
    real_total_patients = len(patients_df) if not patients_df.empty else 0
    real_active_doctors = len(doctors_df) if not doctors_df.empty else 0
    
    if not billing_df.empty:
        real_total_revenue = f"₹ {billing_df['amount'].sum():,.0f}" 
        pending_df = billing_df[billing_df['payment_status'] == 'Pending']
        real_pending_payments = f"₹ {pending_df['amount'].sum():,.0f}"
        real_avg_fee = f"₹ {billing_df['amount'].mean():,.0f}"
    else:
        real_total_revenue = "₹ 0"
        real_pending_payments = "₹ 0"
        real_avg_fee = "₹ 0"

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.markdown(f'<div class="kpi-card"><div class="kpi-title">🧑‍🤝‍🧑 Total Patients</div><div class="kpi-value">{real_total_patients}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi-card"><div class="kpi-title">📅 Total Appts</div><div class="kpi-value">{total_appts}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi-card"><div class="kpi-title">💰 Total Revenue</div><div class="kpi-value">{real_total_revenue}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi-card"><div class="kpi-title">⏳ Pending Bill</div><div class="kpi-value">{real_pending_payments}</div></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="kpi-card"><div class="kpi-title">👨‍⚕️ Active Doctors</div><div class="kpi-value">{real_active_doctors}</div></div>', unsafe_allow_html=True)
    c6.markdown(f'<div class="kpi-card"><div class="kpi-title">🩺 Avg Consult Fee</div><div class="kpi-value">{real_avg_fee}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ==========================================
    # Step 4: Plotly Interactive Charts
    # ==========================================
    st.subheader("📈 Detailed Analysis")
    
    if filtered_df.empty:
        st.info("No data available for the selected filters.")
        return

    trend_df = filtered_df.groupby('appointment_date').size().reset_index(name='count')
    doc_workload = filtered_df.groupby('doctor_id').size().reset_index(name='count').sort_values('count', ascending=True)
    status_counts = filtered_df.groupby('status').size().reset_index(name='count')

    if not patients_df.empty:
        filtered_patients = patients_df[patients_df['patient_id'].isin(filtered_df['patient_id'])]
        gender_counts = filtered_patients.groupby('gender').size().reset_index(name='count')
    else:
        gender_counts = pd.DataFrame(columns=['gender', 'count'])

    if not billing_df.empty:
        filtered_billing = billing_df[billing_df['appointment_id'].isin(filtered_df['appointment_id'])].copy()
        filtered_billing['bill_date'] = pd.to_datetime(filtered_billing['bill_date']).dt.date
        payment_trend = filtered_billing.groupby(['bill_date', 'payment_status'])['amount'].sum().reset_index()
    else:
        payment_trend = pd.DataFrame(columns=['bill_date', 'payment_status', 'amount'])

    chart_col1, chart_col2 = st.columns(2)
    chart_col3, chart_col4 = st.columns(2)
    chart_col5, chart_col6 = st.columns(2)

    with chart_col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=trend_df['appointment_date'], y=trend_df['count'], mode='lines+markers', line=dict(color='#00c0f2', width=3)))
        fig1.update_layout(title="1. Appointment Trend", template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=trend_df['appointment_date'], y=trend_df['count'], marker_color='#7367f0'))
        fig2.update_layout(title="2. Appointments Over Time", template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    with chart_col3:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=doc_workload['count'], y=doc_workload['doctor_id'], orientation='h', marker_color='#ff9f43'))
        fig3.update_layout(title="3. Doctors Workload", template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig3, use_container_width=True)

    with chart_col4:
        fig4 = go.Figure()
        fig4.add_trace(go.Pie(labels=status_counts['status'], values=status_counts['count'], hole=0.5, marker=dict(colors=['#28c76f', '#ea5455', '#ff9f43', '#00cfe8'])))
        fig4.update_layout(title="4. Appointment Status", template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig4, use_container_width=True)

    with chart_col5:
        fig5 = go.Figure()
        if not gender_counts.empty:
            fig5.add_trace(go.Pie(labels=gender_counts['gender'], values=gender_counts['count'], marker=dict(colors=['#00c0f2', '#ea5455'])))
        fig5.update_layout(title="5. Patient Demographics", template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig5, use_container_width=True)

    with chart_col6:
        fig6 = go.Figure()
        if not payment_trend.empty:
            for status in payment_trend['payment_status'].unique():
                subset = payment_trend[payment_trend['payment_status'] == status]
                fig6.add_trace(go.Bar(x=subset['bill_date'], y=subset['amount'], name=status))
        fig6.update_layout(title="6. Payment Breakdown", barmode='stack', template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig6, use_container_width=True)