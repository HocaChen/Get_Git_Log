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

if __name__ == '__main__':
    
    try:
        # team_member = ['jeff' , 'derrick', 'john', 'simon', 'elvis', 'hoca', 'cynthia', 'ingo', 'christoph', 'sandy', 'dory']
        team_member = ['derrick']


        SCF = 'D:/Program_Project/SCF/AST_SCF'
        SENTIO = 'D:/Program_Project/SENTIO/Azure_Sentio/AST_SENTIO'
        date_from = "2022-05-21"
        date_to = "2022-06-22"
        author = "--pretty=\"%an\""

        repo = git.Repo(SENTIO)
        status = repo.git.status()

        start_date = date(2022, 5, 21) 
        end_date = date(2022, 6, 22)    # perhaps date.now()

        delta = end_date - start_date   # returns timedelta
        date_list=[]
        add_data_list=[]
        delete_data_list=[]
        modify_file_list=[]
        add_line_number = 0
        delete_line_number = 0
        modify_line_number = 0
        
        name = repo.git.log('--since='+date_from,'--until='+date_to, author)
        author_list = filter_author(name)   
        
        for author_name in team_member:
            expected_name = get_author_name(author_name , author_list)
            
            for x in expected_name:
                
                add_line_number = 0
                delete_line_number = 0
                modify_line_number = 0
                for i in range(delta.days + 1):
                    prv_date = start_date + timedelta(days=i-1)
                    day = start_date + timedelta(days=i)

                    s_date = '{}-{}-{}'.format(prv_date.year, prv_date.month, prv_date.day)
                    e_date = '{}-{}-{}'.format(day.year, day.month, day.day)
                    date_list.append(e_date)
                    data = repo.git.log('--shortstat','--author='+x, '--pretty=tformat:','--since={}'.format(s_date),'--until={}'.format(e_date))
                    print('{}:{}'.format(e_date,data))

                    if data != '':
                        count = data.count('\n')
                        interval = 7
                        index_modify = 0 # 7 base
                        index_add = 3
                        index_delet = 5
                        
                        for i in range(0, count + 1):
                            dot_count = data.count(',')
                            start_idx = index_modify + interval * i
                            
                            idx_modify = data.find('changed', start_idx, data.find('\n'))
                            idx_add = data.find('insertions', start_idx, data.find('\n'))
                            idx_delete = data.find('deletion', start_idx, data.find('\n'))
                            
                            modify_file = data.split()[index_modify + interval * i]
                            modify_line_number = modify_line_number + int(modify_file)

                            arg_2nd = data.split()[index_add + interval* i]
                            if(idx_add > -1):
                                add_line = arg_2nd
                                add_line_number = add_line_number + int(add_line)
                            else:
                                delete_line = arg_2nd
                                delete_line_number = delete_line_number + int(delete_line)
                            
                            if (dot_count > 1):
                                delete_line = data.split()[index_delet + interval* i]
                                delete_line_number = delete_line_number + int(delete_line)
                            
                            
                            # if(data.find('insertions', start_idx) > -1):
                            #     index = index_modify + 2
                            #     add_line = data.split()[index_add + interval* i]
                            # if(data.find('deletion', start_idx) > -1):
                            #     delete_line = data.split()[index_delet + interval* i]
                                
                            # add_line_number = add_line_number + int(add_line)
                            # delete_line_number = delete_line_number + int(delete_line)
                            # modify_line_number = modify_line_number + int(modify_file)
                        
                    add_data_list.append(add_line_number)
                    delete_data_list.append(delete_line_number)
                    modify_file_list.append(modify_line_number)


                plt.plot(date_list,add_data_list)
                plt.xticks(rotation=45)
                plt.xlabel('Date')
                plt.ylabel('Line of Code')
                plt.title('Code contribution')
                plt.show()
                # plt.hold()
        
    except Exception as e:
        print(str(e))

