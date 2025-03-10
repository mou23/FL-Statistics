import sys
import csv
from bug_data_processor import get_bug_data

project = sys.argv[1] # 'aspectj'
result_directory = sys.argv[2] #'../../dataset/temp/BLUiR_test_run_2/recommended'
bug_report_file = sys.argv[3] #'../../dataset/aspectj-filtered.xml'
typ = sys.argv[4]
bug_data = get_bug_data(bug_report_file, result_directory)


def calculate_reciprocal_rank_at_k(project, typ):
    results = {}

    for top in [10, 20, 30]: #, 40, 50]:
        for current_bug_data in bug_data:
            bug_id = current_bug_data['bug_id']
            suspicious_files = current_bug_data['suspicious_files'].split(",")
            length_of_suspicious_files = len(suspicious_files)
            fixed_files = current_bug_data['files'].split('.java')
            fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
            minimum_length = min(top, length_of_suspicious_files)
            inverse_rank = 0
            
            for i in range(minimum_length):
                if suspicious_files[i] in fixed_files:
                    inverse_rank = 1 / (i + 1)
                    break
            
            if bug_id not in results:
                results[bug_id] = {}
            results[bug_id][top] = inverse_rank

    with open(project+'-' + typ + '-reciprocal-rank.csv', mode='w', newline='') as csv_file:
        fieldnames = ['Bug ID'] + [f'Top-{top}' for top in [10, 20, 30]]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for bug_id, ranks in results.items():
            row = {'Bug ID': bug_id}
            row.update({f'Top-{top}': ranks.get(top, 0) for top in [10, 20, 30]})
            writer.writerow(row)


def calculate_average_precision_at_k(project, typ):
    # Prepare a dictionary to store results
    results = {}

    # Iterate over different top values
    for top in [10, 20, 30]: #, 40, 50]:
        for current_bug_data in bug_data:
            bug_id = current_bug_data['bug_id']
            suspicious_files = current_bug_data['suspicious_files'].split(",")
            length_of_suspicious_files = len(suspicious_files)
            fixed_files = current_bug_data['files'].split('.java')
            fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
            number_of_relevant_files = 0
            precision = 0
            average_precision = 0
            minimum_length = min(top, length_of_suspicious_files)
            
            for i in range(minimum_length):
                if suspicious_files[i] in fixed_files:
                    number_of_relevant_files += 1
                    precision += (number_of_relevant_files / (i + 1))
            
            if fixed_files:
                average_precision = precision / len(fixed_files)
            
            if bug_id not in results:
                results[bug_id] = {}
            results[bug_id][top] = average_precision

    with open(project+'-'+ typ +'-average-precision.csv', mode='w', newline='') as csv_file:
        fieldnames = ['Bug ID'] + [f'Top-{top}' for top in [10, 20, 30]]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()  
        
        for bug_id, precisions in results.items():
            row = {'Bug ID': bug_id}
            row.update({f'Top-{top}': precisions.get(top, 0) for top in [10, 20, 30]})
            writer.writerow(row)


calculate_reciprocal_rank_at_k(project, typ)
calculate_average_precision_at_k(project, typ)
