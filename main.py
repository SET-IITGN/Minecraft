import pandas as pd
import sys
import os
import getCommits
import szz
import checkout
import diff
import AST
import shutil
import bug_type

commit_count = 0
projects = pd.read_csv(sys.argv[1]) #read csv file of projects

def get_project_name():
    return projects['Project_name']

def get_project_url():
    return projects['URL']

def get_last_processed_project():
    if os.path.exists('./log.txt'):
        with open('./log.txt', 'r') as file:
            last_project = file.readlines()
        return last_project[-1].strip()

if os.path.exists('dataset.csv'):
    df = pd.read_csv('dataset.csv')
else:  
    dataframe = pd.DataFrame(columns=['Before Bug fix', 'After Bug fix', 'Location', 
                                      'Bug type', 'Commit Message', 'Project URL', 'File Path'])
    dataframe.to_csv('dataset.csv', index=False)
    df = pd.read_csv('dataset.csv')
try:
    last_project_index = projects[projects['Project_name'] == get_last_processed_project()].index[0]
except:
    last_project_index = -1

for i in range(last_project_index+1,len(projects)):
    project_name = get_project_name()[i].split('/')[1]
    print(f"Processing for project:  {project_name}, remaining projects: {len(projects)-i-1} ")
    project_url = get_project_url()[i]
    # if os.path.exists(project_name):
    #     shutil.rmtree(project_name)
    if not os.path.exists(project_name):
        os.system('git clone '+project_url)
    repo_path = os.getcwd()+'/'+project_name 
    commits_map = getCommits.get_fixed_commits(repo_path)
    print('Processing SZZ')
    for commits in commits_map:
        modified_files = szz.get_szz(repo_path, commits[0]) #get modified files of current commit
        commits.append(modified_files)
    for commit, prev, modified_files in commits_map:
        commit_count += 1
        print("Processing for commmit: ", commit.hash)
        print("Corresponding commit msg: ", commit.msg.split('\n')[0]) 
        checkout.checkout(repo_path, commit.hash, prev.hash)
        for file_path in modified_files:
            diff_text = diff.git_diff(repo_path, prev.hash, commit.hash, file_path)
            bug_type = test.predict(diff_text)
            pairs = diff.get_pairs(diff_text)
            for deletion, addition in pairs:
                line_no_fixed = int(addition.split(',')[0])
                line_no_buggy = int(deletion.split(',')[0])
                file_path_prev = os.getcwd()+'/' + 'prev/' + file_path
                file_path_curr = os.getcwd()+'/'+ 'curr/' + file_path
                # print(file_path_prev, file_path_curr)
                fixed_code = AST.extract_function_by_line(file_path_curr,line_no_fixed)
                # print(fixed_code)
                line_no_curr = int(addition.split(',')[0])
                buggy_code = AST.extract_function_by_line(file_path_prev, line_no_buggy)
                # print(buggy_code)
                location = 'Before: ' + deletion + '\n' +'After: ' + addition
                new_row = pd.DataFrame([[buggy_code, fixed_code, location, bug_type,
                                         commit.msg.split('\n')[0], project_url, file_path]], columns = df.columns)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv('./dataset.csv', index=False)
    print('Removing project folder: ', project_name)
    if os.path.exists('./log.txt'):
        with open('./log.txt', 'a') as f:
            f.write(get_project_name()[i]+'\n')
    else:
        with open('./log.txt', 'w') as f:
            f.write(get_project_name()[i]+'\n')
    shutil.rmtree(project_name)

print('Commit Count:', commit_count)
with open ('commit_count.txt', 'w') as f:
    f.write(str(commit_count))

# dataframe.to_csv('./out_2.csv')
            

