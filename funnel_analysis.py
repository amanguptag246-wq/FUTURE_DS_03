import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. Load data
df = pd.read_csv("marketing_funnel_data.csv")

# 2. Funnel metrics calculation
total_visitors = len(df)
total_leads = df['is_lead'].sum()
total_mql = df['is_mql'].sum()
total_sql = df['is_sql'].sum()
total_opp = df['is_opp'].sum()
total_customers = df['is_customer'].sum()

funnel_df = pd.DataFrame({
    'Stage': ['Visitors', 'Leads', 'MQL', 'SQL', 'Opportunity', 'Customer'],
    'Count': [total_visitors, total_leads, total_mql, total_sql, total_opp, total_customers]
})

funnel_df['Conversion_Rate_%'] = (funnel_df['Count'] / funnel_df['Count'].shift(1) * 100).fillna(100).round(2)
funnel_df['Drop_off_%'] = (100 - funnel_df['Conversion_Rate_%']).round(2)

print("\n--- OVERALL FUNNEL PERFORMANCE ---")
print(funnel_df.to_string(index=False))

print("\n--- KEY SUMMARY KPIS ---")
print(f"Traffic-to-Lead Conversion Rate: {(total_leads / total_visitors * 100):.2f}%")
print(f"Lead-to-Customer Conversion Rate: {(total_customers / total_leads * 100):.2f}%")
print(f"Overall Visitor-to-Customer Rate: {(total_customers / total_visitors * 100):.2f}%")

# 3. Channel breakdown
channel_perf = df.groupby('channel').agg(
    Visitors=('lead_id', 'count'),
    Leads=('is_lead', 'sum'),
    Customers=('is_customer', 'sum'),
    Total_Spend=('cost_usd', 'sum')
).reset_index()

channel_perf['Lead_to_Customer_%'] = (channel_perf['Customers'] / channel_perf['Leads'] * 100).round(2)
channel_perf['CAC_USD'] = (channel_perf['Total_Spend'] / channel_perf['Customers']).round(2)

print("\n--- CHANNEL PERFORMANCE ---")
print(channel_perf.to_string(index=False))

# 4. Generate Interactive Funnel Chart HTML
fig = go.Figure(go.Funnel(
    y=funnel_df['Stage'],
    x=funnel_df['Count'],
    textinfo="value+percent previous"
))
fig.update_layout(title="Marketing & Sales Funnel Drop-off Analysis")
fig.write_html("funnel_chart.html")
print("\nInteractive Funnel Chart saved as 'funnel_chart.html'!")