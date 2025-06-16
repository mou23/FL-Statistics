from collections import defaultdict
from scipy import stats
import numpy as np
import math
import pandas as pd
import sys

def calculate_statistic(arr1, arr2):
    # Perform Wilcoxon signed-rank test
    statistic, p_value = stats.wilcoxon(arr1, arr2)
    
    # Calculate effect size (r = Z/sqrt(N))
    n = len(arr1)  # sample size
    z = abs(stats.norm.ppf(p_value/2))  # convert p-value to z-score
    effect_size = z / math.sqrt(n)
    
    print(f"\nWilcoxon signed-rank test:")
    print(f"Statistic: {statistic:.3f}")
    print(f"p-value: {p_value:.3f}")
    print(f"Effect size (r): {effect_size:.3f}")
    
    # Interpret effect size
    if effect_size < 0.1:
        effect_interpretation = "negligible"
    elif effect_size < 0.3:
        effect_interpretation = "small"
    elif effect_size < 0.5:
        effect_interpretation = "medium"
    else:
        effect_interpretation = "large"

    return statistic, p_value, effect_size, effect_interpretation


if __name__ == "__main__":
    types = ["baseline", "clean"]
    metrics = ["ap", "rr"]
    techniques = ["vsm", "buglocator", "bluir", "brtracer", "dreamloc"]

    print("\n" + "="*80)
    print("WILCOXON SIGNED-RANK TEST RESULTS")
    print("="*80)

    for type_ in types:
        print(f"\n{type_.upper()}")
        results = []
        print("-"*40)
        
        # Create all possible pairs of techniques
        for i, tech1 in enumerate(techniques):
            for tech2 in techniques[i+1:]:  # Only compare with techniques after current one
                for metric in metrics:
                    file1 = f"{tech1}/full-{type_}-{metric}.csv"
                    file2 = f"{tech2}/full-{type_}-{metric}.csv"
                    
                    try:
                        df1 = pd.read_csv(file1)
                        df2 = pd.read_csv(file2)
                        
                        statistic, p_value, effect_size, effect_interpretation = calculate_statistic(df1.iloc[:, 1], df2.iloc[:, 1])

                        results.append({
                            'Technique 1': tech1.upper(),
                            'Technique 2': tech2.upper(),
                            'Metric': metric.upper(),
                            'Statistic': f"{statistic:.3f}",
                            'p-value': f"{p_value:.3f}",
                            'Effect Size': f"{effect_size:.3f}",
                            'Interpretation': effect_interpretation,
                            'Significant': 'Yes' if p_value < 0.05 else 'No'
                        })
                    except FileNotFoundError as e:
                        print(f"Warning: Could not find file for comparison {tech1} vs {tech2} for {metric}: {e}")
                        continue

        print("-"*40)

        # Convert results to DataFrame and print as table
        results_df = pd.DataFrame(results)
        if not results_df.empty:
            print(f"\nWilcoxon Signed-Rank Test {type_.upper()} Results:")
            print("="*120)  # Increased width for the wider table
            print(results_df.to_string(index=False))
            print("="*120)
        else:
            print(f"\nNo valid comparisons found for {type_.upper()}")