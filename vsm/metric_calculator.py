import sys
import csv
import json

def calculate_mean_reciprocal_rank(project, data, typ):
    results = {}
    
    for bug_id, value in data.items():
        inverse_rank = 0
        suspicious_files = value['results']
        fixed_files = value['truth']
        for i, file in enumerate(suspicious_files):
            if file in fixed_files:
                inverse_rank = 1 / (i + 1)
                break
        results[bug_id] = inverse_rank

    with open(f"{project}-{typ}-reciprocal-rank.csv", mode='w', newline='') as csv_file:
        fieldnames = ['Bug ID', 'Reciprocal Rank']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for bug_id, rr in results.items():
            writer.writerow({'Bug ID': bug_id, 'Reciprocal Rank': rr})


def calculate_mean_average_precision(project, data, typ):
    results = {}

    for bug_id, value in data.items():
        suspicious_files = value['results']
        fixed_files = value['truth']
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

    with open(f"{project}-{typ}-average-precision.csv", mode='w', newline='') as csv_file:
        fieldnames = ['Bug ID', 'Average Precision']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for bug_id, ap in results.items():
            writer.writerow({'Bug ID': bug_id, 'Average Precision': ap})


# Main
project = sys.argv[1]
result_directory = sys.argv[2]
typ = sys.argv[3]

with open(f"{result_directory}/results.json", 'r') as file:
    data = json.load(file)

calculate_mean_reciprocal_rank(project, data, typ)
calculate_mean_average_precision(project, data, typ)
