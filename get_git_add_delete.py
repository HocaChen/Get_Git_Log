from cProfile import label
import git
import matplotlib.pyplot as plt
import re
import csv
import datetime
import calendar
from datetime import date, timedelta
import os
import shutil

def creat_folder(repo, nonth):
    cur = os.getcwd()
    dir = '{}\\{}_{}'.format(cur, repo, nonth)

    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

def save_pie_chart(repo, month, author, add, delete):
    plt.figure(figsize=(6, 9))  # 顯示圖框架大小

    labels = 'Add Line', 'Delete Line'
    data = [add, delete]
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('{}:Add and Delete'.format(author), {"fontsize": 18})
    plt.legend(loc="best")
    # plt.show()
    plt.savefig('{}_{}\\{}_add_delete_line'.format(repo, month, author),
                bbox_inches='tight',
                pad_inches=0.0)
    plt.close()

def create_csv_file(year, month):
    csv_header = ['Repo', 'Author', 'Add Line', 'Delet Line']
    with open('{}_{}.csv'.format(year, month), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        file.close()

def save_csv_file(year, month, repo, author, add, delete):
    data = [[repo, author, add, delete]]
    with open('{}_{}.csv'.format(year, month), 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        file.close()

def filter_author(name_list):
    iter = re.finditer('"(.*)"', name_list)
    indices = [m.start(0) for m in iter]

    author_list = []
    for i in range(0, name_list.count('\n')):
        st = name_list[indices[i] + 1:indices[i + 1] - 2]
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


def save_add_line_pie_chart(repo, month, author, add, delete):
    plt.figure(figsize=(9, 9))

    labels = author
    data = add
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Total Add Line', {"fontsize": 18})
    plt.legend(bbox_to_anchor=(1.05, 1), loc="best")  # 設定圖例及其位置為最佳
    plt.tight_layout()
    # plt.show()
    plt.savefig('{}_{}\\Total_add_delete_line'.format(repo, month),
                bbox_inches='tight',
                pad_inches=0.0)
    plt.close()

    data = delete
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Total Delete Line', {"fontsize": 18})
    plt.legend(bbox_to_anchor=(1.05, 1), loc="best")  # 設定圖例及其位置為最佳
    plt.tight_layout()
    # plt.show()
    plt.savefig('{}_{}/Total_delete_delete_line'.format(repo, month),
                bbox_inches='tight',
                pad_inches=0.0)
    plt.close()

    # plt.hold(True)

# def get_add_delete(data):
#     iter = re.finditer('"(.*)"', data)
#     indices = [m.start(0) for m in iter]
#
#     author_list = []
#     for i in range(0, name_list.count('\n')):
#         st = name_list[indices[i] + 1:indices[i + 1] - 2]
#         if not author_list:
#             author_list.append(st)
#         is_diff_int = 0
#         for x in author_list:
#             if x == st:
#                 is_diff_int = is_diff_int + 1
#
#         if is_diff_int == 0:
#             author_list.append(st)
#
#     return author_list


def get_add_delete_data(data):
    # How many line it have
    # 0: only one line
    # 1: have two line
    n_count = data.count('\n')

    list_n = []
    for m in re.finditer('\n', data):
        list_n.append(m.start())

    start_index_search = 0
    end_index_search = 0

    add_line_number = 0
    delete_line_number = 0
    modify_line_number = 0

    for i in range(0, n_count + 1):
        pre_idx = 0
        if (i == 0):
            start_index_search = 0
            if (n_count > 0):
                end_index_search = data.find('\n')
            else:
                end_index_search = len(data)
        else:
            start_index_search = list_n[i - 1]

            if (i < n_count):
                end_index_search = list_n[i]
            else:
                end_index_search = len(data)

        sub_data = data[start_index_search:end_index_search]

        idx_modify = sub_data.find('change')
        idx_add = sub_data.find('insertions')
        idx_delete = sub_data.find('deletion')

        if (idx_modify > -1):
            sub_string = sub_data[pre_idx:idx_modify]
            modify_file = sub_string.split()[0]
            pre_idx = idx_modify
            modify_line_number = modify_line_number + int(modify_file)

        if (idx_add > -1):
            sub_string = sub_data[pre_idx:idx_add]
            add_line = sub_string.split()[1]
            pre_idx = idx_add
            add_line_number = add_line_number + int(add_line)

        if (idx_delete > -1):
            sub_string = sub_data[pre_idx:idx_delete]
            delete_line = sub_string.split()[1]
            pre_idx = idx_delete
            delete_line_number = delete_line_number + int(delete_line)

        # print('{}_{}_{}'.format(modify_line_number, add_line_number, delete_line_number))
    ret = []
    ret.append(modify_line_number)
    ret.append(add_line_number)
    ret.append(delete_line_number)

    return ret


def get_total_add_delete_line(data):
    # iter = re.finditer('\t(.*)\t', data)
    # indices = [m.start(0) for m in iter]
    # print(indices)
    char = '\n'
    indices = [i.start() for i in re.finditer(char, data)]

    ret = []
    increase_line_list = []
    delete_line_list = []
    each_line = []
    # separate each line
    for i in range(0, len(indices)):
        if i == 0:
            each_line.append(data[0:indices[i]])
        else:
            each_line.append(data[indices[i - 1] + 1:indices[i]])
            # print(data[indices[i-1]+1:indices[i]])
            if i == len(indices) - 1:
                each_line.append(data[indices[i] + 1:len(data)])
                # print(data[indices[i]+1:len(data)])

    for line in each_line:
        # exclude 'csv'
        csv_index = line.find('csv')
        if csv_index != -1:
            continue

        string_index = line.find('Strings')
        if string_index != -1:
            continue

        char = '\t'
        space_indices = [i.start() for i in re.finditer(char, line)]
        st = line[0:space_indices[0]]
        increase_line_list.append(st)
        st = line[space_indices[0] + 1:space_indices[1]]
        delete_line_list.append(st)

    total_increase = 0
    total_delete = 0
    for x in increase_line_list:
        if x != '-':
            total_increase = total_increase + int(x)
    for x in delete_line_list:
        if x != '-':
            total_delete = total_delete + int(x)

    ret.append(len(each_line))
    ret.append(total_increase)
    ret.append(total_delete)

    return ret

def create_csv_data(s_date, e_data):
    team_member = ['jeff', 'derrick', 'john', 'simon', 'elvis', 'hoca', 'cynthia', 'ingo', 'christoph', 'sandy', 'dory',
                   'jacky']
    # team_member = ['jeff']

    SCF = 'D:/Program_Project/SCF/AST_SCF'
    SENTIO = 'D:\Program_Project\Git\AST_SENTIO'
    author = "--pretty=\"%an\""
    git_repo = []
    git_repo.append(SENTIO)
    git_repo.append(SCF)

    start_date = s_date
    end_date = e_data  # perhaps date.now()

    delta = end_date - start_date  # returns timedelta
    date_list = []

    date_from = '{}-{}-{}'.format(start_date.year, start_date.month, start_date.day)
    date_to = '{}-{}-{}'.format(end_date.year, end_date.month, end_date.day)

    datem = datetime.datetime.today()
    month_name = calendar.month_name[datem.month]
    create_csv_file(datem.year, month_name)
    repo_name = ['SENTIO', 'SCF']

    idx = 0
    for repo_dir in git_repo:

        repo = git.Repo(repo_dir)
        status = repo.git.status()

        name = repo.git.log('--since=' + date_from, '--until=' + date_to, author)
        if name == '':
            continue
        author_list = filter_author(name)

        creat_folder(repo_name[idx], month_name)
        add_line_list = []
        delete_line_list = []

        for author_name in team_member:
            expected_name = get_author_name(author_name, author_list)

            total_add_line_number = 0
            total_delete_line_number = 0
            total_modify_line_number = 0

            add_data_list = []
            delete_data_list = []
            modify_file_list = []
            date_list = []

            for i in range(delta.days + 1):
                prv_date = start_date + timedelta(days=i - 1)
                day = start_date + timedelta(days=i)

                s_date = '{}-{}-{}'.format(prv_date.year, prv_date.month, prv_date.day)
                e_date = '{}-{}-{}'.format(day.year, day.month, day.day)
                date_list.append(e_date)

                cnt = 0
                data_temp = []
                is_diff = True
                for x in expected_name:
                    # data = repo.git.log('--shortstat', '--author=' + x, '--pretty=tformat:',
                    #                     '--since={}'.format(s_date), '--until={}'.format(e_date))
                    data = repo.git.log('--author=' + x, '--pretty=tformat:', '--numstat', '--since=' + s_date,
                                        '--until=' + e_date)
                    ret = [0, 0, 0]
                    if data != '':
                        if not data_temp:
                            ret = get_total_add_delete_line(data)
                        for d in data_temp:
                            if d == data:
                                is_diff = False

                        if is_diff and len(data_temp) != 0:
                            ret = get_total_add_delete_line(data)
                        data_temp.append(data)

                    print('{}_{}:Add:{},Delete:{}'.format(x, e_date, ret[1], ret[2]))
                    total_add_line_number = total_add_line_number + ret[1]
                    total_delete_line_number = total_delete_line_number + ret[2]
                    total_modify_line_number = total_modify_line_number + ret[0]

                add_data_list.append(total_add_line_number)
                delete_data_list.append(total_delete_line_number)
                modify_file_list.append(total_modify_line_number)

            print('{}:Add:{},Delete:{}'.format(author_name, total_add_line_number, total_delete_line_number))

            add_line_list.append(total_add_line_number)
            delete_line_list.append(total_delete_line_number)
            save_csv_file(datem.year, month_name, repo_name[idx], author_name, total_add_line_number,
                          total_delete_line_number)
            if total_add_line_number != 0 and total_delete_line_number != 0:
                save_pie_chart(repo_name[idx], month_name, author_name, total_add_line_number, total_delete_line_number)

        save_add_line_pie_chart(repo_name[idx], month_name, team_member, add_line_list, delete_line_list)
        idx = idx + 1


#  This program will generate the pie chart and CSV files
if __name__ == '__main__':
    try:
        team_member = ['jeff' , 'derrick', 'john', 'simon', 'elvis', 'hoca', 'cynthia', 'ingo', 'christoph', 'sandy', 'dory', 'jacky']
        # team_member = ['jeff']

        SCF = 'D:/Program_Project/SCF/AST_SCF'
        SENTIO = 'D:\Program_Project\Git\AST_SENTIO'
        author = "--pretty=\"%an\""
        git_repo = []
        git_repo.append(SENTIO)
        git_repo.append(SCF)

        start_date = date(2022, 7, 22)
        end_date = date(2022, 8, 21)  # perhaps date.now()

        delta = end_date - start_date  # returns timedelta
        date_list = []

        date_from = '{}-{}-{}'.format(start_date.year, start_date.month, start_date.day)
        date_to = '{}-{}-{}'.format(end_date.year, end_date.month, end_date.day)

        datem = datetime.datetime.today()
        month_name = calendar.month_name[datem.month]
        create_csv_file(datem.year, month_name)
        repo_name = ['SENTIO', 'SCF']

        idx = 0
        for repo_dir in git_repo:

            repo = git.Repo(repo_dir)
            status = repo.git.status()

            name = repo.git.log('--since=' + date_from, '--until=' + date_to, author)
            if name == '':
                continue
            author_list = filter_author(name)

            creat_folder(repo_name[idx], month_name)
            add_line_list = []
            delete_line_list = []

            for author_name in team_member:
                expected_name = get_author_name(author_name, author_list)

                total_add_line_number = 0
                total_delete_line_number = 0
                total_modify_line_number = 0

                add_data_list = []
                delete_data_list = []
                modify_file_list = []
                date_list = []

                for i in range(delta.days + 1):
                    prv_date = start_date + timedelta(days=i - 1)
                    day = start_date + timedelta(days=i)

                    s_date = '{}-{}-{}'.format(prv_date.year, prv_date.month, prv_date.day)
                    e_date = '{}-{}-{}'.format(day.year, day.month, day.day)
                    date_list.append(e_date)

                    cnt = 0
                    data_temp = []
                    is_diff = True
                    for x in expected_name:
                        # data = repo.git.log('--shortstat', '--author=' + x, '--pretty=tformat:',
                        #                     '--since={}'.format(s_date), '--until={}'.format(e_date))
                        data = repo.git.log('--author=' + x, '--pretty=tformat:', '--numstat', '--since=' + s_date,
                                            '--until=' + e_date)
                        ret = [0, 0, 0]
                        if data != '':
                            if not data_temp:
                                ret = get_total_add_delete_line(data)
                            for d in data_temp:
                                if d == data:
                                    is_diff = False

                            if is_diff and len(data_temp) != 0:
                                ret = get_total_add_delete_line(data)
                            data_temp.append(data)

                        print('{}_{}:Add:{},Delete:{}'.format(x, e_date, ret[1], ret[2]))
                        total_add_line_number = total_add_line_number + ret[1]
                        total_delete_line_number = total_delete_line_number + ret[2]
                        total_modify_line_number = total_modify_line_number + ret[0]

                    add_data_list.append(total_add_line_number)
                    delete_data_list.append(total_delete_line_number)
                    modify_file_list.append(total_modify_line_number)

                print('{}:Add:{},Delete:{}'.format(author_name, total_add_line_number, total_delete_line_number))

                add_line_list.append(total_add_line_number)
                delete_line_list.append(total_delete_line_number)
                save_csv_file(datem.year, month_name, repo_name[idx], author_name, total_add_line_number, total_delete_line_number)
                if total_add_line_number != 0 and total_delete_line_number != 0:
                    save_pie_chart(repo_name[idx], month_name, author_name, total_add_line_number, total_delete_line_number)

            save_add_line_pie_chart(repo_name[idx], month_name, team_member, add_line_list, delete_line_list)
            idx = idx + 1

    except Exception as e:
        print(str(e))

