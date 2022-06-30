
import re
import os
import subprocess
import git

def run(project_dir, date_from, date_to, search_key, filename):
    bug_dic = {}
    bug_branch_dic = {}
    try:
        os.chdir(project_dir)
    except Exception as e:
        raise e
    branches_list = []
    branches_list = get_branches()
    for branch in branches_list:
        bug_branch_dic = deal_branch(date_from,
                                     date_to,
                                     branch,
                                     search_key)
        for item in bug_branch_dic:
            if item not in bug_dic:
                bug_dic[item] = bug_branch_dic[item]
            else:
                bug_dic[item] = bug_branch_dic[item]
    log_output(filename, bug_dic)

# write commits log to file
def log_output(filename, bug_dic):
    fi = open(filename, 'w')
    for item in bug_dic:
        m1 = '--'*5 + 'BUG:' + item + '--'*20 + '\n'
        fi.write(m1)
        for commit in bug_dic[item]:
            fi.write(commit)
        fi.close()


# abstract log of one branch

def deal_branch(date_from, date_to, branch, search_key):
    try:
        os.system('git checkout ' + branch)
        os.system('git pull ')
    except Exception as error:
        print (error)
    cmd_git_log = ['git',
                   'log',
                   '–stat',
                   '–no-merges',
                   '-m',
                   '–after=' +date_from,
                   '–before=' +date_to]
    proc = subprocess.Popen(cmd_git_log,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    bug_branch_dic = deal_lines(date_from,
                                date_to,
                                search_key,
                                stdout)
    return bug_branch_dic

# analyze log
def deal_lines(date_from, date_to, search_key, stdout):
    bug_dic = {}
    for line in stdout.split('commit '):
        if re.search('Bug:? \d+ ', line) is not None and re.search(search_key, line) is not None:
            match = re.search('Bug:? \d+ ', line).group()
            try:
                bug_id = match.split('Bug: ')[1].split('\n')[0]
            except Exception as e:
                bug_id = match.split('Bug ')[1].split(' ')[0]
            if bug_id not in bug_dic:
                bug_dic[bug_id] = [line]
            else:
                bug_dic[bug_id] += [line]
    return bug_dic


# get all branches of a project
def get_branches():
    branch_list = []
    branches = []
    tmp_str = ''
    try:
        cmd_git_remote = 'git remote show origin'
        proc = subprocess.Popen(cmd_git_remote.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        tmp_str = stdout.split('Local branches configured')[0]
        try:
            tmp_str = tmp_str.split('Remote branches:\n')[1]
        except:
            tmp_str = tmp_str.split('Remote branch:\n')[1]
        branches = tmp_str.split('\n')
        for branch in branches[0:-1]:
            if re.search( 'tracked', branch) is not None:
                branch = branch.replace('tracked', '').strip('')
                branch_list.append(branch)
    except Exception as error:
        if branch_list == []:
            print('Can not get any branch!')
    return branch_list


def filter_author(name_list):
    iter = re.finditer('"(.*)"', name_list)
    indices = [m.start(0) for m in iter]

    author_list = [] 
    for i in range(0,name_list.count('\n')):
        st = name_list[indices[i]+1:indices[i+1]-2]
        if not author_list:
            author_list.append(st) 
        is_diff_int = 0
        for x in author_list:
            if x == st:
                is_diff_int = is_diff_int + 1

        if is_diff_int == 0:        
            author_list.append(st)
        
    return author_list

def get_author_name(expected_name, orig_name_list):
    get_author_name = []
    for x in orig_name_list:
        if expected_name in x.lower():
            get_author_name.append(x)
    return get_author_name

def get_total_add_delete_line(data):
    iter = re.finditer('\t(.*)\t', data)
    indices = [m.start(0) for m in iter]

    ret=[]
    increase_line_list = [] 
    delete_line_list = [] 
    for i in range(0,len(indices)):
        st = data[indices[i]-1:indices[i]]
        increase_line_list.append(st)
        st = data[indices[i]+1:indices[i]+2]
        delete_line_list.append(st)
        
    total_increase = 0  
    total_delete = 0  
    for x in increase_line_list:
        total_increase = total_increase + int(x)
    for x in delete_line_list:
        total_delete = total_delete + int(x)
    ret.append(total_increase)
    ret.append(total_delete)
    
    return ret


if __name__ == '__main__':
    try:
        team_member = ['jeff' , 'derrick', 'john', 'simon', 'elvis', 'hoca', 'cynthia', 'ingo', 'christoph']
        project_dir = 'D:/Program_Project/SCF/AST_SCF'
        date_from = "2022-05-21"
        date_to = "2022-06-22"
        author = "--pretty=\"%an\""
        repo = git.Repo(project_dir)
        status = repo.git.status()
        log = repo.git.log('--since=2022-05-21','--author=Jeff','--pretty=tformat:','--numstat')
        
        name = repo.git.log('--since='+date_from,'--until='+date_to, author)
        author_list = filter_author(name)       
        
        
        for author_name in team_member:
            expected_name = get_author_name(author_name , author_list)

            total_increase = 0
            total_delete = 0
            for x in expected_name:
                data = repo.git.log('--author='+x, '--pretty=tformat:','--numstat','--since='+date_from)
                each_ret = get_total_add_delete_line(data)
                
                total_increase = total_increase + each_ret[0]
                total_delete = total_delete + each_ret[1]
                
            print('{}:{},{}'.format(author_name,total_increase,total_delete ))

    except Exception as e:
        print(str(e))
