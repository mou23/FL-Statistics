import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, mannwhitneyu, shapiro, probplot, levene, ks_2samp
from itertools import product


def create_histogram(technique, values1, values2, col):
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.hist(values1, bins=10, color='blue', alpha=0.7, edgecolor='black')
    plt.title('Score Frequency Distribution (Baseline)')
    plt.xlabel('Score')
    plt.ylabel('Frequency')

    plt.subplot(2, 1, 2)
    plt.hist(values2, bins=10, color='red', alpha=0.7, edgecolor='black')
    plt.title('Score Frequency Distribution (Clean)')
    plt.xlabel('Score')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.savefig(technique + '-' + col + '-score-distribution.png')
    plt.close()



def analyze_files(technique, file1, file2):
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)

    common_columns = [col for col in data1.columns if col in data2.columns and col != 'Bug ID']
    if not common_columns:
        print("No common columns to compare!")
        return

    for col in common_columns:
        values1 = data1[col].dropna()
        values2 = data2[col].dropna()

        create_histogram(technique, values1, values2, col)
        

for technique in ["vsm", "buglocator", "bluir", "brtracer", "dreamloc"]:
    for metric in ["average-precision", "reciprocal-rank"]:
        file1 = f"{technique}/baseline-{metric}.csv"
        file2 = f"{technique}/clean-{metric}.csv"
        analyze_files(technique, file1, file2)
