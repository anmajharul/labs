
import pandas as pd
from scipy.stats import mannwhitneyu

DATA_PATH = "data/chapter4_raw.csv"
GENDER_COL = "Gender"

OUTCOMES = {
    "Security_Harassment": "security_harassment",
    "Reliability": "reliability",
    "Road_Accidents": "road_accidents",
    "Comfort": "comfort",
    "Crowding": "crowding",
}

df = pd.read_csv(DATA_PATH)
rows = []

for label, col in OUTCOMES.items():
    d = df[[GENDER_COL, col]].dropna()
    male = d.loc[d[GENDER_COL] == 1, col]
    female = d.loc[d[GENDER_COL] == 2, col]

    res = mannwhitneyu(male, female, alternative="two-sided",
                       method="asymptotic", use_continuity=True)

    U1 = float(res.statistic)
    U2 = len(male)*len(female) - U1
    U = min(U1, U2)

    rows.append({
        "Outcome": label,
        "Male_N": len(male),
        "Female_N": len(female),
        "Male_Mean": male.mean(),
        "Male_Median": male.median(),
        "Female_Mean": female.mean(),
        "Female_Median": female.median(),
        "U1_Male": U1,
        "U2_Female": U2,
        "U_reported": U,
        "p_value": res.pvalue,
        "Significant_alpha_0.05": res.pvalue < 0.05
    })

result = pd.DataFrame(rows)
print(result.to_string(index=False))
result.to_csv("outputs/mann_whitney_table4_4_python.csv", index=False)
