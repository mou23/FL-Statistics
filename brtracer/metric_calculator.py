import sys
import csv
from bug_data_processor import get_bug_data

project = sys.argv[1] # 'aspectj'
result_directory = sys.argv[2] #'../../dataset/temp/bl_test_run_2/recommended'
bug_report_file = sys.argv[3] #'../../dataset/aspectj-filtered.xml'
typ = sys.argv[4]
bug_data = get_bug_data(bug_report_file, result_directory)


def calculate_reciprocal_rank(project, typ):
    results = {}

    for current_bug_data in bug_data:
        bug_id = current_bug_data['bug_id']
        suspicious_files = current_bug_data['suspicious_files'].split(",")
        length_of_suspicious_files = len(suspicious_files)
        fixed_files = current_bug_data['files'].split('.java')
        fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
        
        inverse_rank = 0
        for i in range(length_of_suspicious_files):
            if suspicious_files[i] in fixed_files:
                inverse_rank = 1 / (i + 1)
                break
        
        results[bug_id] = inverse_rank

    output_file = f"{project}-{typ}-reciprocal-rank.csv"
    with open(output_file, mode='w', newline='') as csv_file:
        fieldnames = ['Bug ID', 'Reciprocal Rank']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for bug_id, rr in results.items():
            writer.writerow({'Bug ID': bug_id, 'Reciprocal Rank': rr})

def calculate_average_precision(project, typ):
    results = {}

    for current_bug_data in bug_data:
        bug_id = current_bug_data['bug_id']
        suspicious_files = current_bug_data['suspicious_files'].split(",")
        fixed_files = current_bug_data['files'].split('.java')
        fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
        
        number_of_relevant_files = 0
        precision_sum = 0

        for i, file in enumerate(suspicious_files):
            if file in fixed_files:
                number_of_relevant_files += 1
                precision_sum += number_of_relevant_files / (i + 1)

        if fixed_files:
            average_precision = precision_sum / len(fixed_files)
        else:
            average_precision = 0

        results[bug_id] = average_precision

    output_file = f"{project}-{typ}-average-precision.csv"
    with open(output_file, mode='w', newline='') as csv_file:
        fieldnames = ['Bug ID', 'Average Precision']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for bug_id, ap in results.items():
            writer.writerow({'Bug ID': bug_id, 'Average Precision': ap})


calculate_reciprocal_rank(project, typ)
calculate_average_precision(project, typ)
