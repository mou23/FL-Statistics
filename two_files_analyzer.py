import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, mannwhitneyu, shapiro, probplot, levene, ks_2samp

def get_descriptive_statistics(values1, values2, col):
    print(f"********************Descriptive Statistics: for {col}********************")
    print("File 1:")
    print(values1.describe())
    print("\nFile 2:")
    print(values2.describe())

def create_histogram(project, values1, values2, col):
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.hist(values1, bins=10, color='blue', alpha=0.7, edgecolor='black')
    plt.title('Score Frequency Distribution (File1)')
    plt.xlabel('Score')
    plt.ylabel('Frequency')

    plt.subplot(2, 1, 2)
    plt.hist(values2, bins=10, color='red', alpha=0.7, edgecolor='black')
    plt.title('Score Frequency Distribution (File2)')
    plt.xlabel('Score')
    plt.ylabel('Frequency')


    plt.tight_layout()
    plt.savefig(project + '-' + col + '-score-distribution.png')
    plt.close()

def create_qq_plot(project, values1, values2, col):
    plt.figure(figsize=(12, 8))

    plt.subplot(1, 2, 1)
    probplot(values1, dist="norm", plot=plt)
    plt.title("Q-Q Plot (File1)")
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Sample Quantiles")

    plt.subplot(1, 2, 2)
    probplot(values2, dist="norm", plot=plt)
    plt.title("Q-Q Plot (File2)")
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Sample Quantiles")

    plt.tight_layout()
    plt.savefig(project + '-' + col + '-qq-plot.png', dpi=300)
    plt.close()

    
def check_distribution(values1, values2, col):
    print(f"********************Distribution Result for {col}********************")
    values1 = np.array(values1)
    values2 = np.array(values2)

    if len(values1) < 3 or len(values2) < 3:
        print("Warning: Sample size too small for distribution tests.")
        return
    
    levene_stat, levene_p = levene(values1, values2)
    print(f"Levene’s Test: statistic = {levene_stat}, p-value = {levene_p}")
    if levene_p>0.05:
        print('similar distributions for Levene’s Test')
    else:
        print('different distributions for Levene’s Test')
    ks_stat, ks_p_value = ks_2samp(values1, values2)
    print(f"KS Test: statistic = {ks_stat}, p-value = {ks_p_value}")

    if ks_p_value>0.05:
        print('similar distributions for KS Test')
    else:
        print('different distributions for KS Test')

def interpret_effect_size(r):
    if r < 0.1:
        return "negligible"
    elif r < 0.3:
        return "small"
    elif r < 0.5:
        return "medium"
    else:
        return "large"
    
def check_significance(values1, values2, col):
    print(f"********************Significance Result for {col}********************")
    values1 = np.array(values1)
    values2 = np.array(values2)

    # Check normality for both groups
    _, p_value1 = shapiro(values1)
    _, p_value2 = shapiro(values2)

    print(f"file1 normality p-value for {col}:", p_value1)
    print(f"file2 normality p-value for {col}:", p_value2)

    # If p > 0.05, data is approximately normal; else use Mann-Whitney U test
    if p_value1 > 0.05 and p_value2 > 0.05:
        t_stat, t_p_value = ttest_ind(values1, values2, equal_var=False)
        print(f"T-Test: t-statistic = {t_stat}, p-value = {t_p_value}")
    else:
        u_stat, u_p_value = mannwhitneyu(values1, values2, alternative='two-sided')
        n1 = len(values1)
        n2 = len(values2)
        n = n1 + n2
        # Convert U to z-score
        z = (u_stat - (n1 * n2 / 2)) / np.sqrt((n1 * n2 * (n + 1)) / 12)
        # Calculate effect size r
        r = abs(z) / np.sqrt(n)
        print(f"Mann-Whitney U Test: U-statistic = {u_stat}, p-value = {u_p_value}")
        print(f"Effect size (r) = {r:.3f}")
        print(f"Effect size interpretation: {interpret_effect_size(r)}")

    alpha = 0.05
    if (p_value1 > 0.05 and p_value2 > 0.05 and t_p_value < alpha) or ((p_value1 <= 0.05 or p_value2 <= 0.05) and u_p_value < alpha):
        print("The difference between values1 and value2 is statistically significant.")
    else:
        print("The difference between values1 and value2 is NOT statistically significant.")


def analyze_files(project, file1, file2):
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)

    common_columns = [col for col in data1.columns if col in data2.columns and col != 'Bug ID']
    if not common_columns:
        print("No common columns to compare!")
        return

    for col in common_columns:
        print(f"\n*** Analysis for Column: {col} ***\n")
        values1 = data1[col].dropna()
        values2 = data2[col].dropna()
        get_descriptive_statistics(values1, values2, col)
        create_histogram(project, values1, values2, col)
        create_qq_plot(project, values1, values2, col)
        check_distribution(values1, values2, col)
        check_significance(values1, values2, col)

project = sys.argv[1]
file1 = sys.argv[2]
file2 = sys.argv[3]
analyze_files(project, file1, file2)