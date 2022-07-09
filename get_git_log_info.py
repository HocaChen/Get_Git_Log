import csv
import re
import os
import git
import pandas as pd               
import matplotlib.pyplot as plt  
import datetime
import shutil
import calendar
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
        if x != '-':
            total_increase = total_increase + int(x)
    for x in delete_line_list:
        if x != '-':
            total_delete = total_delete + int(x)
    ret.append(total_increase)
    ret.append(total_delete)
    
    return ret

def save_pie_chart(repo, month, author, add, delete):
    plt.figure(figsize=(6,9))    # 顯示圖框架大小
    
    labels = 'Add Line','Delete Line' 
    data = [add, delete]                        
    plt.pie(data , labels = labels,autopct='%1.1f%%')
    plt.axis('equal')                                          
    plt.title('{}:Add and Delete'.format(author), {"fontsize" : 18})  
    plt.legend(loc = "best")                                   
    # plt.show()
    plt.savefig('{}_{}\\{}_add_delete_line'.format(repo, month, author),   
            bbox_inches='tight',               
            pad_inches=0.0)            
    plt.close() 

def save_add_line_pie_chart(repo, month, author, add, delete):
    plt.figure(figsize=(9,9))    

    labels = author 
    data = add                        
    plt.pie(data , labels = labels,autopct='%1.1f%%')
    plt.axis('equal')                                          
    plt.title('Total Add Line', {"fontsize" : 18})  
    plt.legend(bbox_to_anchor=(1.05, 1), loc = "best")                                   # 設定圖例及其位置為最佳
    plt.tight_layout()                               
    # plt.show()
    plt.savefig('{}_{}\\Total_add_delete_line'.format(repo, month),   
            bbox_inches='tight',               
            pad_inches=0.0)                   
    plt.close() 
    
    data = delete
    plt.pie(data , labels = labels,autopct='%1.1f%%')
    plt.axis('equal')                                          
    plt.title('Total Delete Line', {"fontsize" : 18})  
    plt.legend(bbox_to_anchor=(1.05, 1), loc = "best")                                   # 設定圖例及其位置為最佳
    plt.tight_layout()                               
    # plt.show()
    plt.savefig('{}_{}/Total_delete_delete_line'.format(repo, month),   
            bbox_inches='tight',               
            pad_inches=0.0)                   
    plt.close() 
    
    # plt.hold(True)

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
    
if __name__ == '__main__':
    try:
        team_member = ['jeff' , 'derrick', 'john', 'simon', 'elvis', 'hoca', 'cynthia', 'ingo', 'christoph', 'sandy', 'dory']
        SCF = 'D:/Program_Project/SCF/AST_SCF'
        SENTIO = 'D:/Program_Project/SENTIO/Azure_Sentio/AST_SENTIO'

        start_date = date(2022, 5, 21) 
        end_date = date(2022, 6, 22)    # perhaps date.now()

        date_from = '{}-{}-{}'.format(start_date.year, start_date.month, start_date.day)
        date_to = '{}-{}-{}'.format(end_date.year, end_date.month, end_date.day)

        author = "--pretty=\"%an\""
        git_repo = []
        git_repo.append(SENTIO)
        git_repo.append(SCF)
        repo_name =[]
        repo_name.append('SENTIO')
        repo_name.append('SCF')
        datem = datetime.datetime.today()
        month_name = calendar.month_name[datem.month]
        create_csv_file(datem.year, month_name)
        
        #-----Get by date parameter---
        # delta = end_date - start_date
        # date_list=[]
        # add_data_list=[]
        # delete_data_list=[]
        # modify_file_list=[]
        # add_line_number = 0
        # delete_line_number = 0
        # modify_line_number = 0
        #------Get total Line of Code--------
        idx = 0   
        for repo_dir in git_repo:
            
            cur = os.getcwd()       
            dir = '{}\\{}_{}'.format (cur, repo_name[idx], month_name)
            
            if os.path.exists(dir):
                shutil.rmtree(dir)
            os.makedirs(dir)   
                        
            repo = git.Repo(repo_dir)
            status = repo.git.status()

            name = repo.git.log('--since='+date_from,'--until='+date_to, author)
            author_list = filter_author(name)       
            add_line_list =[]
            delete_line_list =[]
            for author_name in team_member:
                expected_name = get_author_name(author_name , author_list)

                total_increase = 0
                total_delete = 0
                for x in expected_name:
                    #----Get total line of Code----
                    data = repo.git.log('--author='+x, '--pretty=tformat:','--numstat','--since='+date_from, '--until='+ date_to)
                    each_ret = get_total_add_delete_line(data)
                    
                    total_increase = total_increase + each_ret[0]
                    total_delete = total_delete + each_ret[1]
                    
                    #----Get line of code by date---
                    # for i in range(delta.days + 1):
                    #     prv_date = start_date + timedelta(days=i-1)
                    #     day = start_date + timedelta(days=i)

                    #     s_date = '{}-{}-{}'.format(prv_date.year, prv_date.month, prv_date.day)
                    #     e_date = '{}-{}-{}'.format(day.year, day.month, day.day)
                    #     date_list.append(e_date)
                    #     data = repo.git.log('--shortstat','--author='+x, '--pretty=tformat:','--since={}'.format(s_date),'--until={}'.format(e_date))
                    #     print('{}:{}'.format(e_date,data))
                    
                
                add_line_list.append(total_increase)
                delete_line_list.append(total_delete)
                print('{}:{},{}'.format(author_name,total_increase,total_delete ))
                save_pie_chart(repo_name[idx], month_name, author_name,total_increase,total_delete)
                save_csv_file(datem.year, month_name, repo_name[idx], author_name,total_increase,total_delete)

            save_add_line_pie_chart(repo_name[idx], month_name, team_member, add_line_list, delete_line_list)
            idx += 1
        
        #------Get line of code by date-----
            
    except Exception as e:
        print(str(e))
