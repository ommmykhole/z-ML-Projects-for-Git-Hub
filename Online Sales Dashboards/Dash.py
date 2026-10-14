import streamlit as st 
import pandas as pd 
import plotly.graph_objects as go


st.set_page_config(
    layout='wide',
    page_title="Online Sales Dashboard"
)



df = pd.read_csv("Details.csv")




st.sidebar.title("Business Analysis Dashboard")

st.sidebar.write("Dashboard Filters")


st.sidebar.selectbox(
    "Category Filter",
    [
        "Clothing",
        "Electronics",
        "Furniture"
    ],
    key="Category_key"
)


st.sidebar.selectbox(
    "Payment Methods",
    [
        "COD",
        "Credit Card",
        "Debit Card",
        "EMI",
        "UPI"
    ],
    key="Payment_key"
)




st.sidebar.slider(
    "Amount Range",
    min_value=4,
    max_value=5750,
    value=100
)



st.sidebar.slider(
    "Profit Range",
    min_value=-1981,
    max_value=1864,
    value=500
)



st.header("Online Sales Analysis Dashboard")



st.divider()
st.subheader("KPI Cards")
st.caption("All Important Business KPI Cards | Dynamic KPI Cards")



col1,col2,col3,col4,col5,col6 = st.columns(
    6,
    border=True,
    vertical_alignment="center"
)



with col1:
    st.metric("Total Sales",df["Amount"].sum())
    
with col2:
    st.metric("Total Customers",df["Order ID"].nunique())
    
with col3:
    st.metric("Max Sales",df["Amount"].max())
    
with col4:
    st.metric("All Over Profit",df["Profit"].sum())
    
with col5:
    st.metric("Average Profit",df["Profit"].mean())
    
with col6:
    st.metric("All Products", df["Sub-Category"].nunique())
    
    

st.divider()
st.subheader("All Charts Visuals")


#Chart 1
category_wise_profit = df.groupby("Category")["Profit"].sum()

fig1  = go.Figure()

fig1.add_trace(
     go.Bar(
            x=category_wise_profit.index,
            y=category_wise_profit.values
        )
)

fig1.update_traces(
    texttemplate="%{y}",
    textposition="outside",
    marker_line_width=1
)

fig1.update_layout(
    title="Category Wise Profit",
    xaxis_title="Category",
    yaxis_title="Total Profit",
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
        
    font=dict(
        family="Arial",
        size=13,
        color="#F9FAFB"
    ),
    margin=dict(l=20, r=20, t=60, b=20)
    
)





# Chart 2 

Income_From_Payment_Mode = df.groupby("PaymentMode")["Amount"].sum()




fig2 = go.Figure()

fig2.add_trace(
    go.Pie(
        labels=Income_From_Payment_Mode.index,
        values=Income_From_Payment_Mode.values
        
    )
)


fig2.update_layout(
    title="Income From Payment Mode",
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
    
    font=dict(
        family="Arial",
        size=13,
        color="#F9FAFB"
    ),
    margin=dict(l=20, r=20, t=60, b=20)
)

fig2.update_traces(
    texttemplate="%{y}",
    textposition="outside",
    marker_line_width=1
)








#Chart3


top_5_products = (
    df.groupby("Sub-Category")["Profit"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
)



fig3 = go.Figure()

fig3.add_trace(
    go.Bar(
        x=top_5_products.index,
        y=top_5_products.values
    )
)


fig3.update_layout(
    title="Top 5 Profitable Products",
    xaxis_title = "Products",
    yaxis_title = "Profit",
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
        
    font=dict(
        family="Arial",
        size=13,
        color="#F9FAFB"
    ),
    margin=dict(l=20, r=20, t=60, b=20)
)


fig3.update_traces(
    texttemplate="%{y}",
    textposition="outside",
    marker_line_width=1
)












#Chart 4


category_wise_Sales = df.groupby("Category")["Amount"].sum()




fig4 = go.Figure()

fig4.add_trace(
    go.Pie(
        labels=category_wise_Sales.index,
        values=category_wise_Sales.values,
        hole=0.6
    )
)


fig4.update_layout(
    title="Category Wise Sales",
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
            
    font=dict(
        family="Arial",
        size=13,
        color="#F9FAFB"
    ),
    margin=dict(l=20, r=20, t=60, b=20)
)


fig4.update_traces(
    texttemplate="%{y}",
    textposition="inside",
    marker_line_width=1
)







#Chart 5 

Product_Quantity = df.groupby("Sub-Category")["Quantity"].sum()



fig5 = go.Figure()


fig5.add_trace(
    go.Funnel(
        x=Product_Quantity.values,
        y=Product_Quantity.index
    )
)


fig5.update_layout(
    title="Product And Their Quantity",
    xaxis_title="Products",
    yaxis_title="Quantity",
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
                
    font=dict(
        family="Arial",
        size=13,
        color="#F9FAFB"
    ),
    margin=dict(l=20, r=20, t=60, b=20)
    
)


fig5.update_traces(
    texttemplate="%{y}",
    textposition="outside",
    marker_line_width=1
)










#Chart 6



cat_profit_sales = df.groupby("Category")[["Profit","Amount"]].sum()



fig6 = go.Figure()

fig6.add_trace(
    go.Bar(
        x=cat_profit_sales.index,
        y=cat_profit_sales["Profit"],
        name="Profit"
    )
)

fig6.add_trace(
    go.Bar(
        x=cat_profit_sales.index,
        y=cat_profit_sales["Amount"],
        name="Sales"
    )
)

fig6.update_layout(
    title="Category-wise Sales vs Profit",
    barmode="group",
    xaxis_title="Category",
    yaxis_title="Sales And Profit",
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
                    
    font=dict(
        family="Arial",
        size=13,
        color="#F9FAFB"
    ),
    margin=dict(l=20, r=20, t=60, b=20)
)


fig6.update_traces(
    texttemplate="%{y}",
    textposition="outside",
    marker_line_width=1
)













# Streamlit Intigration



col1,col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1,use_container_width=True)
    

with col2:
    st.plotly_chart(fig2,use_container_width=True)







col1,col2 = st.columns(2)

with col1:
    st.plotly_chart(fig3,use_container_width=True)

with col2:
    st.plotly_chart(fig4,use_container_width=True)





col1,col2 = st.columns(2)

with col1:
    st.plotly_chart(fig5,use_container_width=True)

with col2:
    st.plotly_chart(fig6,use_container_width=True)