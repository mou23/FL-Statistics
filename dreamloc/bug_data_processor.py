import xml.etree.ElementTree as ET
from suspicious_filenames_retriever import extract_suspicious_filenames_for_all_bugs

def get_bug_data(xml_path,result_file, index=0):
    bug_wise_suspicious_filenames = extract_suspicious_filenames_for_all_bugs(result_file)
    bug_ids = list(bug_wise_suspicious_filenames.keys())
    
    bugs = []
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for element in root.findall(".//table"):
        bug_id = element[1].text
        fixed_commit_time = element[8].text
        fixed_files = element[9].text
        
        bug_data = {"bug_id": bug_id,
                    "fixed_commit_time": fixed_commit_time, 
                    "fixed_files": fixed_files}
        bugs.append(bug_data)

    bugs = sorted(bugs, key=lambda d: d['fixed_commit_time'])

    length = len(bugs)
    if index==0:
        starting_index = length - int(length*0.4)
    else:
        starting_index = index
    test_bugs = bugs[starting_index:length]
    
    for bug in test_bugs:
        if bug['bug_id'] in bug_ids:
            list_of_suspicious_filenames = bug_wise_suspicious_filenames[bug['bug_id']]
            bug['suspicious_files'] = ','.join(list_of_suspicious_filenames)
        else:
            bug['suspicious_files'] = ''

    return test_bugs