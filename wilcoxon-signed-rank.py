from collections import defaultdict
from scipy import stats
import numpy as np
import math
import pandas as pd
import sys

if __name__ == "__main__":
    df1 = pd.read_csv(sys.argv[1])
    df2 = pd.read_csv(sys.argv[2])

    # Perform Wilcoxon signed-rank test
    statistic, p_value = stats.wilcoxon(df1.iloc[:, 1], df2.iloc[:, 1])
    
    # Calculate effect size (r = Z/sqrt(N))
    n = len(df1)  # sample size
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

    print(f"Effect size interpretation: {effect_interpretation} - The difference between the two groups is {'statistically significant' if p_value < 0.05 else 'NOT statistically significant'}")
