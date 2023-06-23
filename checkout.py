from pydriller import Git
import os
import shutil
import sys
def checkout(repo_path, commit, prev):
    '''
    checkout to a specific commit
    '''
    # gr=Git(repo_path)
    # print('checkout to commit: ', commit)
    # print(repo_path)
    prev_path = os.path.join(os.getcwd(),'prev')
    curr_path = os.path.join(os.getcwd(),'curr')
    prev_comm = Git(prev_path)
    curr_comm = Git(curr_path)
    prev_comm.checkout(prev)
    curr_comm.checkout(commit)
