import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Data Load & Preprocessing
df = pd.read_csv('index_1.csv')
df['date'] = pd.to_datetime(df['date'])

# 2. Aggregating Data for Visuals
daily_revenue = df.groupby('date')['money'].sum().reset_index()
coffee_counts = df['coffee_name'].value_counts().reset_index()
coffee_counts.columns = ['coffee_name', 'count']
payment_types = df['cash_type'].value_counts().reset_index()
payment_types.columns = ['cash_type', 'count']
revenue_by_coffee = df.groupby('coffee_name')['money'].sum().reset_index().sort_values(by='money', ascending=False)

# 3. Dashboard Layout (2x2 Grid)
# Pie chart sathi 'domain' type use karava lagto
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "xy"}, {"type": "xy"}],
           [{"type": "domain"}, {"type": "xy"}]],    
    subplot_titles=("Daily Revenue Trend", "Most Popular Coffees", 
                    "Payment Method Breakdown", "Revenue by Coffee Type")
)

# Trace 1: Daily Revenue (Line Chart)
fig.add_trace(
    go.Scatter(x=daily_revenue['date'], y=daily_revenue['money'], 
               mode='lines+markers', name="Revenue", marker_color='indigo'),
    row=1, col=1
)

# Trace 2: Most Popular Coffees (Bar Chart)
fig.add_trace(
    go.Bar(x=coffee_counts['coffee_name'], y=coffee_counts['count'], 
           name="Orders", marker_color='teal'),
    row=1, col=2
)

# Trace 3: Payment Method (Donut Chart)
fig.add_trace(
    go.Pie(labels=payment_types['cash_type'], values=payment_types['count'], 
           hole=0.4, name="Payment"),
    row=2, col=1
)

# Trace 4: Revenue by Coffee Type (Bar Chart)
fig.add_trace(
    go.Bar(x=revenue_by_coffee['coffee_name'], y=revenue_by_coffee['money'], 
           name="Total Revenue", marker_color='coral'),
    row=2, col=2
)

# 4. Dashboard Styling
fig.update_layout(
    title_text="☕ Coffee Sales Analytics Dashboard",
    title_x=0.5,
    title_font=dict(size=24),
    height=800,
    showlegend=False,
    template="plotly_white", # Tu 'plotly_dark' pan try karu shaktos
    hovermode="x unified"
)

# 5. Render
fig.show()