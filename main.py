import pandas as pd
import sys
import os
import getCommits
import szz
import checkout
import diff
import AST
import shutil
import bug_type_gen


commit_count = 0
projects = pd.read_csv(sys.argv[1]) #read csv file of projects

def get_project_name():
    return projects['Project_name']

def get_project_url():
    return projects['URL']

def get_last_processed_project():
    if os.path.exists('./log_commit.txt'):
        with open('./log_commit.txt', 'r') as file:
            last_project = file.readlines()
        return last_project[-1].split()

if not os.path.exists('dataset.csv'): 
    dataframe = pd.DataFrame(columns=['Before Bug fix', 'After Bug fix', 'Location', 
                                      'Bug type', 'Commit Message', 'Project URL', 'File Path'])
    dataframe.to_csv('dataset.csv', index=False)

try:
    processing_project, commit_hash = get_last_processed_project()
    last_project_index = projects[projects['Project_name'] == processing_project].index[0]
except:
    last_project_index = 0
    commit_hash = None

for i in range(last_project_index,len(projects)):
    project_name = get_project_name()[i].split('/')[1]
    print(f"Processing for project:  {project_name}, remaining projects: {len(projects)-i-1} ")
    project_url = get_project_url()[i]
    # if os.path.exists(project_name):
    #     shutil.rmtree(project_name)
    if not os.path.exists(project_name):
        os.system('git clone '+project_url)
        os.system('cp -R '+project_name + ' prev')
        os.system('cp -R '+project_name + ' curr')
    repo_path = os.getcwd()+'/'+project_name 
    commits_map = getCommits.get_fixed_commits(repo_path)
    print('Processing SZZ')
    if commit_hash is None:
        szz_index=0
        for commits in commits_map:
            modified_files = szz.get_szz(repo_path, commits[0]) #get modified files of current commit
            commits.append(modified_files)
    else:
        for index, commits in enumerate(commits_map):
            if commit_hash == commits[0].hash:
                szz_index = index
                break
        for _, commits in enumerate(commits_map[szz_index:],start=szz_index):
            modified_files = szz.get_szz(repo_path, commits[0]) #get modified files of current commit
            commits.append(modified_files)
    for commit, prev, modified_files in commits_map[szz_index:]:
        commit_count += 1
        if os.path.exists('./log_commit.txt'):
            with open('./log_commit.txt', 'a') as f:
                f.write(get_project_name()[i]+' '+commit.hash+'\n')
        else:
            with open('./log_commit.txt', 'w') as f:
                f.write(get_project_name()[i]+' '+commit.hash+'\n')
        print("Processing for commmit: ", commit.hash)
        print("Corresponding commit msg: ", commit.msg.split('\n')[0]) 
        checkout.checkout(repo_path, commit.hash, prev.hash)
        for file_path in modified_files:
            diff_text = diff.git_diff(repo_path, prev.hash, commit.hash, file_path)
            bug_type = bug_type_gen.predict(diff_text)
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
                                         commit.msg.split('\n')[0], project_url, file_path]], columns = ['Before Bug fix', 'After Bug fix', 'Location', 
                                      'Bug type', 'Commit Message', 'Project URL', 'File Path'])
                new_row.to_csv('./dataset.csv', mode='a',header=False,index=False)
    print('Removing project folder: ', project_name)
    if os.path.exists('./log.txt'):
        with open('./log.txt','a') as f:
            f.write(get_project_name()[i])
    else:
        with open('./log.txt','w') as f:
            f.write(get_project_name()[i])
    if os.path.exists('./projects_done.txt'):
        with open('./projects_done.txt','r') as f:
            projects_done = int(f.readline())
            
        with open('./projects_done.txt', 'w') as f:
            f.write(str(projects_done+1))
    else:
        with open('./projects_done.txt', 'w') as f:
            f.write(str(1))
    shutil.rmtree(project_name)
    shutil.rmtree('prev')
    shutil.rmtree('curr')
    commit_hash = None
print('Commit Count:', commit_count)
with open ('commit_count.txt', 'w') as f:
    f.write(str(commit_count))

# dataframe.to_csv('./out_2.csv')
            

