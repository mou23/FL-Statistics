import csv
import sys
from bug_data_processor import get_bug_data

project = sys.argv[1]
result_file = sys.argv[2] #'tomcat_ranked_result_mapped.csv'
bug_report_file = sys.argv[3] #'../../dataset/tomcat-updated-data.xml'
bug_data = get_bug_data(bug_report_file, result_file)

def create_csv():
    results = {
        1: [],
        5: [],
        10: []
    }
    
    for top in [1, 5, 10]:
        count = 0
        total_bug = 0
        for current_bug_data in bug_data:
            suspicious_files = current_bug_data['suspicious_files'].split(",")
            fixed_files = current_bug_data['fixed_files'].split('.java')
            fixed_files = [(file + '.java').strip() for file in fixed_files[:-1]]
            
            for fixed_file in fixed_files:
                if fixed_file in suspicious_files[0:top]:
                    count = count + 1
                    results[top].append(current_bug_data['bug_id'])
                    break
            total_bug = total_bug + 1
        print(f'accuracy@{top}: {count}/{total_bug} ({(count*100/total_bug):.2f}%)')
    
    with open('localized_bugs_'+project+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(['Accuracy@1', 'Accuracy@5', 'Accuracy@10'])
        
        max_length = max(len(results[1]), len(results[5]), len(results[10]))
        
        for i in range(max_length):
            row = []
            for k in [1, 5, 10]:
                if i < len(results[k]):
                    row.append(results[k][i])
                else:
                    row.append('')
            writer.writerow(row)


create_csv()