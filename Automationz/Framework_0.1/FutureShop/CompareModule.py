import inspect
import copy
import CommonUtil

class CompareModule():
    def FieldCompare(self,expected_list,actual_list,ignore_list=[],keyfield_list=[]):
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
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
        
        print "Expected           records:", len(expected_list)
        CommonUtil.ExecLog(sModuleInfo, "Expected           records:%s" % len(expected_list), 1)
        for i in range(len(expected_list)):
            CommonUtil.ExecLog(sModuleInfo, "Expected           records#%s:%s" % (i, expected_list[i]), 4)
        print "Actual             records:", len(actual_list)
        CommonUtil.ExecLog(sModuleInfo, "Actual             records:%s" % len(actual_list), 1)
        for i in range(len(actual_list)):
            CommonUtil.ExecLog(sModuleInfo, "Actual             records#%s:%s" % (i, actual_list[i]), 4)

        if (len(total_missing)==0 and len(total_extra)==0):
            print "Found              records:", len(matched_tuple)+len(match_group_data)
            CommonUtil.ExecLog(sModuleInfo, "Found              records:%s" % (len(matched_tuple)+len(match_group_data)), 1)
            for i in range(len(matched_tuple)):
                CommonUtil.ExecLog(sModuleInfo, "Matching           records#%s" % (i + 1), 1)
                CommonUtil.ExecLog(sModuleInfo, "%s" % (str(matched_tuple[i])), 1)
            for i in range(len(match_group_data)):
                CommonUtil.ExecLog(sModuleInfo, "Matching           records#%s" % (i + 1), 1)
                CommonUtil.ExecLog(sModuleInfo, "%s" % (str(match_group_data[i])), 1)
            print "Missing            records:", len(total_missing)
            CommonUtil.ExecLog(sModuleInfo, "Missing            records:%s" % len(total_missing), 1)
            print "Verification of expected and actual  data matched"
            CommonUtil.ExecLog(sModuleInfo, "Verification of expected and actual  data matched", 1)

            sVerificationStatus = "Passed"
        else:
            sVerificationStatus = "Failed"
        return sVerificationStatus
    
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