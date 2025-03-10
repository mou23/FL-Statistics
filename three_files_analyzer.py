import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import levene, shapiro, probplot

def get_descriptive_statistics(values1, values2, values3, col):
    print(f"********************Descriptive Statistics: for {col}********************")
    print("File 1:")
    print(values1.describe())
    print("\nFile 2:")
    print(values2.describe())
    print("\nFile 3:")
    print(values3.describe())

def create_histogram(project, values1, values2, values3, col):
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.hist(values1, bins=10, color='blue', alpha=0.7, edgecolor='black')
    plt.title('Score Frequency Distribution (File1)')
    plt.xlabel('Score')
    plt.ylabel('Frequency')

    plt.subplot(3, 1, 2)
    plt.hist(values2, bins=10, color='red', alpha=0.7, edgecolor='black')
    plt.title('Score Frequency Distribution (File2)')
    plt.xlabel('Score')
    plt.ylabel('Frequency')

    plt.subplot(3, 1, 3)
    plt.hist(values3, bins=10, color='green', alpha=0.7, edgecolor='black')
    plt.title('Score Frequency Distribution (File2)')
    plt.xlabel('Score')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.savefig(project + '-' + col + '-score-distribution.png')
    plt.close()

def create_qq_plot(project, values1, values2, values3, col):
    plt.figure(figsize=(12, 8))

    plt.subplot(1, 3, 1)
    probplot(values1, dist="norm", plot=plt)
    plt.title("Q-Q Plot (File1)")
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Sample Quantiles")

    plt.subplot(1, 3, 2)
    probplot(values2, dist="norm", plot=plt)
    plt.title("Q-Q Plot (File2)")
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Sample Quantiles")

    plt.subplot(1, 3, 3)
    probplot(values3, dist="norm", plot=plt)
    plt.title("Q-Q Plot (File3)")
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Sample Quantiles")

    plt.tight_layout()
    plt.savefig(project + '-' + col + '-qq-plot.png', dpi=300)
    plt.close()

def check_significance(values1, values2, values3, col):
    print(f"********************Result for {col}********************")
    values1 = np.array(values1)
    values2 = np.array(values2)
    values3 = np.array(values3)

    # Check normality for both groups
    _, p_value1 = shapiro(values1)
    _, p_value2 = shapiro(values2)
    _, p_value3 = shapiro(values3)

    print(f"file1 normality p-value for {col}:", p_value1)
    print(f"file2 normality p-value for {col}:", p_value2)
    print(f"file2 normality p-value for {col}:", p_value3)

    bf_stat, bf_p_value = levene(values1, values2, values3, center='median')
    print(f"Brown-Forsythe Test: statistic = {bf_stat}, p-value = {bf_p_value}")

    # Significance threshold
    alpha = 0.05
    if bf_p_value < alpha:
        print("The variances between the groups are significantly different.")
    else:
        print("The variances between the groups are NOT significantly different.")


def analyze_files(project, file1, file2, file3):
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)
    data3 = pd.read_csv(file3)

    common_columns = [col for col in data1.columns if col in data2.columns and col in data3.columns and col != 'Bug ID']
    if not common_columns:
        print("No common columns to compare!")
        return

    for col in common_columns:
        print(f"\n*** Analysis for Column: {col} ***\n")
        values1 = data1[col].dropna()
        values2 = data2[col].dropna()
        values3 = data3[col].dropna()
        get_descriptive_statistics(values1, values2, values3, col)
        create_histogram(project, values1, values2, values3, col)
        create_qq_plot(project, values1, values2, values3, col)
        check_significance(values1, values2, values3, col)

project = sys.argv[1]
file1 = sys.argv[2]
file2 = sys.argv[3]
file3 = sys.argv[4]
analyze_files(project, file1, file2, file3)