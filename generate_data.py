import pandas as pd
import numpy as np

np.random.seed(42)
n_records = 5000

channels = ['Google Ads', 'Meta Ads', 'Organic Search', 'LinkedIn', 'Email Marketing']
campaigns = ['Brand_Awareness', 'Lead_Gen_Q1', 'Retargeting_Promo', 'Product_Webinar']
channel_weights = [0.35, 0.25, 0.20, 0.12, 0.08]

data = []
for i in range(1, n_records + 1):
    lead_id = f"LEAD_{i:05d}"
    channel = np.random.choice(channels, p=channel_weights)
    campaign = np.random.choice(campaigns)
    
    qual_boost = 0.15 if channel in ['LinkedIn', 'Organic Search'] else 0.05
    
    is_lead = np.random.rand() < 0.35
    is_mql = is_lead and (np.random.rand() < (0.45 + qual_boost))
    is_sql = is_mql and (np.random.rand() < (0.40 + qual_boost))
    is_opp = is_sql and (np.random.rand() < 0.50)
    is_customer = is_opp and (np.random.rand() < 0.45)
    
    stage = "Visitor"
    if is_customer:
        stage = "Customer"
    elif is_opp:
        stage = "Opportunity"
    elif is_sql:
        stage = "SQL"
    elif is_mql:
        stage = "MQL"
    elif is_lead:
        stage = "Lead"
        
    spend = round(np.random.uniform(5, 50), 2) if channel in ['Google Ads', 'Meta Ads', 'LinkedIn'] else 0.0
    
    data.append({
        "lead_id": lead_id,
        "channel": channel,
        "campaign": campaign,
        "stage": stage,
        "is_lead": int(is_lead),
        "is_mql": int(is_mql),
        "is_sql": int(is_sql),
        "is_opp": int(is_opp),
        "is_customer": int(is_customer),
        "cost_usd": spend
    })

df = pd.DataFrame(data)
df.to_csv("marketing_funnel_data.csv", index=False)
print("Dataset created: marketing_funnel_data.csv successfully generated!")