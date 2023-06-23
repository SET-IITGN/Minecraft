import re
import subprocess
from typing import Literal
import chardet

def git_diff(repo_path: Literal["Git repository path"], commit_1:Literal['Commit 1'], 
             commit_2:Literal['Commit 2'], file_path:Literal['File path to do fit diff on']):
    ''''
    return git diff of two commits.
    Commit 1 and Commit 2 arre hashes
    '''
    # print(commit_1, commit_2, file_path)
    cmd = ['git', 'diff',commit_1, commit_2, file_path]
    result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    codecs_list = ['utf-8', 'iso-8859-1','utf-16', 'utf-32', 'latin-1', 'cp1252']
    for codec in codecs_list:
        try:
            decoded_text = result.stdout.decode(codec)
            return decoded_text
        except:
            continue
    return None 


def get_pairs(diff:str, output='number'):
    '''
    returns pairs of deletions and addition
    when diff output is provided as input 
    output [optional]: default is number, 
    if you need pair of added and deleted line
    use line
    '''
    

    deletion_regex = r'^-(?![\s+]).*'
    addition_regex = r'^\+(?![\s-]).*'
    pairs = []
    current_pair = []
    is_negative = False
    is_positive = False
    line_no = 1
    at_found = False
    for line in diff.splitlines():    
        # try:
        #     print(line_no_old, line_no_new,line)
        # except:
        #     pass
        if line.startswith("@@"):
            at_found = True
            line_no = int(re.findall(r"\+(\d+)", line)[0])
            try:
                line_no_new = int(line.split('+')[1].split(',')[0])
            except:
                line_no_new = int(line.split('+')[1].split('@@')[0])
            try:
                line_no_old = int(line.split('-')[1].split(',')[0])
            except:
                line_no_old = int(line.split('-')[1].split('+')[0].strip())
            # print(line_no_old, line_no_new)
            if current_pair:
                current_pair[1] = current_pair[1].rstrip(", ")
                pairs.append(current_pair)
            current_pair = []
            is_negative = False
            is_positive = False
        elif line.startswith("-") and not line.startswith("---"):
            if not is_negative:
                current_pair = [str(line_no_old), ""]
                is_negative = True
            elif is_negative and not is_positive:
                current_pair[0] += ", " + str(line_no_old)
            elif is_negative and is_positive:
                current_pair[1] = current_pair[1].rstrip(", ")
                pairs.append(current_pair)
                current_pair = [str(line_no_old), ""]
                is_positive = False
            line_no_old += 1
            
                
        elif line.startswith("+") and not line.startswith("+++") and is_negative:

            is_positive = True
            if is_negative and is_positive:
                
                current_pair[1] += str(line_no_new)+", "
            line_no_new += 1
            
        elif line == '\ No newline at end of file':
            continue
        elif line.startswith("+") and not line.startswith("+++") and not is_negative:
            line_no_new += 1
        elif at_found:
            line_no_new += 1
            line_no_old += 1

    # Process the last pair if any
    if current_pair:
        current_pair[1] = current_pair[1].rstrip(", ")
        pairs.append(current_pair)
    
    # Print all the pairs
    del_add=[]
    for pair in pairs:
        deletion, addition = pair
        if addition and deletion:
            del_add.append([deletion,addition])
    return del_add


# for deletion, addition in get_pairs(diff):
#     print("Deletion:", deletion)
#     print("Addition:", addition)
#     print()