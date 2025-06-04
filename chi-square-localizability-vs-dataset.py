import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt

# Read the dataset
df = pd.read_csv('merged_dataset.csv')

# Filter for test set only
test_df = df[df['train_test'] == 'test']

# Define the techniques and their corresponding columns
techniques = {
    'buglocator': ['buglocator_baseline_k@10', 'buglocator_clean_k@10'],
    'bluir': ['bluir_baseline_k@10', 'bluir_clean_k@10'],
    'vsm': ['vsm_baseline_k@10', 'vsm_clean_k@10'],
    'brtracer': ['brtracer_baseline_k@10', 'brtracer_clean_k@10'],
    'dreamloc': ['dreamloc_baseline_k@10', 'dreamloc_clean_k@10']
}

# Function to create contingency table and perform chi-square test
def perform_chi_square_test(data, baseline_col, clean_col):
    # Binary localization outcomes
    baseline_localized = (data[baseline_col] > 0).astype(int)
    clean_localized = (data[clean_col] > 0).astype(int)

    # Build contingency table: rows = version, cols = localized/not
    contingency = pd.DataFrame({
        'Localized': [
            baseline_localized.sum(),
            clean_localized.sum()
        ],
        'Not Localized': [
            len(baseline_localized) - baseline_localized.sum(),
            len(clean_localized) - clean_localized.sum()
        ]
    }, index=['Baseline', 'Clean'])

    # Chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency)

    return {
        'contingency_table': contingency,
        'chi2_statistic': chi2,
        'p_value': p_value,
        'degrees_of_freedom': dof,
        'baseline_localized_count': baseline_localized.sum(),
        'clean_localized_count': clean_localized.sum(),
        'total_cases': len(data)
    }


results = {}

for technique, columns in techniques.items():
    print(f"\nAnalyzing {technique.upper()}:")
    print("-" * 50)
    
    result = perform_chi_square_test(test_df, columns[0], columns[1])
    results[technique] = result
    
    # Print results
    print("\nContingency Table:")
    print(result['contingency_table'])
    print(f"\nChi-square statistic: {result['chi2_statistic']:.4f}")
    print(f"p-value: {result['p_value']:.4f}")
    print(f"Degrees of freedom: {result['degrees_of_freedom']}")
    print(f"\nLocalization Statistics:")
    print(f"Total cases: {result['total_cases']}")
    print(f"Baseline localized: {result['baseline_localized_count']} ({result['baseline_localized_count']/result['total_cases']*100:.1f}%)")
    print(f"Clean localized: {result['clean_localized_count']} ({result['clean_localized_count']/result['total_cases']*100:.1f}%)")

# Create a summary DataFrame
summary_data = {
    'Technique': [],
    'Chi-square': [],
    'p-value': [],
    'Significant': [],
    'Baseline Localized %': [],
    'Clean Localized %': []
}

for technique, result in results.items():
    summary_data['Technique'].append(technique)
    summary_data['Chi-square'].append(result['chi2_statistic'])
    summary_data['p-value'].append(result['p_value'])
    summary_data['Significant'].append('Yes' if result['p_value'] < 0.05 else 'No')
    summary_data['Baseline Localized %'].append(f"{result['baseline_localized_count']/result['total_cases']*100:.1f}%")
    summary_data['Clean Localized %'].append(f"{result['clean_localized_count']/result['total_cases']*100:.1f}%")

summary_df = pd.DataFrame(summary_data)
print("\nSummary of Chi-square Tests:")
print("=" * 50)
print(summary_df.to_string(index=False))

# Create a visualization of p-values
plt.figure(figsize=(12, 6))
sns.barplot(data=summary_df, x='Technique', y='p-value')
plt.axhline(y=0.05, color='r', linestyle='--', label='Significance threshold (p=0.05)')
plt.title('Chi-square Test p-values by Technique')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('chi_square_results.png')
plt.close()

# Create a visualization of localization percentages
plt.figure(figsize=(12, 6))
summary_df_melted = pd.melt(
    summary_df,
    id_vars=['Technique'],
    value_vars=['Baseline Localized %', 'Clean Localized %'],
    var_name='Version',
    value_name='Percentage'
)
summary_df_melted['Percentage'] = summary_df_melted['Percentage'].str.rstrip('%').astype(float)

sns.barplot(data=summary_df_melted, x='Technique', y='Percentage', hue='Version')
plt.title('Localization Success Rate by Technique and Version')
plt.xticks(rotation=45)
plt.ylabel('Localization Success Rate (%)')
plt.legend(title='Version')
plt.tight_layout()
plt.savefig('localization_comparison.png')
plt.close()

# Create visualizations of contingency tables for each technique
for technique, result in results.items():
    plt.figure(figsize=(8, 6))
    contingency = result['contingency_table']
    
    # Create a heatmap of the contingency table
    sns.heatmap(contingency, annot=True, fmt='d', cmap='YlOrRd')
    plt.title(f'Contingency Table for {technique.upper()}\nChi-square: {result["chi2_statistic"]:.2f}, p-value: {result["p_value"]:.4f}')
    plt.xlabel('Clean Version Localized')
    plt.ylabel('Baseline Version Localized')
    plt.tight_layout()
    plt.savefig(f'contingency_table_{technique}.png')
    plt.close()

# Print detailed contingency tables
print("\nDetailed Contingency Tables:")
print("=" * 50)
for technique, result in results.items():
    print(f"\n{technique.upper()}:")
    print("-" * 30)
    print(result['contingency_table'])
    print(f"Chi-square: {result['chi2_statistic']:.2f}")
    print(f"p-value: {result['p_value']:.4f}")
    print(f"Significant: {'Yes' if result['p_value'] < 0.05 else 'No'}")
    print()
