from cProfile import label
import git
import matplotlib.pyplot as plt
import re

from datetime import date, timedelta

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

def get_add_delete(data):
    iter = re.finditer('"(.*)"', data)
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

def get_add_delete_data(data):

    #How many line it have
    # 0: only one line
    # 1: have two line
    n_count = data.count('\n')

    list_n=[]
    for m in re.finditer('\n', data):
        list_n.append(m.start())
            
    start_index_search = 0
    end_index_search = 0

    add_line_number = 0
    delete_line_number = 0
    modify_line_number = 0


    for i in range(0, n_count + 1):
        pre_idx = 0
        if(i == 0):
            start_index_search = 0
            if(n_count > 0):
                end_index_search = data.find('\n')
            else:
                end_index_search = len(data)
        else:
            start_index_search = list_n[i-1]
            
            if (i < n_count):
                end_index_search = list_n[i]
            else:
                end_index_search = len(data)

        sub_data = data[start_index_search:end_index_search]

        idx_modify = sub_data.find('change')
        idx_add = sub_data.find('insertions')
        idx_delete = sub_data.find('deletion')
        
        if(idx_modify > -1):
            sub_string = sub_data[pre_idx:idx_modify]
            modify_file = sub_string.split()[0]
            pre_idx = idx_modify
            modify_line_number = modify_line_number + int(modify_file)
        
        if(idx_add > -1):
            sub_string = sub_data[pre_idx:idx_add]
            add_line = sub_string.split()[1]
            pre_idx = idx_add
            add_line_number = add_line_number + int(add_line)
            
        if(idx_delete > -1):
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

if __name__ == '__main__':
    try:
        team_member = ['jeff' , 'derrick', 'john', 'simon', 'elvis', 'hoca', 'cynthia', 'ingo', 'christoph', 'sandy', 'dory']
        # team_member = ['jeff']
        #
        #
        SCF = 'D:/Program_Project/SCF/AST_SCF'
        SENTIO = 'D:/Program_Project/SENTIO/Azure_Sentio/AST_SENTIO'
        # date_from = "2022-05-21"
        # date_to = "2022-06-22"
        author = "--pretty=\"%an\""

        repo = git.Repo(SENTIO)
        status = repo.git.status()

        start_date = date(2022, 6, 22)
        end_date = date(2022, 7, 21)    # perhaps date.now()

        delta = end_date - start_date   # returns timedelta
        date_list=[]

        date_from = '{}-{}-{}'.format(start_date.year, start_date.month, start_date.day)
        date_to = '{}-{}-{}'.format(end_date.year, end_date.month, end_date.day)

        name = repo.git.log('--since='+date_from,'--until='+date_to, author)
        author_list = filter_author(name)

        fig = plt.figure(dpi=128, figsize=(10, 6))

        for author_name in team_member:
            expected_name = get_author_name(author_name , author_list)

            total_add_line_number = 0
            total_delete_line_number = 0
            total_modify_line_number = 0

            add_data_list = []
            delete_data_list = []
            modify_file_list = []
            date_list = []

            for i in range(delta.days + 1):
                prv_date = start_date + timedelta(days=i-1)
                day = start_date + timedelta(days=i)

                s_date = '{}-{}-{}'.format(prv_date.year, prv_date.month, prv_date.day)
                e_date = '{}-{}-{}'.format(day.year, day.month, day.day)
                date_list.append(e_date)

                cnt = 0
                data_temp = []
                is_diff = True
                for x in expected_name:
                    data = repo.git.log('--shortstat', '--author='+x, '--pretty=tformat:', '--since={}'.format(s_date), '--until={}'.format(e_date))


                    ret = [0, 0, 0]
                    if data != '':
                        if not data_temp:
                            ret = get_add_delete_data(data)
                        for d in data_temp:
                            if d == data:
                                is_diff = False

                        if is_diff and len(data_temp) != 0:
                            ret = get_add_delete_data(data)
                        data_temp.append(data)

                    print('{}_{}:Add:{},Delete:{}'.format(x, e_date, ret[1], ret[2]))
                    total_add_line_number = total_add_line_number + ret[1]
                    total_delete_line_number = total_delete_line_number + ret[2]
                    total_modify_line_number = total_modify_line_number + ret[0]

                add_data_list.append(total_add_line_number)
                delete_data_list.append(total_delete_line_number)
                modify_file_list.append(total_modify_line_number)

            print('{}:Add:{},Delete:{}'.format(author_name, total_add_line_number, total_delete_line_number))
            plt.plot(date_list, add_data_list, label=author_name)
            plt.xticks(rotation=45)
            plt.xlabel('Date')
            plt.ylabel('Line of Code')
            plt.title('Code contribution')
            plt.legend()

        plt.tight_layout()
        # plt.tick_params(axis='x', which='major', labelsize=20)
        plt.show()
        # plt.savefig('plot.png')
    except Exception as e:
        print(str(e))

