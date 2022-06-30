import re

text = "\"jeff.yang\"\n\"jeff.yang\"\n\"derrick\"\n\"Johnwu\"\n\"derrick\"\n\"Jeff Yang\"\n\"Jeff Yang\""
text = "\"jeff.yang\"\n\"jeff.yang\"\n\"derrick\"\n\"derrick\"\n\"Johnwu\"\n\"derrick\"\n\"Derrick\"\n\"elvis\"\n\"jeff.yang\"\n\"Jeff Yang\"\n\"hoca\"\n\"derrick.chen\"\n\"Derrick\"\n\"Jeff Yang\"\n\"john.wu\"\n\"Johnwu\"\n\"Johnwu\"\n\"Johnwu1020\"\n\"Derrick\"\n\"Jeff Yang\"\n\"Derrick\"\n\"Derrick\"\n\"Derrick\"\n\"Jeff Yang\"\n\"john.wu\"\n\"Johnwu1020\"\n\"jeff.yang\"\n\"Cynthia\"\n\"Jeff Yang\"\n\"jeff.yang\"\n\"Cynthia\"\n\"Hoca.Chen\"\n\"IanChen0209\"\n\"IanChen0209\"\n\"derrick.chen\"\n\"IanChen0209\"\n\"jeff.yang\"\n\"Jeff Yang\"\n\"Jeff Yang\"\n\"Cynthia\"\n\"jeff.yang\"\n\"Jeff Yang\""
print(text)
print(text.count('\n'))
result = re.search('"(.*)"', text)
iter = re.finditer('"(.*)"', text)
indices = [m.start(0) for m in iter]
print(indices)

author_list = [] 
for i in range(0,text.count('\n')):
    st = text[indices[i]+1:indices[i+1]-2]
    if not author_list:
        author_list.append(st) 
    is_diff = False
    is_diff_int = 0
    for x in author_list:
        if x == st:
            is_diff_int = is_diff_int + 1

    if is_diff_int == 0:        
        author_list.append(st)
    
    #print(text[indices[i]+1:indices[i+1]-2])
print('List:/n')
print(author_list)
    