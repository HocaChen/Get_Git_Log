
author_list = ['jeff.yang', 'Jeff.Yang', 'Jeff', 'derrick', 'Hoca']
author = 'jeff'

get_author_name = []
for x in author_list:
    if author in x.lower():
        get_author_name.append(x)