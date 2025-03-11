import sys
import csv
import json

def calculate_mean_reciprocal_rank_at_k(project, data, typ):
    results = {}
    for top in [10, 20, 30]: #, 40, 50]:
        for key, value in data.items():
            bug_id = key
            inverse_rank = 0
            suspicious_files = value['results']
            length_of_suspicious_files = len(suspicious_files)
            fixed_files = value['truth']
            minimum_length = min(top,length_of_suspicious_files)
            for i in range(minimum_length):
                if(suspicious_files[i] in fixed_files):
                    inverse_rank = (1/(i+1))
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


def calculate_mean_average_precision_at_k(project, data, typ):
    results = {}
    for top in [10, 20, 30]: #, 40, 50]:
        for key, value in data.items():
            bug_id = key
            average_precision = 0
            precision = 0
            suspicious_files = value['results']
            length_of_suspicious_files = len(suspicious_files)
            fixed_files = value['truth']
            number_of_relevant_files = 0
            minimum_length = min(top,length_of_suspicious_files)
            
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


project = sys.argv[1]
result_directory = sys.argv[2]
typ = sys.argv[3]     
with open(result_directory +'/results.json', 'r') as file:
    data = json.load(file)

calculate_mean_reciprocal_rank_at_k(project, data, typ)
calculate_mean_average_precision_at_k(project, data, typ)
