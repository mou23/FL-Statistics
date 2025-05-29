import sys
import pandas as pd
from bug_data_retriever import get_bug_data
from scipy.stats import chi2_contingency

def get_invalid_bug_ids(file_path):
    invalid_bug_ids = []
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split(',')
            invalid_bug_ids.extend([str(value) for value in values])
    print(invalid_bug_ids)
    return invalid_bug_ids

project = sys.argv[1]
xml_path = sys.argv[2]
localization_data = sys.argv[3]
invalid_bug_data = sys.argv[4]

invalid_bugs = get_invalid_bug_ids(invalid_bug_data)
new_bugs = get_bug_data(xml_path)

bug_status = []

for bug in new_bugs:
    bug_id = str(bug['bug_id'])  # Ensure consistency in format
    status = 'invalid' if bug_id in invalid_bugs else 'valid'
    bug_status.append({'bug_id': bug_id, 'status': status})

bug_df = pd.DataFrame(bug_status)

accuracy_df = pd.read_csv(localization_data)
accuracy = 'Accuracy@10'
# Determine if each bug_id from bug_df was localized at accuracy@10
bug_df['localized'] = bug_df['bug_id'].apply(lambda x: 'localized' if x in accuracy_df[accuracy].values else 'not-localized')

# Create a contingency table
# counts for the combinations of 'status' (bug/not-bug) and 'localized' (localized/not-localized)
contingency_table = pd.crosstab(bug_df['status'], bug_df['localized'])

# Display the contingency table
print("Contingency Table:")
print(contingency_table)

# Perform the chi-square test
chi2, p, dof, expected = chi2_contingency(contingency_table)

# Display the results
print("\nChi-Square Test Results:")
print(f"Chi-Square Statistic: {chi2:.4f}")
print(f"P-value: {p:.4f}")
print(f"Degrees of Freedom: {dof}")
print("\nExpected Frequencies:")
print(expected)

# Interpret the results
alpha = 0.05  # Significance level
if p < alpha:
    print(f"\nSince the p-value ({p:.4f}) is less than {alpha}, we reject the null hypothesis.")
    print(f"There is a significant relationship between the presence of 'reproduction' keywords and bug localization {accuracy}")
else:
    print(f"\nSince the p-value ({p:.4f}) is greater than {alpha}, we fail to reject the null hypothesis.")
    print(f"There is no significant relationship between the presence of 'reproduction' keywords and bug localization {accuracy}")