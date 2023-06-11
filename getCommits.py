import re
from pydriller import Git

keywords = [
    "fixed ", " bug", "fixes ", "fix ", " fix", " fixed", " fixes", "crash", "solves", " resolves",
    "resolves ", " issue", "issue ", "regression", "fall back", "assertion", "coverity", "reproducible",
    "stack-wanted", "steps-wanted", "testcase", "failur", "fail", "npe ", " npe", "except", "broken",
    "differential testing", "error", "hang ", " hang", "test fix", "steps to reproduce", "crash",
    "assertion", "failure", "leak", "stack trace", "heap overflow", "freez", "problem ", " problem",
    " overflow", "overflow ", "avoid ", " avoid", "workaround ", " workaround", "break ", " break",
    " stop", "stop "
]


def get_fixed_commits(repo_path: str):
    '''
    return all the fixed commits along with its previous commits
    in {fixed_commit : previous_commit} format
    '''
    print("Getting fixed commits...")
    git1=Git(repo_path)
    print("Repo: ", repo_path)
    commits = []
    commits_gen=git1.get_list_commits()  # get all commits
    
    for i in commits_gen:
        commits.append(i)
        # print(i.hash)
    print("Total commits: ", len(commits))
    commit_map = []
    for i in range(1,len(commits)):
        commit = commits[i]
        prev_commit = commits[i-1]
        commit_msg = commit.msg.lower()
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            pattern2 = r'.*((solv(ed|es|e|ing))|(fix(s|es|ing|ed)?)|((error|bug|issue)(s)?)).*'
            if re.search(pattern, commit_msg) or re.search(pattern2, commit_msg) or keyword in commit_msg:
                commit_map.append([commit, prev_commit])
                break
    return commit_map





# get_fixed_commits('./geocoder')