import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('merged_dataset.csv')
test_df = df[df['train_test'] == 'test']

techniques = {
    'buglocator': 'buglocator_baseline_k@10',
    'bluir': 'bluir_baseline_k@10',
    'vsm': 'vsm_baseline_k@10',
    'brtracer': 'brtracer_baseline_k@10',
    'dreamloc': 'dreamloc_baseline_k@10'
}

def perform_chi_square_test(data, baseline_col):
    # Create binary column for localization
    data['localized'] = data[baseline_col]
    
    # Create binary column for bug type (True for bug, False for not bug)
    data['is_bug'] = data['label'] == 'BUG'
    
    # Create contingency table
    contingency = pd.crosstab(
        data['localized'],
        data['is_bug'],
        margins=True
    )
    
    # Perform chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency.iloc[:-1, :-1])
    
    # Calculate phi coefficient
    n = contingency.iloc[-1, -1]  # total sample size
    phi = np.sqrt(chi2 / n)
    
    return {
        'contingency_table': contingency,
        'chi2_statistic': chi2,
        'p_value': p_value,
        'degrees_of_freedom': dof,
        'phi_coefficient': phi,
        'localized_bugs': data[data['is_bug']]['localized'].sum(),
        'localized_non_bugs': data[~data['is_bug']]['localized'].sum(),
        'total_bugs': data['is_bug'].sum(),
        'total_non_bugs': (~data['is_bug']).sum(),
        'total_cases': len(data)
    }

results = {}

for technique, baseline_col in techniques.items():
    print(f"\nAnalyzing {technique.upper()}:")
    print("-" * 50)
    
    result = perform_chi_square_test(test_df, baseline_col)
    results[technique] = result
    
    # Print results
    print("\nContingency Table:")
    print(result['contingency_table'])
    print(f"\nChi-square statistic: {result['chi2_statistic']:.4f}")
    print(f"p-value: {result['p_value']:.4f}")
    print(f"Degrees of freedom: {result['degrees_of_freedom']}")
    print(f"Phi coefficient: {result['phi_coefficient']:.4f}")
    print(f"\nLocalization Statistics:")
    print(f"Total cases: {result['total_cases']}")
    print(f"Total bugs: {result['total_bugs']}")
    print(f"Total non-bugs: {result['total_non_bugs']}")
    print(f"Localized bugs: {result['localized_bugs']} ({result['localized_bugs']/result['total_bugs']*100:.1f}%)")
    print(f"Localized non-bugs: {result['localized_non_bugs']} ({result['localized_non_bugs']/result['total_non_bugs']*100:.1f}%)")

# Create a summary DataFrame
summary_data = {
    'Technique': [],
    'Chi-square': [],
    'p-value': [],
    'Phi Coefficient': [],
    'Significant': [],
    'Bug Localization %': [],
    'Non-Bug Localization %': []
}

for technique, result in results.items():
    summary_data['Technique'].append(technique)
    summary_data['Chi-square'].append(result['chi2_statistic'])
    summary_data['p-value'].append(result['p_value'])
    summary_data['Phi Coefficient'].append(result['phi_coefficient'])
    summary_data['Significant'].append('Yes' if result['p_value'] < 0.05 else 'No')
    summary_data['Bug Localization %'].append(f"{result['localized_bugs']/result['total_bugs']*100:.1f}%")
    summary_data['Non-Bug Localization %'].append(f"{result['localized_non_bugs']/result['total_non_bugs']*100:.1f}%")

summary_df = pd.DataFrame(summary_data)
print("\nSummary of Chi-square Tests:")
print("=" * 50)
print(summary_df.to_string(index=False))

# Create a visualization of p-values
plt.figure(figsize=(12, 6))
sns.barplot(data=summary_df, x='Technique', y='p-value')
plt.axhline(y=0.05, color='r', linestyle='--', label='Significance threshold (p=0.05)')
plt.title('Chi-square Test p-values by Technique\n(Baseline Localization vs Issue Type)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('chi_square_bug_not_bug_results.png')
plt.close()

# Create a visualization of localization percentages
plt.figure(figsize=(12, 6))
summary_df_melted = pd.melt(
    summary_df,
    id_vars=['Technique'],
    value_vars=['Bug Localization %', 'Non-Bug Localization %'],
    var_name='Issue Type',
    value_name='Percentage'
)
summary_df_melted['Percentage'] = summary_df_melted['Percentage'].str.rstrip('%').astype(float)

sns.barplot(data=summary_df_melted, x='Technique', y='Percentage', hue='Issue Type')
plt.title('Localization Success Rate by Technique and Issue Type')
plt.xticks(rotation=45)
plt.ylabel('Localization Success Rate (%)')
plt.legend(title='Issue Type')
plt.tight_layout()
plt.savefig('localization_bug_not_bug_comparison.png')
plt.close()
