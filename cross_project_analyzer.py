import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from scipy.stats import wilcoxon, norm

# def wilcoxon_effect_size(csv1, csv2, column_name, alpha=0.05):
#     df1 = pd.read_csv(csv1)
#     df2 = pd.read_csv(csv2)
    
#     x = df1[column_name].values
#     y = df2[column_name].values
    
#     if len(x) != len(y):
#         raise ValueError("Both files must have the same number of observations.")
    
#     stat, p_value = wilcoxon(x, y)
    
#     N = len(x)  # Number of pairs
#     z = norm.ppf(1 - p_value / 2)  # Approximate Z-score
#     r = z / np.sqrt(N)
    
#     significance = "Significant" if p_value < alpha else "Not Significant"
    
#     if r < 0.1:
#         effect_size_desc = "Negligible"
#     elif r < 0.3:
#         effect_size_desc = "Small"
#     elif r < 0.5:
#         effect_size_desc = "Medium"
#     else:
#         effect_size_desc = "Large"

#     return {"Wilcoxon Statistic": stat, "p-value": p_value, "Effect Size (r)": r, "Significance": significance, "Effect Size Description": effect_size_desc}

# file1 = sys.argv[1]

def wilcoxon_effect_size(csv1, csv2, column_name, alpha=0.05):
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)
    
    x = df1[column_name].values
    y = df2[column_name].values
    
    if len(x) != len(y):
        return None  # Skip if sizes mismatch
    
    stat, p_value = wilcoxon(x, y)
    
    N = len(x)
    if p_value == 0:
        p_value = 1e-10  # Avoid log(0) errors
    
    z = norm.ppf(1 - p_value / 2)  
    r = z / np.sqrt(N)  # Effect size
    
    # Convert numerical effect size to categorical
    if r < 0.1:
        return 'negligible'
    elif r < 0.3:
        return 'small'
    elif r < 0.5:
        return 'medium'
    else:
        return 'large'

column = sys.argv[1]  # Top-10
metric = sys.argv[2]  # average-precision, reciprocal-rank
typ = sys.argv[3]  # clean, baseline

projects = ["aspectj", "birt", "eclipse", "jdt", "swt", "tomcat"]
techniques = ["buglocator", "bluir", "vsm", "brtracer"]

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle(f"Effect Size Heatmaps: {metric} ({typ})", fontsize=16)

# Define categorical color mapping
color_map = {
    'negligible': 0.25,
    'small': 0.5,
    'medium': 0.75,
    'large': 1.0
}

for idx, project in enumerate(projects):
    row, col = divmod(idx, 3)  # Compute subplot position

    # Initialize DataFrame for the current project
    comparison_matrix = pd.DataFrame(index=techniques, columns=techniques, dtype=str)

    for i in range(len(techniques)):
        for j in range(i+1, len(techniques)):
            file1 = f"{techniques[i]}/{project}-{typ}-{metric}.csv"
            file2 = f"{techniques[j]}/{project}-{typ}-{metric}.csv"

            effect_size = wilcoxon_effect_size(file1, file2, column)
            
            if effect_size is not None:
                comparison_matrix.loc[techniques[i], techniques[j]] = effect_size

    # Convert categorical values to numerical for heatmap
    numeric_matrix = comparison_matrix.applymap(lambda x: color_map.get(x, 0) if pd.notnull(x) else 0)
    
    # Plot heatmap for the project
    sns.heatmap(numeric_matrix, annot=comparison_matrix, fmt='', cmap="Blues", 
                linewidths=0.5, vmin=0, vmax=1, ax=axes[row, col])
    axes[row, col].set_title(f"{project}")

# Adjust layout and save
plt.tight_layout(rect=[0, 0, 1, 0.95])
combined_heatmap_path = f"effect_size_combined_{column}_{metric}_{typ}.png"
plt.savefig(combined_heatmap_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Combined heatmap saved to {combined_heatmap_path}")
