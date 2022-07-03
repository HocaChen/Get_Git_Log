
import re
import os
import subprocess
import git
import pandas as pd               
import matplotlib.pyplot as plt  
import datetime
import pathlib
import shutil

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

def save_pie_chart(author, add, delete):
    plt.figure(figsize=(6,9))    # 顯示圖框架大小
    datem = datetime.datetime.today()
    
    labels = 'Add Line','Delete Line' 
    data = [add, delete]                        
    plt.pie(data , labels = labels,autopct='%1.1f%%')
    plt.axis('equal')                                          
    plt.title('{}:Add and Delete'.format(author), {"fontsize" : 18})  
    plt.legend(loc = "best")                                   
    # plt.show()
    plt.savefig('{}/{}_add_delete_line'.format(datem.month,author),   
            bbox_inches='tight',               
            pad_inches=0.0)                   
    plt.close() 

def save_add_line_pie_chart(author, add, delete):
    plt.figure(figsize=(9,9))    
    datem = datetime.datetime.today()
    
    labels = author 
    data = add                        
    plt.pie(data , labels = labels,autopct='%1.1f%%')
    plt.axis('equal')                                          
    plt.title('Total Add Line', {"fontsize" : 18})  
    plt.legend(bbox_to_anchor=(1.05, 1), loc = "best")                                   # 設定圖例及其位置為最佳
    plt.tight_layout()                               
    # plt.show()
    plt.savefig('{}/Total_add_delete_line'.format(datem.month),   
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
    plt.savefig('{}/Total_delete_delete_line'.format(datem.month),   
            bbox_inches='tight',               
            pad_inches=0.0)                   
    plt.close() 
    
    # plt.hold(True)
      
    
if __name__ == '__main__':
    try:
        team_member = ['abc' , 'def']
        git_project_dir = 'D:/Program_Project/'
        date_from = "2022-05-21"
        date_to = "2022-06-22"
        author = "--pretty=\"%an\""
        datem = datetime.datetime.today()
        
        cur = os.getcwd()       
        dir = '{}\\{}'.format (cur, datem.month)
        
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)          
        
        repo = git.Repo(git_project_dir)
        status = repo.git.status()
        #log = repo.git.log('--since=2022-05-21','--author=Jeff','--pretty=tformat:','--numstat')
        
        name = repo.git.log('--since='+date_from,'--until='+date_to, author)
        author_list = filter_author(name)       
        add_line_list =[]
        delete_line_list =[]
        for author_name in team_member:
            expected_name = get_author_name(author_name , author_list)

            total_increase = 0
            total_delete = 0
            for x in expected_name:
                data = repo.git.log('--author='+x, '--pretty=tformat:','--numstat','--since='+date_from)
                each_ret = get_total_add_delete_line(data)
                
                total_increase = total_increase + each_ret[0]
                total_delete = total_delete + each_ret[1]
            
            add_line_list.append(total_increase)
            delete_line_list.append(total_delete)
            print('{}:{},{}'.format(author_name,total_increase,total_delete ))
            save_pie_chart(author_name,total_increase,total_delete)

        save_add_line_pie_chart(team_member, add_line_list, delete_line_list)

    except Exception as e:
        print(str(e))
