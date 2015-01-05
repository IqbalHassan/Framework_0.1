import copy
class CompareModule():
    def FieldCompare(self,expected_list,actual_list,ignore_list=[],keyfield_list=[]):
        expected_list_group_data_label=[]
        actual_list_group_data_label=[]
        
        #copying the actaul listings here
        expList=copy.deepcopy(expected_list)
        actList=copy.deepcopy(actual_list)
        
        #now find the group data label
        for each in expList:
            if each[1]!='':
                if each[0] not in expected_list_group_data_label:
                    expected_list_group_data_label.append(each[0])
        expected_list_group_data_label=list(set(expected_list_group_data_label))
        for each in actList:
            if each[1]!='':
                if each[0] not in actual_list_group_data_label:
                    actual_list_group_data_label.append(each[0])
        actual_list_group_data_label=list(set(actual_list_group_data_label))
        
        match_group_data_list=list(set(expected_list_group_data_label) & set(actual_list_group_data_label))
        missing_group_data_list=list(set(expected_list_group_data_label) - set(actual_list_group_data_label))
        extra_group_data_list=list(set(actual_list_group_data_label)-set(expected_list_group_data_label))
        #finishing finding the group data label 
        
        #print match_group_data_list
        #print missing_group_data_list
        #print extra_group_data_list
        
        #listing all the missing and extra group data tuples are started
        missing_group_data=[]
        for each in missing_group_data_list:
            for i in range(len(expList)-1,-1,-1):
                if each==expList[i][0]:
                    missing_group_data.append(expList.pop(i))
        #print missing_group_data
        
        extra_group_data=[]
        for each in extra_group_data_list:
            for i in range(len(actList)-1,-1,-1):
                if each==actList[i][0]:
                    extra_group_data.append(actList.pop(i))
        #print extra_group_data
        #listing all missing and extra group data tuples are finished here
        
        #listing all the group data to be compared started
        expected_group_data=[]
        for each in match_group_data_list:
            for  i in range(len(expList)-1,-1,-1):
                if each==expList[i][0]:
                    expected_group_data.append(expList.pop(i))
        actual_group_data=[]
        for each in match_group_data_list:
            for i in range(len(actList)-1,-1,-1):
                if each==actList[i][0]:
                    actual_group_data.append(actList.pop(i))
        
        match_group_data=list(set(expected_group_data) & set(actual_group_data))
        match_missing_group_data=list(set(expected_group_data)- set(actual_group_data))
        match_extra_group_data=list(set(actual_group_data)-set(expected_group_data))
        
        #print match_group_data
        #print match_missing_group_data
        #print match_extra_group_data            
        #listing all the group data finished here
        
        #rest is printed here
        matched_tuple=list(set(expList) & set(actList))
        missing_tuple=list(set(expList)-set(actList))
        extra_tuple=list(set(actList)-set(expList))
        #rest is finished here
        
        #summarizing the result here
        total_match=list(set(match_group_data+matched_tuple))
        total_missing=list(set(missing_tuple+missing_group_data+match_missing_group_data))
        total_extra=list(set(extra_tuple+extra_group_data+match_extra_group_data))
        #summarizing the result end here
        
        print "total_match:%d"%len(total_match)
        for each in total_match:
            print each
        print "total_missing:%d"%len(total_missing)
        for each in total_missing:
            print each
        print "total_extra:%d"%len(total_extra)
        for each in total_extra:
            print each
        return "Failed"
    
def main():
    oCompare=CompareModule()
    """actual_list=[
        ('Academic', 'Institution', 'BUET'),
        ('Academic', 'Roll', '0905011'),
        ('Address', 'District', 'Jessore'),
        ('Address', 'Country', 'Bangladesh'),
        ('Address', 'Road No', '721'),
        ('First Name', '', 'Raju'),
        ('Last Name', '', 'Shetu'),
        ('Middle Name', '', 'Ahmed'),
        ('Sur Name','','Mollah'),
        ('Phone', 'Mobile', '01719-267494'),
        ('Phone', 'Home', '04221-71194'),
    ]
    expected_list=[
        ('Academic', 'Department', 'CSE'),
        ('Academic', 'Institution', 'BUET'),
        ('Academic', 'Roll', '0905011'),
        ('Address', 'Area', 'Bezpara'),
        ('Address', 'District', 'Jessore'),
        ('Address', 'Division', 'Khulna'),
        ('Address', 'Road No', '721'),
        ('First Name', '', 'Raju'),
        ('Last Name', '', 'Shetu'),
        ('Middle Name', '', 'Ahmed'),
        ('Phone', '', '01719-267494'),
        ('Work','Address','Automation Solution'),
        ('Work','Designation','Programmer')
    ]"""
    actual_list=[
        ('Academic', 'Institution', 'BUET'),#match
        ('Academic', 'Roll', '0905011'),#match
        ('Address', 'District', 'Jessore'),#match
        ('Address', 'Road No', '721'),#match
        ('First Name', '', 'Raju'),#match
        ('Last Name', '', 'Shetu'),#match
        ('Middle Name', '', 'Ahmed'),#match        
        ('Address', 'Country', 'Bangladesh'),#extra
        ('Sur Name','','Mollah'),#extra
        ('Phone', 'Mobile', '01719-267494'),#extra
        ('Phone', 'Home', '04221-71194'),#extra
    ]#7 match 4 extra
    expected_list=[
        ('Phone', '', '01719-267494'),#missing
        ('Academic', 'Department', 'CSE'),#missing
        ('Address', 'Area', 'Bezpara'),#missing
        ('Address', 'Division', 'Khulna'),#missing
        ('Academic', 'Institution', 'BUET'),#match
        ('Academic', 'Roll', '0905011'),#match
        ('Address', 'District', 'Jessore'),#match
        ('Address', 'Road No', '721'),#match
        ('First Name', '', 'Raju'),#match
        ('Last Name', '', 'Shetu'),#match
        ('Middle Name', '', 'Ahmed'),#match
        
    ]#7 match 4 missing

    status=oCompare.FieldCompare(expected_list, actual_list, [],[])
    print status
if __name__=='__main__':
    main()