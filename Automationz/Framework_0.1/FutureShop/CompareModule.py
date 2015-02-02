import inspect
import copy
import CommonUtil    
from _elementtree import Element
class CompareModule():
    def compare(self, expected_list,actual_list,keywordlist=[],ignorelist=[]):
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        expected_copy=copy.deepcopy(expected_list)
        actual_copy=copy.deepcopy(actual_list)
        print expected_copy
        print actual_copy
        
        if len(keywordlist)==0:
            print "normal data is here"
            return single_dataset_compare(expected_copy[0],actual_copy[0])
        else:
            print "keyfield data is here"
            dataset_without_keyfield_expected=[]
            dataset_with_keyfield_expected=[]
            #strip out all the entry that do not have the keyword as specified
            for index in range(len(expected_copy)-1,-1,-1):
                each=expected_copy[index]
                temp_keyfield=find_keylist(each)
                if len(temp_keyfield)==0:
                    dataset_without_keyfield_expected.append(each)
                    expected_copy.pop(index)
                else:
                    matching_keyfield=list(set(temp_keyfield) & set(keywordlist))
                    extra_keyfield_in_expected=list(set(temp_keyfield)- set(keywordlist))
                    missing_keyfield_in_expected=list(set(keywordlist)-set(temp_keyfield))
                    if len(extra_keyfield_in_expected)==0 and len(missing_keyfield_in_expected)==0:
                        dataset_with_keyfield_expected.append(each)
                        expected_copy.pop(index)
                    else:
                        dataset_without_keyfield_expected.append(each)
                        expected_copy.pop(index)
            dataset_without_keyfield_actual=[]
            dataset_with_keyfield_actual=[]                    
            for index in range(len(actual_copy)-1,-1,-1):
                each=actual_copy[index]
                temp_keyfield=find_keylist(each)
                if len(temp_keyfield)==0:
                    dataset_without_keyfield_actual.append(each)
                    actual_copy.pop(index)
                else:
                    matching_keyfield=list(set(temp_keyfield) & set(keywordlist))
                    extra_keyfield_in_expected=list(set(temp_keyfield)- set(keywordlist))
                    missing_keyfield_in_expected=list(set(keywordlist)-set(temp_keyfield))
                    if len(extra_keyfield_in_expected)==0 and len(missing_keyfield_in_expected)==0:
                        dataset_with_keyfield_actual.append(each)
                        actual_copy.pop(index)
                    else:
                        dataset_without_keyfield_actual.append(each)
                        actual_copy.pop(index)
            #now match the copy of expected and actual datasets
            #for iExp in range(len(dataset_with_keyfield_expected)-1,-1,-1)
def single_dataset_compare(expected_copy,actual_copy):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    expected_list=copy.deepcopy(expected_copy)
    actual_list=copy.deepcopy(actual_copy)
    
    #take out the group data here
    expected_group_data=[]
    expected_tuple_data=[]
    for index in range(len(expected_list)-1,-1,-1):
        element=expected_list[index]
        #ignore_list compare here 
        if element[4]:
            expected_list.pop(index)
        else:
            if element[1]=='':
                expected_tuple_data.append((element[0],element[1],element[2]))
            else:
                expected_group_data.append((element[0],element[1],element[2]))
    actual_tuple_data=[]
    actual_group_data=[]
    for index in range(len(actual_list)-1,-1,-1):
        element=actual_list[index]
        #ignore_list compare here 
        if element[4]:
            actual_list.pop(index)
        else:
            if element[1]=='':
                actual_tuple_data.append((element[0],element[1],element[2]))
            else:
                actual_group_data.append((element[0],element[1],element[2]))
    matching_tuple_data=list(set(expected_tuple_data) & set(actual_tuple_data))
    missing_tuple_data=list(set(expected_tuple_data) - set(actual_tuple_data))
    extra_tuple_data=list(set(actual_tuple_data) - set(expected_tuple_data))
    
    matching_group_data=list(set(expected_group_data) & set(actual_group_data))
    missing_group_data=list(set(expected_group_data) - set(actual_group_data))
    extra_group_data=list(set(actual_group_data) - set(expected_group_data))
    
    matching_group_record_label=[]
    for each in matching_group_data:
        if each[0] not in matching_group_record_label:
            matching_group_record_label.append(each[0])
    final=[]
    for each in matching_group_record_label:
        temp_label=each
        temp=[]
        for eachitem in matching_group_data:
            if temp_label == eachitem[0]:
                temp.append((eachitem[1],eachitem[2]))
        final.append((temp_label,temp))
    matching_group_data=final
    
    missing_group_data_label=[]
    for each in missing_group_data:
        if each[0] not in missing_group_data_label:
            missing_group_data_label.append(each[0])
    
    final_missing_group_data=[]
    for each in missing_group_data_label:
        temp_label=each
        temp=[]
        for eachitem in missing_group_data:
            if temp_label==eachitem[0]:
                temp.append((eachitem[1],eachitem[2]))
        final_missing_group_data.append((temp_label,temp))
    
    extra_group_data_label=[]
    for each in extra_group_data:
        if each[0] not in extra_group_data_label:
            extra_group_data_label.append(each[0])
    final_extra_group_data=[]        
    for each in extra_group_data_label:
        temp_label=each
        temp=[]
        for eachitem in extra_group_data:
            if temp_label==eachitem[0]:
                temp.append((eachitem[1],eachitem[2]))
        final_extra_group_data.append((temp_label,temp))
    
    #match the group data missing compare
    group_data_not_matching=[]
    for  index in range(len(final_missing_group_data)-1,-1,-1):
        element=final_missing_group_data[index]
        for actindex in range(len(final_extra_group_data)-1,-1,-1):
            data_to_compare=final_extra_group_data[actindex]
            if element[0]==data_to_compare[0]:
                label=element[0]
                temp_expected=[]
                temp_actual=[]
                for i in range(len(element[1])-1,-1,-1):
                    for j in range(len(data_to_compare[1])-1,-1,-1):
                        if element[1][i][0]==data_to_compare[1][j][0]:
                            temp_expected.append(element[1][i])
                            temp_actual.append(data_to_compare[1][j])
                            element[1].pop(i)
                            data_to_compare[1].pop(j)
                expected_tuple=[label,temp_expected]
                actual_tuple=[label,temp_actual]
                group_data_not_matching.append((tuple(expected_tuple),tuple(actual_tuple)))
    
    if len(missing_tuple_data)>0 or len(extra_tuple_data)>0 or len(final_missing_group_data)>0 or len(final_extra_group_data) or len(group_data_not_matching)>0:
        status=3
    else:
        status=1
    CommonUtil.ExecLog(sModuleInfo,"Matching Records: %d"%len(matching_tuple_data),status)
    for i,each in enumerate(matching_tuple_data):
        CommonUtil.ExecLog(sModuleInfo,"#%d : %s : %s : %s"%((i+1),each[0],each[2],each[2]),status)
        
    CommonUtil.ExecLog(sModuleInfo,"Missing Records: %d"%len(missing_tuple_data),status)
    for i,each in enumerate(missing_tuple_data):
        element=each
        found=False
        for j,eachitem in enumerate(extra_tuple_data):
            if((element[0],element[1])==(eachitem[0],eachitem[1])):
                CommonUtil.ExecLog(sModuleInfo,"#%d : %s : %s : %s"%((j+1),element[0],element[2],eachitem[2]),status)
                extra_tuple_data.pop(j)
                found=True
                break
        if not found:
            CommonUtil.ExecLog(sModuleInfo,"#%d : %s : %s : %s"%((i+1),element[0],element[2],'N/A'),status)                
    CommonUtil.ExecLog(sModuleInfo,"Extra Records: %d"%len(extra_tuple_data),status)
    for i,each in enumerate(extra_tuple_data):
        CommonUtil.ExecLog(sModuleInfo,"#%d : %s : %s : %s"%((i+1),each[0],'N/A',each[2]),status)
    
    CommonUtil.ExecLog(sModuleInfo,"Matching Group Records: %d"%len(matching_group_data),status)
    for i,each in enumerate(matching_group_data):
        CommonUtil.ExecLog(sModuleInfo,"Matching Group Record: #%d"%(i+1),status)
        CommonUtil.ExecLog(sModuleInfo,"Matching Group Label: %s"%each[0],status)
        CommonUtil.ExecLog(sModuleInfo,"Matching Group Entry Count: %d"%len(each[1]),status) 
        for j,eachitem in enumerate(each[1]):
            CommonUtil.ExecLog(sModuleInfo,"#%d : %s : %s : %s"%((j+1),eachitem[0],eachitem[1],eachitem[1]),status)
    final_list=[] 
    for each in group_data_not_matching:
        temp_label=each[0][0]
        expected_data=each[0][1]
        actual_data=each[1][1]
        temp=[]
        for eachitem in expected_data:
            for eachitemtemp in actual_data:
                if eachitem[0]==eachitemtemp[0]:
                    temp.append((eachitem[0],eachitem[1],eachitemtemp[1]))
        final_list.append((temp_label,temp))
    CommonUtil.ExecLog(sModuleInfo,"Non Match Group Data: %d"%len(final_list),status)
    for each in final_list:
        CommonUtil.ExecLog(sModuleInfo,"Non Match Group Label: %s"%each[0],status)
        CommonUtil.ExecLog(sModuleInfo,"Non Match Group Entry Count: %d"%len(each[1]),status) 
        for i,eachitem in enumerate(each[1]):
            CommonUtil.ExecLog(sModuleInfo,"#%d : %s : %s :%s"%((i+1),eachitem[0],eachitem[1],eachitem[2]),status)
    CommonUtil.ExecLog(sModuleInfo,"Missing Group Data: %d"%len(final_missing_group_data),status)
    for each in final_missing_group_data:
        CommonUtil.ExecLog(sModuleInfo,"Missing Group Label: %s"%each[0],status)
        CommonUtil.ExecLog(sModuleInfo,"Missing Group Entry Count: %d"%len(each[1]),status) 
        for i,eachitem in enumerate(each[1]):
            CommonUtil.ExecLog(sModuleInfo,"#%d : %s : %s : %s"%((i+1),eachitem[0],eachitem[1],'N/A'),status)
    CommonUtil.ExecLog(sModuleInfo,"Extra Group Data: %d"%len(final_extra_group_data),status)
    for each in final_extra_group_data:
        CommonUtil.ExecLog(sModuleInfo,"Extra Group Label: %s"%each[0],status)
        CommonUtil.ExecLog(sModuleInfo,"Extra Group Entry Count: %d"%len(each[1]),status)         
        for i,eachitem in enumerate(each[1]):
            CommonUtil.ExecLog(sModuleInfo,"#%d : %s : %s : %s"%((i+1),eachitem[0],'N/A',eachitem[1]),status)
    
    if status==1:
        return "Passed"
    else:
        return "Failed"
    
def find_keylist(list_element):
    key_list=[]
    for each in list_element:
        if each[1]=='':
            if each[3] and not each[4]:
                if each[0] not in key_list:
                        key_list.append(each[0])
    return key_list
                    
def main():
    oCompare=CompareModule()
    
    expected_list=[
                   [
                    ('Address', 'hall', 'titumir', False, False),
                    ('Address', 'district', 'cox\'s bazar', False, False),
                    ('name', '', 'shetu', True, False), 
                    ('roll', '', '0905011', True, False),
                    ('Academic', 'dept', 'cse', False, False),
                    ('Academic', 'cg', '3.25', False, False)
                    ]
                   ]
    actual_list=[
                 [
                    ('name', '', 'minar', True, False), 
                    ('roll', '', '0905011', True, False),
                    ('first name','','matiur',False,False),
                    ('Academic', 'dept', 'cse', False, False),
                    ('Academic', 'cg', '3.24', False, False),
                    ('Contact','mobile','01719-267494',False,False),
                    ('Contact','land','0421-71194',False,False)                  
                 ]
                ]
    keyword_list=[]
    status=oCompare.compare(expected_list,actual_list,keyword_list)
    print status
if __name__=='__main__':
    main()