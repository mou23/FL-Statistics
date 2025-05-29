import csv

def extract_suspicious_filenames_for_all_bugs(result_file):
    bug_wise_suspicious_filenames = {}
    
    try:
        with open(result_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                bug_id = row['Bug-ID']
                filename = row['Path']
                
                if bug_id in bug_wise_suspicious_filenames:
                    bug_wise_suspicious_filenames[bug_id].append(filename)
                else:
                    bug_wise_suspicious_filenames[bug_id] = [filename]
                    
        return bug_wise_suspicious_filenames
    
    except FileNotFoundError:
        print(f"Error: The file {result_file} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None