from pydriller import Git


def get_szz(repo_path, commit, file_ext='.py'):
    '''
    return all the modified files in the commit
    using SZZ algorithm. 
    file: file extension to filter the files
    default: .py (python files) [optional] if needed
    any file, use all then, all files will be returned
    '''
    git = Git(repo_path)
    modif_files = []
    modified_commits = git.get_commits_last_modified_lines(commit)
    if file_ext == 'all':
        return git.get_commits_last_modified_lines(commit)
    for file in modified_commits:
        file = file.rstrip('.REMOVED.git-id')
        ext = file.split('/')[-1].split('.')[-1]
        if ext in ['py', 'cpp', 'c', 'java']:
            #print(file.rstrip('.REMOVED.git-id'))
            
            modif_files.append(file.rstrip('.REMOVED.git-id'))
    return modif_files


