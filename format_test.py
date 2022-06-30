import re
text = '4\t4\tGMPIMachineSeqCtrl/GMPIMachineSeqCtrl.cpp\n3\t2\tMPIASTSystem/ED_IndexEnum.h\n2\t1\tMPIASTSystem/ED_SystemEnum.h\n23\t26\tMPIModuleSeqCtrl/ChuckStageCommonSeqCtrl.cpp\n4\t4\tMPIModuleSeqCtrl/WorkArea.cpp\n1\t1\tMPIModuleSeqCtrl/MoveToPos.cpp'

iter = re.finditer('\t(.*)\t', text)
indices = [m.start(0) for m in iter]
print(indices)

increase_line_list = [] 
delete_line_list = [] 
for i in range(0,len(indices)):
    st = text[indices[i]-1:indices[i]]
    increase_line_list.append(st)
    st = text[indices[i]+1:indices[i]+2]
    delete_line_list.append(st)

total_increase = 0  
total_delete = 0  
for x in increase_line_list:
    total_increase = total_increase + int(x)
for x in delete_line_list:
    total_delete = total_delete + int(x)
    
print('add line:')
print(increase_line_list)
print('delete line:')
print(delete_line_list)