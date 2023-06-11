from pydriller import Git
import os
import shutil
import sys
def checkout(repo_path, commit, prev):
    '''
    checkout to a specific commit
    '''
    gr=Git(repo_path)
    # print('checkout to commit: ', commit)
    # print(repo_path)
    prev_path = os.path.join(os.getcwd(),'prev')
    curr_path = os.path.join(os.getcwd(),'curr')
    if os.path.exists(prev_path):
        shutil.rmtree(prev_path)
    gr.checkout(prev)
    shutil.copytree(repo_path, prev_path)
    if os.path.exists(curr_path):
        shutil.rmtree(curr_path)
    gr.checkout(commit)
    shutil.copytree(repo_path, curr_path)
    try:
        gr.checkout('master')
    except:
        gr.checkout('main')
    return gr
