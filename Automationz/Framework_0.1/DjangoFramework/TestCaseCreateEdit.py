'''
Created on May 1, 2014
Author: @Taitalus
'''
import DataBaseUtilities as DBUtil
import CommonUtil
import inspect
import datetime
from MySite.models import GetConnection
import time
from TestCaseOperations import LogMessage
"""
    1- info
    2 - warning
    3 - error
"""
def Update_Test_Case_Tag(Conn, TC_Id, Platform, Manual_TC_Id, TC_Type, Custom_Tag_List, Dependency_List, Priority, Associated_Bugs_List, Status, Section_Path, Requirement_ID_List):
    sModuleInfo = inspect.stack()[0][3] + " : " +inspect.getmoduleinfo(__file__).name
    Tag_List = []
    #Add test case id tag
    Tag_List.append(('%s' % TC_Id, 'tcid'))
    ManualTCIDFound = False
    for eachManual_Id in [Manual_TC_Id]:
        if eachManual_Id.strip() != '':
            Tag_List.append(('%s' % eachManual_Id, 'MKS'))
            ManualTCIDFound = True
    if ManualTCIDFound == False:
        Tag_List.append(('%s' % TC_Id, 'MKS'))

    #hard coded tags for now
    Tag_List.append(('Default', 'Data_Type'))

    #Add Section names & initialize variables
    if Platform.lower() == 'pc':
        Tag_List.append(('PC', 'machine_os'))
        Section_Tag = 'Section'
        Custom_Tag = 'CustomTag'
        Section_Path_Tag = 'section_id'
        TestRunType_Tag = 'test_run_type'
        Priority_Tag = 'Priority'
        Dependency_Tag = 'Dependency'
        Tag_List.append(('Status', Status))
        if Status=="Forced":
            Tag_List.append(('Status', 'Ready'))
    elif Platform.lower() == 'mac':
        Tag_List.append(('MAC', 'machine_os'))
        Section_Tag = 'MacSection'
        Custom_Tag = 'MacCustomTag'
        Section_Path_Tag = 'mac_section_id'
        TestRunType_Tag = 'Mac_test_run_type'
        Priority_Tag = 'MacPriority'
        Dependency_Tag = 'MacDependency'
        Tag_List.append(('MacStatus', Status))
        if Status=="Forced":
            Tag_List.append(('Status', 'Ready'))
    else:
        err_msg = LogMessage(sModuleInfo, "Unknown platform value for the test case: %s" % (Platform), 4)
        return err_msg

    #Add test case type, priority, Data Type
    for each_TC_Type in TC_Type.split("|"):
        Tag_List.append(('%s' % each_TC_Type, TestRunType_Tag))
    Tag_List.append(('%s' % Priority, Priority_Tag))

    #Add custom tags
    for eachTag in Custom_Tag_List:
        Tag_List.append(('%s' % eachTag, Custom_Tag))

    #Add Section id based on hierarchy
    if DBUtil.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()
    Section_Id = DBUtil.GetData(Conn, "select section_id from product_sections where section_path = '%s'" % Section_Path)
    if len(Section_Id) > 0:
        Tag_List.append(('%d' % Section_Id[0], Section_Path_Tag))

    #Work around to display section names in run page
    for eachSection in Section_Path.split('.'):
        Tag_List.append(('%s' % eachSection, Section_Tag))

    #Add Dependency tags
    for eachDependency in Dependency_List:
        Tag_List.append(('%s' % Dependency_Tag, eachDependency))
        if eachDependency in ['Outlook', 'MacNative', 'iTunes', 'iPhoto', 'WMP', 'Chrome', 'FireFox', 'IE']:
            Tag_List.append(('%s' % eachDependency, 'client'))
        elif eachDependency in ['BBX', 'SD']:
            Tag_List.append(('%s' % eachDependency, 'device_memory'))

    #Add Associated Bugs
    for eachBugId in Associated_Bugs_List:
        Tag_List.append(('%s' % eachBugId, 'JiraId'))

    #Add Associated Requirements
    for eachReqId in Requirement_ID_List:
        Tag_List.append(('%s' % eachReqId, 'PRDId'))
    test_case_tag_query="select tc_id,name,property from test_case_tag where tc_id='%s'"%TC_Id
    if DBUtil.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()
    test_case_tag_collected_data=DBUtil.GetData(Conn,test_case_tag_query,False)
    print test_case_tag_collected_data
    print Tag_List
    test_case_tag_dict={}
    for each in Tag_List:
        if (TC_Id,each[0],each[1]) not in test_case_tag_collected_data:
            test_case_tag_dict.update({'tc_id':TC_Id,'name':each[0],'property':each[1]})
            if DBUtil.IsDBConnectionGood(Conn)==False:
                time.sleep(1)
                Conn=GetConnection()
            result=DBUtil.InsertNewRecordInToTable(Conn, "test_case_tag",**test_case_tag_dict)
            if result==True:
                LogMessage(sModuleInfo,"Added %s in test case tag for test case %s"%(str(test_case_tag_dict),TC_Id),1)
            else:
                LogMessage(sModuleInfo,result,3)
        else:
            test_case_tag_collected_data.remove((TC_Id,each[0],each[1]))
            LogMessage(sModuleInfo,"%s is present already for the test case %s"%(str((TC_Id,each[0],each[1])),TC_Id),1)
    test_case_tag_column=['tc_id','name','property']
    for each in test_case_tag_collected_data:
        test_case_tag_dict={}
        for eachitem in zip(test_case_tag_column,each):
            test_case_tag_dict.update({eachitem[0]:eachitem[1]})
        if DBUtil.IsDBConnectionGood(Conn)==False:
            time.sleep(1)
            Conn=GetConnection()
        result=DBUtil.DeleteRecord(Conn,"test_case_tag",**test_case_tag_dict)
        if result==True:
            LogMessage(sModuleInfo,"Deleting Unnecessary %s tuple from test case tag for test case %s"%(str(test_case_tag_dict),TC_Id),1)
        else:
            LogMessage(sModuleInfo,result,3)
    return "Pass"
def Update_Test_Steps_Data(Conn,tc_id,dataset_id,steps_data_list):
    sModuleInfo = inspect.stack()[0][3] + " : " +inspect.getmoduleinfo(__file__).name
    #Collect the master data table entry and the test_steps_table_entry
    test_step_collect_query="select tc_id,step_id,teststepsequence from test_steps where tc_id='%s' order by teststepsequence"%tc_id
    #test_steps_data_collect_query=""
    if DBUtil.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()
    test_step_collected_data=DBUtil.GetData(Conn,test_step_collect_query,False)
    updated_test_step_list=[]
    Step_Index=1
    for each in steps_data_list:
        step_name=each[0]
        step_data=each[1]
        step_description=each[2]
        step_expected=each[3]
        step_verification=each[4]
        step_time=each[5]
        #get the step_id for the current step_name
        step_id_query="select step_id,data_required from test_steps_list where stepname='%s'"%step_name
        if DBUtil.IsDBConnectionGood(Conn)==False:
            time.sleep(1)
            Conn=GetConnection()
        step_info=DBUtil.GetData(Conn,step_id_query,False)
        #check the test_steps_table
        if len(step_info)==0:
            LogMessage(sModuleInfo,"No Step Name is found in the test_steps_list for test case %s with name %s"%(tc_id,step_name),3)
        else:
            test_steps_table_tuple=(tc_id,step_info[0][0])
            if (test_step_collected_data[Step_Index-1][0],test_step_collected_data[Step_Index-1][1]) == test_steps_table_tuple :
                #del test_step_collected_data[Step_Index-1]
                Step_Seq=test_step_collected_data[Step_Index-1][2]
                updated_test_step_list.append((test_step_collected_data[Step_Index-1][0],test_step_collected_data[Step_Index-1][1],Step_Seq))     
                LogMessage(sModuleInfo,"Test Steps is not changed for the Step Index %s of test case %s"%(Step_Index,tc_id),1)
            else:
                #insert the test_steps in the table,first form the dict
                test_step_dict={'tc_id':tc_id,'step_id':step_info[0][0]}
                if DBUtil.IsDBConnectionGood(Conn)==False:
                    time.sleep(1)
                    Conn=GetConnection()
                result=DBUtil.InsertNewRecordInToTable(Conn,"test_steps",**test_step_dict)
                if result==True:
                    updated_test_step_list.append(test_steps_table_tuple)
                    test_step_sequence_get_query="select teststepsequence from test_steps where tc_id='%s' order by teststepsequence desc limit 1"%tc_id
                    if DBUtil.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    test_step_sequence=DBUtil.GetData(Conn,test_step_sequence_get_query)
                    Step_Seq=test_step_sequence[0]
                    updated_test_step_list.append((test_step_collected_data[Step_Index-1][0],test_step_collected_data[Step_Index-1][1],Step_Seq))    
                    LogMessage(sModuleInfo,"Added new test step at position %s during updating the test case %s"%(Step_Index,tc_id),1)
                else:
                    err_msg="Failed to add new test step at postion %s while updating test_case %s"%(Step_Index,tc_id)
                    LogMessage(sModuleInfo,err_msg,3)
                    return err_msg
            #get the test step sequenece
            master_id=('%s_s'%tc_id)+str(Step_Index)
            master_data_collect_query="select * from master_data where id Ilike '%s%%'"%master_id 
            if DBUtil.IsDBConnectionGood(Conn)==False:
                time.sleep(1)
                Conn=GetConnection()
            master_data_collected_data=DBUtil.GetData(Conn,master_data_collect_query,False)
            print master_data_collected_data
            if step_info[0][1]:
                print "data step"
                current_step_data=PrepareDataStep(master_id, step_data)
                if len(current_step_data)>0:
                    for each in current_step_data:
                        if each not in master_data_collected_data:
                            master_data_column=['id','field','value','description']
                            master_data_dict={}
                            for eachitem in zip(master_data_column,each):
                                master_data_dict.update({eachitem[0]:eachitem[1]})
                            if DBUtil.IsDBConnectionGood(Conn)==False:
                                time.sleep(1)
                                Conn=GetConnection()
                            result=DBUtil.InsertNewRecordInToTable(Conn,"master_data",**master_data_dict)
                            if result==True:
                                LogMessage(sModuleInfo,"Tuple %s is added in master_data for step %s of test_case %s"%(str(each),Step_Index,tc_id),1)
                            else:
                                LogMessage(sModuleInfo,result,3)
                        else:
                            master_data_collected_data.remove(each)
                            LogMessage(sModuleInfo,"Tuple %s is present in the master_data before for step %s of test_case %s"%(str(each),Step_Index,tc_id),1)
                else:
                    err_msg="Test Case Data is not in Valid Format"
                    LogMessage(sModuleInfo,err_msg,3)
                #edit the test step data
                #form the entry
                test_steps_data_entry={'tcdatasetid':dataset_id,'testdatasetid':master_id,'teststepseq':Step_Seq}
                test_steps_data_collect_query="select tcdatasetid,testdatasetid,teststepseq from test_steps_data where testdatasetid='%s'"%master_id
                if DBUtil.IsDBConnectionGood(Conn)==False:
                    time.sleep(1)
                    Conn=GetConnection()
                test_steps_data_collected_data=DBUtil.GetData(Conn,test_steps_data_collect_query,False)
                if (test_steps_data_entry['tcdatasetid'],test_steps_data_entry['testdatasetid'],test_steps_data_entry['teststepseq']) not in test_steps_data_collected_data:
                    #print insert the test steps data
                    if DBUtil.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    result=DBUtil.InsertNewRecordInToTable(Conn,"test_steps_data",**test_steps_data_entry)
                    if result==True:
                        LogMessage(sModuleInfo,"Added %s in test_steps_data while updating step %s for test case %s"%(str(test_steps_data_entry),Step_Index,tc_id),1)
                    else:
                        LogMessage(sModuleInfo,result, 3)
                else:
                    LogMessage(sModuleInfo,"Tuple %s is present already in the test_steps_data table for step %s for test case %s"%(str(test_steps_data_entry),Step_Index,tc_id),1)
                    test_steps_data_collected_data.remove((test_steps_data_entry['tcdatasetid'],test_steps_data_entry['testdatasetid'],test_steps_data_entry['teststepseq']))
                test_steps_data_column=['tcdatasetid','testdatasetid','teststepseq']
                for each in zip(test_steps_data_column,test_steps_data_collected_data):
                    test_steps_data_dict={}
                    test_steps_data_dict.update({each[0]:each[1]})
                    if DBUtil.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    result=DBUtil.DeleteRecord(Conn,"test_steps_data",**test_steps_data_dict)
                    if result==True:
                        LogMessage(sModuleInfo,"Deleted %s from test_steps_data for step %s updating test case %s"%(str(test_steps_data_dict),Step_Index,tc_id),1)
                    else:
                        LogMessage(sModuleInfo,result,3)
                #container data change
                if isinstance(step_data,list) and not isinstance(step_data[0],tuple):
                    #form tuple for the container type data table
                    DataSet=1
                    container_list=[]
                    #new_name=None
                    for each in step_data:
                        curname=master_id+('_d')+str(DataSet)
                        container_list.append((master_id,curname))
                        DataSet+=1
                    container_type_data_query="select dataid,curname from container_type_data where dataid='%s'"%master_id
                    if DBUtil.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    container_type_data=DBUtil.GetData(Conn,container_type_data_query,False)
                    container_data_column=['dataid','curname']
                    for each in container_list:
                        if each not in container_type_data:
                            container_type_data_dict={}
                            for eachitem in zip(container_data_column,each):
                                container_type_data_dict.update({eachitem[0]:eachitem[1]})
                            if DBUtil.IsDBConnectionGood(Conn)==False:
                                time.sleep(1)
                                Conn=GetConnection()
                            result=DBUtil.InsertNewRecordInToTable(Conn,"container_type_data",**container_type_data_dict)
                            if result==True:
                                LogMessage(sModuleInfo,"Added %s tuple to container_type_data while updating test case %s Step %s"%(str(container_type_data_dict),tc_id,Step_Index),1)
                            else:
                                LogMessage(sModuleInfo,result,3)
                        else:
                            container_type_data.remove(each)
                            LogMessage(sModuleInfo,"Tuple %s found in container_type_data already for step %s in test case %s"%(str(each),Step_Index,tc_id),1)
                    for each in container_type_data:
                        container_data_dict={}
                        for eachitem in zip(container_data_column,each):
                            container_data_dict.update({eachitem[0]:eachitem[1]})
                        #del container_data_dict['newname']
                        if DBUtil.IsDBConnectionGood(Conn)==False:
                            time.sleep(1)
                            Conn=GetConnection()
                        result=DBUtil.DeleteRecord(Conn,"container_type_data",**container_data_dict)
                        if result==True:
                            LogMessage(sModuleInfo,"Deleted Unnecessary entry %s from container_type_data while updating step %s in test case %s"%(str(each),Step_Index,tc_id),1)
                        else:
                            LogMessage(sModuleInfo,result,3)    
                if isinstance(step_data[0],tuple) and len(step_data[0])==2:
                    print "datasets to be changed for the edit data"
                    curname=master_id+('_d1_fr')
                    newname=master_id+('_d1_to')
                    container_type_data_query="select dataid,curname,newname from container_type_data where dataid='%s'"%master_id
                    container_type_tuple=(master_id,curname,newname)
                    if DBUtil.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    container_type_data=DBUtil.GetData(Conn,container_type_data_query,False)
                    container_data_column=['dataid','curname','newname']
                    if container_type_tuple not in container_type_data:
                        container_type_data_dict={}
                        for each in zip(container_data_column,container_type_tuple):
                            container_type_data_dict.update({each[0]:each[1]})
                        if DBUtil.IsDBConnectionGood(Conn)==False:
                            time.sleep(1)
                            Conn=GetConnection()
                        result=DBUtil.InsertNewRecordInToTable(Conn,"container_type_data",**container_type_data_dict)
                        if result==True:
                            LogMessage(sModuleInfo,"Added %s tuple to container_type_data while updating test case %s Step %s"%(str(container_type_data_dict),tc_id,Step_Index),1)
                        else:
                            LogMessage(sModuleInfo,result,3)        
                    else:
                        container_type_data.remove(container_type_tuple)
                        LogMessage(sModuleInfo,"Tuple %s found in container_type_data already for step %s in test case %s"%(container_type_tuple,Step_Index,tc_id),1)
                    for each in container_type_data:
                        container_data_dict={}
                        for eachitem in zip(container_data_column,each):
                            container_data_dict.update({eachitem[0]:eachitem[1]})
                        #del container_data_dict['newname']
                        if DBUtil.IsDBConnectionGood(Conn)==False:
                            time.sleep(1)
                            Conn=GetConnection()
                        result=DBUtil.DeleteRecord(Conn,"container_type_data",**container_data_dict)
                        if result==True:
                            LogMessage(sModuleInfo,"Deleted Unnecessary entry %s from container_type_data while updating step %s in test case %s"%(str(each),Step_Index,tc_id),1)
                        else:
                            LogMessage(sModuleInfo,result,3)
            #form master_id
            master_data_current_data=PrepareNonDataStep(master_id, step_description, step_expected, step_verification, step_time)
            print master_data_current_data
            #updated_master_data_list=[]
            for each in master_data_current_data:
                if each not in master_data_collected_data:
                    #data to be inserted
                    master_data_column=['id','field','value','description']
                    master_data_dict={}
                    for eachitem in zip(master_data_column,each):
                        master_data_dict.update({eachitem[0]:eachitem[1]})
                    if DBUtil.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    result=DBUtil.InsertNewRecordInToTable(Conn,"master_data",**master_data_dict)
                    if result==True:
                        LogMessage(sModuleInfo,"Added Master Data Entry while Updating step %s in test case %s"%(Step_Index,tc_id),1)
                    else:
                        LogMessage(sModuleInfo,"Failed to add Master Data while Updating step %s in test case %s"%(Step_Index,tc_id),3)    
                else:
                    master_data_collected_data.remove(each)
                    LogMessage(sModuleInfo,"Master Data Table already contains the tuple for step %s in test case %s"%(Step_Index,tc_id),1)
            print master_data_collected_data
            ##Cleaning up the unnecessary data from the master_data:
            master_data_column=['id','field','value','description']
            for each in master_data_collected_data:
                master_data_dict={}
                for eachitem in zip(master_data_column,each):
                    master_data_dict.update({eachitem[0]:eachitem[1]})
                del master_data_dict['description']
                if DBUtil.IsDBConnectionGood(Conn)==False:
                    time.sleep(1)
                    Conn=GetConnection()
                result=DBUtil.DeleteRecord(Conn,"master_data",**master_data_dict)
                if result==True:
                    LogMessage(sModuleInfo,"Deleting unnecessary %s tuple from masterdata for step %s"%(each,Step_Index),1)
                else:
                    LogMessage(sModuleInfo,result,3)
        Step_Index+=1
    test_step_column=['tc_id','step_id','teststepsequence']
    for each in test_step_collected_data:
        if each not in updated_test_step_list:
            for eachitem in zip(test_step_column,each):
                test_steps_dict={}
                test_steps_dict.update({eachitem[0]:eachitem[1]})
            if DBUtil.IsDBConnectionGood(Conn)==False:
                time.sleep(1)
                Conn=GetConnection()
            result=DBUtil.DeleteRecord(Conn,"container_type_data",**test_steps_dict)
            if result==True:
                LogMessage(sModuleInfo,"Deleting unnecessary %s tuple from masterdata for step %s"%(each,Step_Index),1)
            else:
                LogMessage(sModuleInfo,result,3)
    return "Pass"
def PrepareDataStep(master_data_id,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    dataset_id=1
    address_index=1
    final_list=[]
    description=None
    for each in step_data:
        print each
        if isinstance(each,list):
            print "normal_data"
            group_data_id=master_data_id+('_d')+str(dataset_id)
            for eachitem in each:
                if isinstance(eachitem[0],basestring) and isinstance(eachitem[1],basestring):
                    final_list.append((group_data_id,eachitem[0],eachitem[1],description))
                    print final_list
                elif isinstance(eachitem[0],basestring) and isinstance(eachitem[1],list):
                    #form the group data entry at first
                    address_data_id=group_data_id+('_a')+str(address_index)
                    #Enter the group data entry to final list
                    final_list.append((group_data_id,eachitem[0],address_data_id,description))
                    print final_list
                    for eachitementry in eachitem[1]:
                        final_list.append((address_data_id,eachitementry[0],eachitementry[1],description))
                    print final_list
                    address_index+=1
                else:
                    LogMessage(sModuleInfo,"No Valid data Format in the normal data for step %s"%master_data_id,3)
        elif isinstance(each,tuple) and len(each)==2:
            from_data=each[0]
            to_data=each[1]
            if not isinstance(from_data,list) or not isinstance(to_data,list):
                LogMessage(sModuleInfo,"Wrong data format in from and to data in step %s.Should be a list"%master_data_id,3)
                final_list=[]
                return final_list
            from_data_id=master_data_id+('_d')+str(dataset_id)+('_fr')
            for eachitem in from_data:
                if isinstance(eachitem[0],basestring) and isinstance(eachitem[1],list):
                    #give entry for the grouped from data index
                    from_data_index=from_data_id+('_a')+str(address_index)
                    final_list.append((from_data_id,eachitem[0],from_data_index,description))
                    for eachitementry in eachitem[1]:
                        final_list.append((from_data_index,eachitementry[0],eachitementry[1],description))
                    address_index+=1
                elif isinstance(eachitem[0],basestring) and isinstance(eachitem[1],basestring):
                    final_list.append((from_data_id,eachitem[0],eachitem[1],description))
                else:
                    LogMessage(sModuleInfo,"Wrong data format in from data while updating step %s.should be tuple or list"%master_data_id,3)
            to_address_index=1
            to_data_id=master_data_id+('_d')+str(dataset_id)+('_to')
            for eachitem in to_data:
                if isinstance(eachitem[0],basestring) and isinstance(eachitem[1],list):
                    #give entry for the grouped from data index
                    to_data_index=to_data_id+('_a')+str(to_address_index)
                    final_list.append((to_data_id,eachitem[0],to_data_index,description))
                    for eachitementry in eachitem[1]:
                        final_list.append((to_data_index,eachitementry[0],eachitementry[1],description))
                    to_address_index+=1
                elif isinstance(eachitem[0],basestring) and isinstance(eachitem[1],basestring):
                    final_list.append((to_data_id,eachitem[0],eachitem[1],description))
                else:
                    LogMessage(sModuleInfo,"Wrong data format in from data while updating step %s.should be tuple or list"%master_data_id,3)
        else:
            LogMessage(sModuleInfo,"No Valid data Format during editing for step %s"%master_data_id,3)
            final_list=[]
            return final_list
        dataset_id+=1
    return final_list
def PrepareNonDataStep(master_data_id,description,expected,verification,time):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    fields=['step','expected','verification','estimated']
    value=['description','result','point','time']
    description_values=[description,expected,verification,time]
    final_list=[]                    
    for each in zip(fields,value,description_values):
        final_list.append((master_data_id,each[0],each[1],each[2]))
    return final_list
def Update_Test_Case_Datasets(Conn,dataset_id,tc_id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    #check already existing or not.
    existing_dataset_query="select tcdatasetid from test_case_datasets where tc_id='%s'"%tc_id
    if DBUtil.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()
    existing_dataset=DBUtil.GetData(Conn,existing_dataset_query)
    found=False
    for each in existing_dataset:
        if each==dataset_id:
            found=True
            break
    if not found:
        #data is to be inserted.
        #form dict to insert the test_case_datasets
        test_case_dataset_dict={'tcdatasetid':dataset_id,'tc_id':tc_id,'execornot':'Yes','data_type':'Default'}
        if DBUtil.IsDBConnectionGood(Conn)==False:
            time.sleep(1)
            Conn=GetConnection()
        result=DBUtil.InsertNewRecordInToTable(Conn,"test_case_datasets",**test_case_dataset_dict)
        if result==True:
            LogMessage(sModuleInfo,"Inserted the datasets for the test case %s"%tc_id,1)
        else:
            LogMessage(sModuleInfo, result,3)
    else:
        LogMessage(sModuleInfo,"Test Case DataSet Found for test case %s.No Need to add datasets"%tc_id,1)
    return "Pass"
def Update_TestCaseDetails(Conn, New_TC_Id, TC_Name, TC_Creator):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    #Form the Dictionary to add test case information
    Dict={
              'tc_id':New_TC_Id,
              'tc_name':TC_Name,
              'tc_type':'Auto',
              'tc_localization':'Yes',
              'tc_modifiedby':TC_Creator,
              'tc_modifydate':datetime.date.today()
              }
    if DBUtil.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()
    result = DBUtil.UpdateRecordInTable(Conn,"test_cases","where tc_id='%s'"%New_TC_Id,**Dict)
    if result == True:
        LogMessage(sModuleInfo, "Updated test case %s: %s" % (New_TC_Id, TC_Name),1)
        return "Pass"
    else:
        err_msg = LogMessage(sModuleInfo, "Failed to Update test case %s: %s" % (New_TC_Id, TC_Name),3)
        return err_msg
def Get_PIM_Data_By_Id(conn, Data_Id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    Data_List = []
    SQLQuery = ("select "
    " pmd.id,"
    " pmd.field,"
    " pmd.value"
    " from master_data pmd"
    " where"
    " pmd.id = '%s';" % (Data_Id))

    Data_List = DBUtil.GetData(conn, SQLQuery, False)
    Data_List = [tuple(x[1:3])for x in Data_List]

    AddressList = []
    for i in range(len(Data_List) - 1, -1, -1):
        eachTuple = Data_List[i]
        if eachTuple[1].startswith(Data_Id):# or eachTuple[0] == 'Home Address' or eachTuple[0] == 'Other Address':
            if eachTuple[1] != "":
                address_find_SQLQuery = ("select "
                " pmd.field,"
                " pmd.value"
                " from master_data pmd"
                " where"
                " pmd.id = '%s'"
                " ;" % (eachTuple[1]))
                AddressData = DBUtil.GetData(conn, address_find_SQLQuery, False)
            else:
                AddressData = ''
            Data_List.pop(i)
            AddressList.append((eachTuple[0], AddressData))
    for eachAddrData in AddressList:
        Data_List.append(eachAddrData)

    return Data_List

def TestCase_DataValidation(Platform, TC_Name, TC_Type, Priority, Tag_List, Dependency_List, Steps_Data_List, Section_Path):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    if Platform == '':
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case Platform", 3)
        return err_msg


    if TC_Name == '':
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case name", 3)
        return err_msg

    if TC_Type == '':
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case type", 3)
        return err_msg

    if Priority == '':
        print "Error. Test case Priority cannot be empty"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case Priority", 3)
        return err_msg

    if Section_Path == '':
        print "Error. Test Section cannot be empty"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case Section", 3)
        return err_msg
    if not isinstance(Tag_List, list):
        print "Error. Test case tag format is incorrect"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case tag format. It should be a list.", 3)
        return err_msg

    if not isinstance(Dependency_List, list):
        print "Error. Test case dependency format is incorrect"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case dependency format. It should be a list.", 3)
        return err_msg 

    if not isinstance(Steps_Data_List,list):
        print "Error. Test case steps format is incorrect"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case steps format. It should be a list.", 3)
        return err_msg
    else:
        for each in Steps_Data_List:
            if not isinstance(each[0],basestring) and not isinstance(each[2],basestring) and not isinstance(each[3],basestring) and not isinstance(each[4],basestring) and not isinstance(each[5],basestring):
                err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case steps format. StepName,Description,ExpectedResult,Time,Verification should be a basestring.", 3)
                return err_msg
            if not isinstance(each[1],list):
                err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case data format.It should be a list.",3)
                return err_msg
            else:
                for eachitem in each[1]:
                    if not isinstance(eachitem,list):
                        ######################Edit Data######################################
                        if isinstance(eachitem,tuple) and len(eachitem)==2:
                            #check for first edit data correct or not
                            print "edit_data"
                            ######################From DATA CHECK######################################
                            if isinstance(eachitem[0],list):
                                for eachitementry in eachitem[0]:
                                    if isinstance(eachitementry,tuple):
                                        if isinstance(eachitementry[0],basestring) and isinstance(eachitementry[1],basestring) and len(eachitementry)==2:
                                            print "edit from tuple data"
                                            if not isinstance(eachitementry[0],basestring) and not isinstance(eachitementry[1],basestring):
                                                err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:From normal tuple must be basestring",3)
                                                return err_msg
                                        elif isinstance(eachitementry[0],basestring) and isinstance(eachitementry[1],list) and len(eachitementry)==2:
                                            print "edit  from group data"
                                            for tupledata in eachitementry[1]:
                                                if not isinstance(tupledata[0],basestring) and not isinstance(tupledata[1],basestring):
                                                    err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:From Grouped Data tuple must be basestring",3)
                                                    return err_msg
                                        else:
                                            err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:From data tuple must be normal or Grouped",3)
                                            return err_msg
                                    else:
                                        err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case data format.From Data List is to be tuple Data",3)
                                        return err_msg
                            else:
                                err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case data format.From Data is to be a list",3)
                                return err_msg
                            ######################TO DATA CHECK######################################
                            if isinstance(eachitem[1],list):
                                for eachitementry in eachitem[1]:
                                    if isinstance(eachitementry,tuple):
                                        if isinstance(eachitementry[0],basestring) and isinstance(eachitementry[1],basestring) and len(eachitementry)==2:
                                            print "edit to tuple data"
                                            if not isinstance(eachitementry[0],basestring) and not isinstance(eachitementry[1],basestring):
                                                err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:To normal tuple must be basestring",3)
                                                return err_msg
                                        elif isinstance(eachitementry[0],basestring) and isinstance(eachitementry[1],list) and len(eachitementry)==2:
                                            print "edit to group data"
                                            for tupledata in eachitementry[1]:
                                                if not isinstance(tupledata[0],basestring) and not isinstance(tupledata[1],basestring):
                                                    err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:From Grouped Data tuple must be basestring",3)
                                                    return err_msg
                                        else:
                                            err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:To data tuple must be normal or Grouped",3)
                                            return err_msg
                                    else:
                                        err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case data format.To Data List is to be tuple Data",3)
                                        return err_msg
                            else:
                                err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case data format.To Data is to be a list",3)
                                return err_msg
                        else:
                            err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case data format.Edit data must be a tuple",3)
                            return err_msg
                    elif isinstance(eachitem,list):
                        ######################Normal Data######################################
                        for eachitementry in eachitem:
                            if isinstance(eachitementry,tuple):
                                ######################Grouped Data Check######################################
                                if isinstance(eachitementry[0],basestring) and isinstance(eachitementry[1],list) and len(eachitementry)==2:
                                    print "grouped_data"
                                    for tupledata in eachitementry[1]:
                                        if not isinstance(tupledata[0],basestring) and not isinstance(tupledata[1],basestring):
                                            err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case data format.GroupedData should contain basestring.",3)
                                            return err_msg
                                elif isinstance(eachitementry[0],basestring) and isinstance(eachitementry[1],basestring) and len(eachitementry)==2:
                                ######################Tuple Data Check######################################    
                                    print "tuple_data"
                                    if not isinstance(eachitementry[0],basestring) and not isinstance(eachitementry[1],basestring):
                                        err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case data format.TupleData should contain basestring.",3)
                                        return err_msg
                                else:
                                    err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case data format.Data Should be either edit type,tuple or grouped",3)
                                    return err_msg
                            else:
                                err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Invalid test case data format.DataSets should be a list.",3)
                                return err_msg
                    else:
                        err_msg=LogMessage(sModuleInfo,"TEST CASE CREATION Failed:Expected Normal or Edit Data",3)
                        return err_msg
    return "Pass"
def Insert_TestCase_Tags(conn, TC_Id, Platform, Manual_TC_Id, TC_Type, Custom_Tag_List, Dependency_List, Priority, Associated_Bugs_List, Status, Section_Path, Requirement_ID_List):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    Tag_List = []
    #Add test case id tag
    Tag_List.append(('%s' % TC_Id, 'tcid'))
    ManualTCIDFound = False
    for eachManual_Id in Manual_TC_Id:
        if eachManual_Id.strip() != '':
            Tag_List.append(('%s' % eachManual_Id, 'MKS'))
            ManualTCIDFound = True
    if ManualTCIDFound == False:
        Tag_List.append(('%s' % TC_Id, 'MKS'))
    #hard coded tags for now
    Tag_List.append(('Default', 'Data_Type'))
    #Add Section names & initialize variables
    if Platform.lower() == 'pc':
        Tag_List.append(('PC', 'machine_os'))
        Section_Tag = 'Section'
        Custom_Tag = 'CustomTag'
        Section_Path_Tag = 'section_id'
        TestRunType_Tag = 'test_run_type'
        Priority_Tag = 'Priority'
        Dependency_Tag = 'Dependency'
        Tag_List.append(('Status', Status))
        if Status=="Forced":
            Tag_List.append(('Status', 'Ready'))
    elif Platform.lower() == 'mac':
        Tag_List.append(('MAC', 'machine_os'))
        Section_Tag = 'MacSection'
        Custom_Tag = 'MacCustomTag'
        Section_Path_Tag = 'mac_section_id'
        TestRunType_Tag = 'Mac_test_run_type'
        Priority_Tag = 'MacPriority'
        Dependency_Tag = 'MacDependency'
        Tag_List.append(('MacStatus', Status))
        if Status=="Forced":
            Tag_List.append(('Status', 'Ready'))
    else:
        err_msg = LogMessage(sModuleInfo, "Unknown platform value for the test case: %s" % (Platform), 3)
        return err_msg
    #Add test case type, priority, Data Type
    for each_TC_Type in TC_Type:
        Tag_List.append(('%s' % each_TC_Type, TestRunType_Tag))
    Tag_List.append(('%s' % Priority, Priority_Tag))

    #Add custom tags
    for eachTag in Custom_Tag_List:
        Tag_List.append(('%s' % eachTag, Custom_Tag))

    #Add Section id based on hierarchy
    if DBUtil.IsDBConnectionGood(conn)==False:
        time.sleep(1)
        conn=GetConnection()
    Section_Id = DBUtil.GetData(conn, "select section_id from product_sections where section_path = '%s'" % Section_Path)
    if len(Section_Id) > 0:
        Tag_List.append(('%d' % Section_Id[0], Section_Path_Tag))

    #Work around to display section names in run page
    for eachSection in Section_Path.split('.'):
        Tag_List.append(('%s' % eachSection, Section_Tag))

    #Add Dependency tags
    for eachDependency in Dependency_List:
        Tag_List.append(('%s' % Dependency_Tag, eachDependency))
        if eachDependency in ['Outlook', 'MacNative', 'iTunes', 'iPhoto', 'WMP', 'Chrome', 'FireFox', 'IE']:
            Tag_List.append(('%s' % eachDependency, 'client'))
        elif eachDependency in ['BBX', 'SD']:
            Tag_List.append(('%s' % eachDependency, 'device_memory'))

    #Add Associated Bugs
    for eachBugId in Associated_Bugs_List:
        Tag_List.append(('%s' % eachBugId, 'JiraId'))

    #Add Associated Requirements
    for eachReqId in Requirement_ID_List:
        Tag_List.append(('%s' % eachReqId, 'PRDId'))

    for eachTag in Tag_List:
        if DBUtil.IsDBConnectionGood(conn)==False:
            time.sleep(1)
            conn=GetConnection()
        result = AddTag(conn, TC_Id, eachTag[0], eachTag[1])
        if result !="Pass":
            err_msg = LogMessage(sModuleInfo, "Failed to add tag %s: %s" % (eachTag[0], eachTag[1]), 3)
            return err_msg

    if result == "Pass":
        LogMessage(sModuleInfo, "Entered test case tags %s" % (TC_Id), 1)
        return "Pass"
    else:
        err_msg = LogMessage(sModuleInfo, "Failed to Enter test case tags %s" % (TC_Id), 1)
        return err_msg

def AddTag(conn, TC_Id, name, property):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    try:
        if DBUtil.IsDBConnectionGood(conn)==False:
            time.sleep(1)
            conn=GetConnection()
        result=DBUtil.InsertNewRecordInToTable(conn, 'test_case_tag',
            tc_id='%s' % TC_Id,
            name='%s' % name,
            property='%s' % property)
        #print "Tag: %s with Property: %s added." %(name, property)
        if result==True:
            LogMessage(sModuleInfo,"Inserted %s - %s in test_case_tag table"%(name,property),1)
        else:
            LogMessage(sModuleInfo, result,3)
        return "Pass"
    except Exception, e:
        err_msg = LogMessage(sModuleInfo, e, 2)
        return err_msg

def Insert_TestSteps_StepsData(Conn, TC_Id, Test_Case_DataSet_Id, Steps_Data_List):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    Step_Index=1
    for each in Steps_Data_List:
        step_name=each[0]
        step_data_query="select step_id,data_required from test_steps_list where stepname='%s'"%step_name
        if DBUtil.IsDBConnectionGood(Conn)==False:
            time.sleep(1)
            Conn=GetConnection()
        step_data_attr=DBUtil.GetData(Conn,step_data_query,False)
        if len(step_data_attr)>0:
            step_id=step_data_attr[0][0]
            step_data_required=step_data_attr[0][1]
            step_data=each[1]
        else:
            error_message="No steps is found with the name %s in the test_steps_list table"%step_name
            LogMessage(sModuleInfo,error_message,2)
            return error_message
        #Populate the test_steps_list
        #Form the directory for the test_steps table
        test_step_dict={'tc_id':TC_Id,'step_id':step_id}
        if DBUtil.IsDBConnectionGood(Conn)==False:
            time.sleep(1)
            Conn=GetConnection()
        result=DBUtil.InsertNewRecordInToTable(Conn, "test_steps",**test_step_dict)
        if result==True:
            message="Added test step to test case id %s: %s"%(TC_Id,step_name)
            LogMessage(sModuleInfo,message,1)
            step_sequence_get_query=("select teststepsequence from test_steps where tc_id = '%s' and step_id='%s' order by teststepsequence desc limit 1" % (TC_Id,step_id))
            if DBUtil.IsDBConnectionGood(Conn)==False:
                time.sleep(1)
                Conn=GetConnection()
            step_sequence=DBUtil.GetData(Conn,step_sequence_get_query)
            if len(step_sequence)>0:
                seq=step_sequence[0]
                step_description=each[2]
                expected_result=each[3]
                verification_point=each[4]
                time_expected=each[5]
                if step_data_required:
                    #Data_List=each[1]
                    print seq
                    if DBUtil.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    Data_ID_List=InsertMasterDataForDataRequired(Conn,TC_Id,Step_Index,step_data,step_description,expected_result,verification_point,time_expected)
                    if isinstance(Data_ID_List,list):
                        #Get them to the container_data
                        if DBUtil.IsDBConnectionGood(Conn)==False:
                            time.sleep(1)
                            Conn=GetConnection()
                        container_data_id=InsertContainerData(Conn,TC_Id,Step_Index,Data_ID_List)
                        ##insert it in the test_steps_data
                        test_steps_data_dict={'tcdatasetid':Test_Case_DataSet_Id,'testdatasetid':container_data_id,'teststepseq':seq}
                        if DBUtil.IsDBConnectionGood(Conn)==False:
                            time.sleep(1)
                            Conn=GetConnection()
                        result=DBUtil.InsertNewRecordInToTable(Conn,"test_steps_data",**test_steps_data_dict)
                        if result==True:
                            msg="Added test_steps_data tcdataset:%s"%Test_Case_DataSet_Id
                            LogMessage(sModuleInfo,msg,1)
                        else:
                            LogMessage(sModuleInfo,result,3)
                else:
                    Master_Data_ID=('%s_s%s'%(TC_Id,Step_Index))
                    if DBUtil.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
                    InsertMasterMetaData(Conn,Master_Data_ID,step_description,expected_result,verification_point,time_expected)
            else:
                error_message=("No stepsequence is listed test_steps table for test case %s and step id %s"%(TC_Id,step_id))
                LogMessage(sModuleInfo,error_message,2)
                #Conn=GetConnection()
                return error_message
        else:
            LogMessage(sModuleInfo,result,3)
            Conn=GetConnection()
        Step_Index+=1
    return "Pass"
def InsertContainerData(Conn,TC_Id,Step_Index,Data_ID_List):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    container_data_id=('%s_s%s'%(TC_Id,Step_Index))
    for each in Data_ID_List:
        #form the Dict
        if isinstance(each,tuple) and len(each)==2:
            container_dict={'dataid':container_data_id,'curname':each[0],'newname':each[1]}
            if DBUtil.IsDBConnectionGood(Conn)==False:
                    time.sleep(1)
                    Conn=GetConnection()
            result=DBUtil.InsertNewRecordInToTable(Conn,"container_type_data",**container_dict)
        else:
            container_dict={'dataid':container_data_id,'curname':each}
            if DBUtil.IsDBConnectionGood(Conn)==False:
                        time.sleep(1)
                        Conn=GetConnection()
            result=DBUtil.InsertNewRecordInToTable(Conn,"container_type_data",**container_dict)
        if result==True:
            msg="Added container data entry data id:%s - curname:%s"%(container_data_id,each)
            LogMessage(sModuleInfo,msg,1)
        else:
            error_message=LogMessage(sModuleInfo,result,1)
            return error_message
    return container_data_id
def InsertMasterDataForDataRequired(Conn,TC_Id,Step_Index,Data_List,step_description,expected_result,verification_point,time_expected):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    DataIDList=[]
    DataIndex=1
    Master_Data_ID=('%s_s%s'%(TC_Id,Step_Index))
    if DBUtil.IsDBConnectionGood(Conn)==False:
                    time.sleep(1)
                    Conn=GetConnection()
    InsertMasterMetaData(Conn, Master_Data_ID, step_description, expected_result, verification_point, time_expected)
    for each in Data_List:
        if isinstance(each,list):
            Data_ID=Master_Data_ID+('_d%s'%DataIndex)
            if DBUtil.IsDBConnectionGood(Conn)==False:
                    time.sleep(1)
                    Conn=GetConnection()  
            result=InsertMasterData(Conn,Data_ID,each)
            if result=="Pass":
                DataIDList.append(Data_ID)
                DataIndex+=1
            else:
                LogMessage(sModuleInfo,result,3)
        elif isinstance(each,tuple) and len(each)==2:
            From_Data_Id = Master_Data_ID+('_d%s_fr'%(DataIndex))
            To_Data_Id = Master_Data_ID+('_d%s_to'%(DataIndex))
            if isinstance(each[0], list):
                if DBUtil.IsDBConnectionGood(Conn):
                    time.sleep(1)
                    Conn=GetConnection()
                result =InsertMasterData(Conn, From_Data_Id, each[0])
            else:
                err_msg = LogMessage(sModuleInfo, "Failed to add From Master data. Incorrect format %s" % each, 3)
                return err_msg
            if isinstance(each[1], list):
                if DBUtil.IsDBConnectionGood(Conn):
                    time.sleep(1)
                    Conn=GetConnection()
                result =InsertMasterData(Conn, To_Data_Id, each[1])
            else:
                err_msg = LogMessage(sModuleInfo, "Failed to add To Master data. Incorrect format %s" % each, 3)
                return err_msg
            if result=="Pass":
                DataIDList.append((From_Data_Id,To_Data_Id))
                DataIndex+=1
        else:
            error_message="Wrong Formatted Data in Step %s of test case ID %s"%(Step_Index,TC_Id)
            LogMessage(sModuleInfo, error_message, 2)
    return DataIDList     
def InsertMasterData(Conn,Data_ID,dataList):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    address_Index=1
    for each in dataList:
        if isinstance(each,tuple):
            if isinstance(each[1],list):
                print "Grouped Data Entry"
                #first give the entry for the group data
                data_index=(Data_ID+"_a%s"%address_Index)
                master_data_group_data={}
                master_data_group_data.update({'id':Data_ID,'field':each[0],'value':data_index})
                if DBUtil.IsDBConnectionGood(Conn)==False:
                    time.sleep(1)
                    Conn=GetConnection()
                result=DBUtil.InsertNewRecordInToTable(Conn,"master_data",**master_data_group_data)
                if result==True:
                    msg="Added Grouped Data -- id:%s - field:%s - value:%s"%(master_data_group_data['id'],master_data_group_data['field'],master_data_group_data['value'])
                    LogMessage(sModuleInfo,msg,1)
                else:
                    LogMessage(sModuleInfo,result,3)
                for eachitem in each[1]:
                    if isinstance(eachitem,tuple):
                        #form dict
                        group_data_entry={}
                        group_data_entry.update({'id':data_index,'field':eachitem[0],'value':eachitem[1]})
                        if DBUtil.IsDBConnectionGood(Conn)==False:
                            time.sleep(1)
                            Conn=GetConnection()
                        result=DBUtil.InsertNewRecordInToTable(Conn,"master_data",**group_data_entry)
                        if result==True:
                            msg="Added Grouped Data Entry -- id:%s - field:%s - value:%s"%(data_index,eachitem[0],eachitem[1])
                            LogMessage(sModuleInfo,msg,1)
                        else:
                            LogMessage(sModuleInfo,result,3)
                    else:
                        error_message="Wrong Formatted Grouped Data.Data id:%s"%data_index
                        LogMessage(sModuleInfo,error_message,2)
                        return error_message
                address_Index+=1
            else:
                #Normal Data is to be given here
                #form the dict for the normal tuple data
                master_data_tuple_data={}
                master_data_tuple_data.update({'id':Data_ID,'field':each[0],'value':each[1]})
                if DBUtil.IsDBConnectionGood(Conn)==False:
                    time.sleep(1)
                    Conn=GetConnection()
                result=DBUtil.InsertNewRecordInToTable(Conn,"master_data",**master_data_tuple_data)
                if result==True:
                    msg=("Added tuple Data -- id:%s - field:%s - value: %s"%(master_data_tuple_data['id'],master_data_tuple_data['field'],master_data_tuple_data['value']))
                    LogMessage(sModuleInfo,msg,1) 
                else:
                    LogMessage(sModuleInfo,result,3)    
        else:
            error_message="Wrong Formatted Data.Data is not Tuple.Master_Data_ID - %s"%(Data_ID)
            LogMessage(sModuleInfo,error_message,3)
            return error_message
    return "Pass"
def InsertMasterMetaData(Conn,Master_Data_ID,step_description,expected_result,verification_point,time_expected):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    #create the array for entering the data
    field_array=['step','expected','verification','estimated']
    value_array=['description','result','point','time']
    values=[step_description,expected_result,verification_point,time_expected]
    for each in zip(field_array,value_array,values):
        #form Dict
        Dict={}
        Dict.update({'id':Master_Data_ID,'field':each[0],'value':each[1],'description':each[2]})
        if DBUtil.IsDBConnectionGood(Conn)==False:
            time.sleep(1)
            Conn=GetConnection()
        result=DBUtil.InsertNewRecordInToTable(Conn,"master_data",**Dict)
        if result==True:
            msg=("Added id:%s - field:%s - value:%s - description:%s"%(Dict['id'],Dict['field'],Dict['value'],Dict['description']))
            LogMessage(sModuleInfo,msg,1)
        else:
            LogMessage(sModuleInfo,result,3)
def Insert_TestCaseDataSet(conn, TC_DataSet_Id, TC_Id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    Dict={
          'tcdatasetid':TC_DataSet_Id,
          'tc_id':TC_Id,
          'execornot':'Yes',
          'data_type':'Default'                           
          }
    if DBUtil.IsDBConnectionGood(conn)==False:
        time.sleep(1)
        conn=GetConnection()
    result = DBUtil.InsertNewRecordInToTable(conn, "test_case_datasets",**Dict)

    if result == True:
        LogMessage(sModuleInfo, "Entered test case dataset %s: %s" % (TC_Id, TC_DataSet_Id), 1)
        return "Pass"
    else:
        err_msg = LogMessage(sModuleInfo, "Failed to Enter test case dataset %s: %s" % (TC_Id, TC_DataSet_Id), 3)
        return err_msg

def Insert_TestCaseName(Conn, TC_Id, TC_Name, TC_Creator):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    #Form the Dictionary to add test case information
    Dict={
              'tc_id':TC_Id,
              'tc_name':TC_Name,
              'tc_type':'Auto',
              'tc_localization':'Yes',
              'tc_createdby':TC_Creator,
              'tc_creationdate':datetime.date.today(),
              'tc_modifiedby':TC_Creator,
              'tc_modifydate':datetime.date.today()
              }
    if DBUtil.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()
    result = DBUtil.InsertNewRecordInToTable(Conn, "test_cases",**Dict)
    if result == True:
        LogMessage(sModuleInfo, "Entered test case %s: %s" % (TC_Id, TC_Name),1)
        return "Pass"
    else:
        err_msg = LogMessage(sModuleInfo, "Failed to Enter test case %s: %s" % (TC_Id, TC_Name),3)
        return err_msg
def Generate_TCId(Section_Path,tc_id):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        TC_ID_Prefix = ''
        TC_ID_Prefix = Section_Path.split('.')[len(Section_Path.split('.')) - 1][:3].upper()
        TC_Id = "%s-%s" % (TC_ID_Prefix.upper(), str(tc_id).lstrip('0').zfill(4))
        LogMessage(sModuleInfo,TC_Id+" is generated",1)
        return TC_Id
    except Exception,e:
        print "exception:",e
        LogMessage(sModuleInfo,e,3)
        return tc_id
def LogMessage(sModuleInfo, msg, level, debug=True):
    if debug:
        print msg
        CommonUtil.ExecLog(sModuleInfo, msg, level)
    return msg 