import pandas as pd
import numpy as np
from scipy.stats import wilcoxon, norm
import sys

def wilcoxon_effect_size(csv1, csv2, column_name, alpha=0.05):
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)
    
    x = df1[column_name].values
    y = df2[column_name].values
    
    if len(x) != len(y):
        raise ValueError("Both files must have the same number of observations.")
    
    stat, p_value = wilcoxon(x, y)
    
    N = len(x)  # Number of pairs
    z = norm.ppf(1 - p_value / 2)  # Approximate Z-score
    r = z / np.sqrt(N)
    
    significance = "Significant" if p_value < alpha else "Not Significant"
    
    if r < 0.1:
        effect_size_desc = "Negligible"
    elif r < 0.3:
        effect_size_desc = "Small"
    elif r < 0.5:
        effect_size_desc = "Medium"
    else:
        effect_size_desc = "Large"

    print(f"Wilcoxon Statistic: {stat:.4f}")
    print(f"p-value: {p_value:.4e} ({significance})")
    print(f"Effect Size (r): {r:.4f} ({effect_size_desc})")
    
    return {"Wilcoxon Statistic": stat, "p-value": p_value, "Effect Size (r)": r, "Significance": significance, "Effect Size Description": effect_size_desc}

# file1 = sys.argv[1]
# file2 = sys.argv[2]
column = sys.argv[1] # Top-10
metric = sys.argv[2] # average-precision, reciprocal-rank
typ = sys.argv[3] # clean, baseline

projects = ["aspectj", "birt", "eclipse", "jdt", "swt", "tomcat"]
techniques = ["buglocator", "bluir", "vsm", "brtracer"]

for project in projects:
    for i in range(len(techniques)):
        for j in range(i+1, len(techniques)):
            file1 = f"{techniques[i]}/{project}-{typ}-{metric}.csv"
            file2 = f"{techniques[j]}/{project}-{typ}-{metric}.csv"

            id = f"{project}-{techniques[i]}-{techniques[j]}-{metric}-{typ}-{column}"
            result = wilcoxon_effect_size(file1, file2, column)

            print(" ***** ")
            print(id, result)
            print()