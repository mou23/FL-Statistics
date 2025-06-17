from collections import defaultdict
from scipy import stats
import numpy as np
import math
import pandas as pd
from scipy.stats import rankdata

def rank_biserial_from_arrays(arr1, arr2):
    diff = np.array(arr1) - np.array(arr2)
    non_zero_indices = diff != 0
    diff = diff[non_zero_indices]
    n = len(diff)
    
    abs_diff = np.abs(diff)
    ranks = rankdata(abs_diff)

    R1 = np.sum(ranks[diff > 0])  # sum of ranks for positive differences
    R2 = np.sum(ranks[diff < 0])  # sum of ranks for negative differences
    T = min(R1, R2)

    effect_size = abs((4 * (T - (R1 + R2)/2))) / (n * (n + 1))

def z_score_based_correlation(p_value, n, min_p=1e-16):
    p = max(p_value, min_p)  # Clamps p-value to avoid infinite z-scores.
    z = abs(stats.norm.ppf(p / 2))
    effect_size = z / math.sqrt(n)
    return effect_size

def calculate_statistic(arr1, arr2):
    # Perform Wilcoxon signed-rank test
    statistic, p_value = stats.wilcoxon(arr1, arr2, zero_method='wilcox', correction=False)
    
    # effect_size = rank_biserial_from_arrays(arr1, arr2)

    n = np.sum(np.array(arr1) != np.array(arr2))
    effect_size = z_score_based_correlation(p_value, n)
    
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

    # Create separate tables for each type-metric combination
    for metric in metrics:
        for type_ in types:
            print(f"\n{type_.upper()} - {metric.upper()} COMPARISONS")
            results = []
            
            # Create all possible pairs of techniques
            for i, tech1 in enumerate(techniques):
                for tech2 in techniques[i+1:]:  # Only compare with techniques after current one
                    file1 = f"{tech1}/full-{type_}-{metric}.csv"
                    file2 = f"{tech2}/full-{type_}-{metric}.csv"
                    
                    try:
                        df1 = pd.read_csv(file1)
                        df2 = pd.read_csv(file2)
                        
                        statistic, p_value, effect_size, effect_interpretation = calculate_statistic(df1.iloc[:, 1], df2.iloc[:, 1])

                        results.append({
                            'Technique 1': tech1.upper(),
                            'Technique 2': tech2.upper(),
                            'Statistic': f"{statistic:.3f}",
                            'p-value': f"{p_value:.3f}",
                            'Effect Size': f"{effect_size:.3f}",
                            'Interpretation': effect_interpretation,
                            'Significant': 'Yes' if p_value < 0.05 else 'No'
                        })
                    except FileNotFoundError as e:
                        print(f"Warning: Could not find file for comparison {tech1} vs {tech2}: {e}")
                        continue

            # Convert results to DataFrame and print as table
            results_df = pd.DataFrame(results)
            if not results_df.empty:
                print(f"\nWilcoxon Signed-Rank Test Results for {type_.upper()} - {metric.upper()}:")
                print("="*100)
                print(results_df.to_string(index=False))
                print("="*100)
            else:
                print(f"\nNo valid comparisons found for {type_.upper()} - {metric.upper()}")