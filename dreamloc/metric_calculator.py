import sys
import csv
from bug_data_processor import get_bug_data

project = sys.argv[1]
result_file = sys.argv[2] #'tomcat_ranked_result_mapped.csv'
bug_report_file = sys.argv[3] #'../../dataset/tomcat-updated-data.xml'
typ = sys.argv[4]
index = sys.argv[5]
bug_data = get_bug_data(bug_report_file, result_file, index)


arr = [10]

def calculate_reciprocal_rank_at_k():
    results = {}

    for top in arr:
        for current_bug_data in bug_data:
            bug_id = current_bug_data['bug_id']
            suspicious_files = current_bug_data['suspicious_files'].split(",")
            fixed_files = current_bug_data['fixed_files'].split('.java')
            fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
            minimum_length = min(top, len(suspicious_files))
            inverse_rank = 0

            for i in range(minimum_length):
                if suspicious_files[i] in fixed_files:
                    inverse_rank = 1 / (i + 1)
                    break

            if bug_id not in results:
                results[bug_id] = {}
            results[bug_id][top] = inverse_rank

    with open(f"{project}-{typ}-reciprocal-rank.csv", mode='w', newline='') as csv_file:
        fieldnames = ['Bug ID'] + [f'Top-{top}' for top in arr]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for bug_id, ranks in results.items():
            row = {'Bug ID': bug_id}
            row.update({f'Top-{top}': round(ranks.get(top, 0), 3) for top in arr})
            writer.writerow(row)


def calculate_average_precision_at_k():
    results = {}

    for top in arr:
        for current_bug_data in bug_data:
            bug_id = current_bug_data['bug_id']
            suspicious_files = current_bug_data['suspicious_files'].split(",")
            fixed_files = current_bug_data['fixed_files'].split('.java')
            fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
            number_of_relevant_files = 0
            precision_sum = 0
            minimum_length = min(top, len(suspicious_files))

            for i in range(minimum_length):
                if suspicious_files[i] in fixed_files:
                    number_of_relevant_files += 1
                    precision_sum += (number_of_relevant_files / (i + 1))

            average_precision = precision_sum / len(fixed_files) if fixed_files else 0

            if bug_id not in results:
                results[bug_id] = {}
            results[bug_id][top] = average_precision

    with open(f"{project}-{typ}-average-precision.csv", mode='w', newline='') as csv_file:
        fieldnames = ['Bug ID'] + [f'Top-{top}' for top in arr]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for bug_id, precisions in results.items():
            row = {'Bug ID': bug_id}
            row.update({f'Top-{top}': round(precisions.get(top, 0), 3) for top in arr})
            writer.writerow(row)


calculate_reciprocal_rank_at_k()
calculate_average_precision_at_k()