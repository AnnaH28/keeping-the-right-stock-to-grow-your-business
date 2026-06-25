import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Optimizing Inventory Turnover and Profit Margins: A Comprehensive Business Overview for Small Retailers", layout="wide")
st.title("Optimizing Inventory Turnover and Profit Margins: A Comprehensive Business Overview for Small Retailers")
# CSS tạo phong cách Minimalist (sang trọng)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 2px 2px 5px #f0f0f0; }
    h1 { color: #1a1a1a; }
    </style>
""", unsafe_allow_html=True)

st.title("Inventory Management & Profit Optimization")

# --- PHẦN KHỞI TẠO DỮ LIỆU (GIỮ NGUYÊN) ---
if 'df' not in st.session_state:
    data = {
        "Product Name": ["Croptop A", "Linen Top", "Bikini", "Denim Shorts", "Tote Bag"],
        "Quantity": [1000, 600, 500, 800, 300],
        "Price ($)": [24.0, 30.0, 70.0, 35.0, 31.67],
        "COGS ($)": [14400.0, 12600.0, 15750.0, 14000.0, 5700.0],
        "Beginning Inv ($)": [1200.0, 900.0, 2200.0, 3100.0, 1900.0],
        "Ending Inv ($)": [1000.0, 1100.0, 2800.0, 2900.0, 2100.0]
    }
    st.session_state.df = pd.DataFrame(data)

# --- PHẦN TÍNH TOÁN (GIỮ NGUYÊN) ---
edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
df = edited_df.copy()
df["Revenue ($)"] = df["Quantity"] * df["Price ($)"]
df["Average Inv ($)"] = (df["Beginning Inv ($)"] + df["Ending Inv ($)"]) / 2
df["Gross Profit ($)"] = df["Revenue ($)"] - df["COGS ($)"]
df["Gross Margin (%)"] = (df["Gross Profit ($)"] / df["Revenue ($)"]) * 100
df["Inventory Turnover (IT)"] = df["COGS ($)"] / df["Average Inv ($)"]
df["DIO (Days)"] = 365 / df["Inventory Turnover (IT)"]

shop_it_baseline = df["Inventory Turnover (IT)"].median() if not df.empty else 0
shop_margin_baseline = df["Gross Margin (%)"].median() if not df.empty else 0

def generate_insights(row):
    it = row["Inventory Turnover (IT)"]
    margin = row["Gross Margin (%)"]
    if it >= shop_it_baseline and margin >= shop_margin_baseline: return "Optimal Efficiency"
    elif it >= shop_it_baseline and margin < shop_margin_baseline: return "Volume Trap"
    elif it < shop_it_baseline and margin >= shop_margin_baseline: return "Capital Tie-up"
    else: return "Operational Failure"

df["Strategic Quadrant"] = df.apply(generate_insights, axis=1)

# --- TẠO CẤU TRÚC 4 TAB (VÒNG TRÒN DỊCH VỤ) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Research","Metrics", "Matrix", "Strategies", "Inventory Planner"])

with tab1:
    st.subheader("Data Input")
    st.write("Dữ liệu được nhập và quản lý thông qua bảng ở phía trên.")

with tab2:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Gross Margin",
        f"{df['Gross Margin (%)'].mean():.1f}%"
    )

    col2.metric(
        "Average Inventory Turnover",
        f"{df['Inventory Turnover (IT)'].mean():.2f}"
    )

    col3.metric(
        "Average DIO",
        f"{df['DIO (Days)'].mean():.1f} days"
    )

    fig_metrics = px.bar(
        df,
        x="Product Name",
        y=[
            "Gross Margin (%)",
            "Inventory Turnover (IT)",
            "DIO (Days)"
        ],
        barmode="group",
        title="Inventory Performance Dashboard"
    )

    st.plotly_chart(fig_metrics, use_container_width=True)
    st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("Portfolio Matrix")

    fig = px.scatter(
        df,
        x="Inventory Turnover (IT)",
        y="Gross Margin (%)",
        size="Revenue ($)",
        color="Strategic Quadrant",
        hover_name="Product Name",
        title="Inventory Turnover vs Gross Margin Portfolio Matrix"
    )

    fig.add_vline(
        x=shop_it_baseline,
        line_dash="dash",
        annotation_text="Median Inventory Turnover"
    )

    fig.add_hline(
        y=shop_margin_baseline,
        line_dash="dash",
        annotation_text="Median Gross Margin"
    )

    fig.update_layout(
        xaxis_title="Inventory Turnover (IT)",
        yaxis_title="Gross Margin (%)"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Strategic Recommendations")
    strategy_data = {
        "Quadrant": ["Optimal Efficiency", "Volume Trap", "Capital Tie-up", "Operational Failure"],
        "Insight": ["Peak Performance", "Thin Margins", "High Stagnation", "Low Sustainability"],
        "Action Plan": ["Scale Up", "Reduce COGS", "Promote/Bundle", "Liquidate"]
    }
    st.table(pd.DataFrame(strategy_data))
    
    with st.expander("Detailed Management Insights"):
        st.write("""
        - **Optimal Efficiency**: Maintain current inventory levels; prioritize supply chain consistency.
        - **Volume Trap**: Focus on 'Value Engineering'. Audit logistics costs and seek volume-based supplier discounts.
        - **Capital Tie-up**: High margin is good, but cash flow is frozen. Use 'Pull' marketing strategies.
        - **Operational Failure**: The product is a liability. Cut losses, liquidate, or pivot the pricing model immediately.
        """)
with tab5:
    st.subheader("How Much Inventory Should the Business Order?")

    st.write("This section helps estimate the minimum quantity needed to cover operating expenses and achieve a target profit.")

    col1, col2, col3 = st.columns(3)

    with col1:
        selling_price = st.number_input("Selling Price per Unit ($)", min_value=0.0, value=40.0, step=1.0)
        unit_cost = st.number_input("Unit Cost / COGS per Unit ($)", min_value=0.0, value=18.0, step=1.0)

    with col2:
        operating_expenses = st.number_input("Monthly Operating Expenses ($)", min_value=0.0, value=2000.0, step=100.0)
        target_profit = st.number_input("Target Monthly Profit ($)", min_value=0.0, value=1000.0, step=100.0)

    with col3:
        unsold_rate = st.slider("Estimated Unsold Inventory Rate (%)", 0, 50, 10)

    gross_profit_per_unit = selling_price - unit_cost

    if gross_profit_per_unit <= 0:
        st.error("Selling price must be higher than unit cost to generate profit.")
    else:
        break_even_units = operating_expenses / gross_profit_per_unit
        target_units_sold = (operating_expenses + target_profit) / gross_profit_per_unit
        recommended_order_qty = target_units_sold / (1 - unsold_rate / 100)

        st.markdown("### Key Results")

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        kpi1.metric("Gross Profit per Unit", f"${gross_profit_per_unit:,.2f}")
        kpi2.metric("Break-even Quantity", f"{break_even_units:,.0f} units")
        kpi3.metric("Units Needed for Target Profit", f"{target_units_sold:,.0f} units")
        kpi4.metric("Recommended Order Quantity", f"{recommended_order_qty:,.0f} units")

        st.info(f"""
        To cover monthly operating expenses of **${operating_expenses:,.0f}** and earn a target profit of 
        **${target_profit:,.0f}**, the business should sell about **{target_units_sold:,.0f} units**.

        Considering an estimated unsold inventory rate of **{unsold_rate}%**, the recommended order quantity is 
        approximately **{recommended_order_qty:,.0f} units**.
        """)

        scenario_df = pd.DataFrame({
            "Scenario": ["Conservative", "Recommended", "Growth"],
            "Order Quantity": [
                recommended_order_qty * 0.85,
                recommended_order_qty,
                recommended_order_qty * 1.20
            ]
        })

        scenario_df["Expected Sold Units"] = scenario_df["Order Quantity"] * (1 - unsold_rate / 100)
        scenario_df["Revenue ($)"] = scenario_df["Expected Sold Units"] * selling_price
        scenario_df["COGS ($)"] = scenario_df["Order Quantity"] * unit_cost
        scenario_df["Gross Profit ($)"] = scenario_df["Revenue ($)"] - scenario_df["COGS ($)"]
        scenario_df["Net Profit After Operating Expenses ($)"] = scenario_df["Gross Profit ($)"] - operating_expenses

        st.markdown("### Scenario Analysis")
        st.dataframe(scenario_df, use_container_width=True)

        fig_order = px.bar(
            scenario_df,
            x="Scenario",
            y="Net Profit After Operating Expenses ($)",
            color="Scenario",
            title="Projected Net Profit by Order Quantity Scenario"
        )

        st.plotly_chart(fig_order, use_container_width=True)