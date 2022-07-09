
import re


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
        
        # print('search:{} to {}'.format(start_index_search, end_index_search))
        
        sub_data = data[start_index_search:end_index_search]
        # print('search data:'+sub_data)
        # sub_data = data
        
        # idx_modify = sub_data.find('file', start_index_search, end_index_search)
        # idx_add = sub_data.find('insertions', start_index_search, end_index_search)
        # idx_delete = sub_data.find('deletion', start_index_search, end_index_search)
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
        # data = ' 8 files changed, 19 insertions(+), 9 deletions(-)\n 1 file changed, 1 insertion(+), 20 deletions(-)'
        data = ' 2 files changed, 2 insertions(+), 2 deletions(-)\n 4 files changed, 144 insertions(+), 80 deletions(-)\n 1 file changed, 5 insertions(+), 1 deletion(-)\n 3 files changed, 14 insertions(+), 6 deletions(-)\n 7 files changed, 124 insertions(+), 68 deletions(-)'
        # data = ' 2 files changed, 16 insertions(+), 16 deletions(-)'
        # data = ' 1 file changed, 30 deletions(-)\n 1 file changed, 22 insertions(+), 2 deletions(-)'
        
        ret = get_add_delete_data(data)
        print('Result:{}_{}_{}'.format(ret[0], ret[1], ret[2]))
    except Exception as e:
        print(str(e))
