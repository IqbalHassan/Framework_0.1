'''
Created on May 13, 2013

'''
import datetime
import inspect

import CommonUtil
import DataBaseUtilities as DBUtil


def Insert_TestCaseName(conn, TC_Id, TC_Name, TC_Creator):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    result = DBUtil.InsertNewRecordInToTable(conn, "test_cases",
                                    tc_id=TC_Id,
                                    tc_name=TC_Name,
                                    tc_type='Auto',
                                    tc_localization='Yes',
                                    tc_createdby=TC_Creator,
                                    tc_creationdate=datetime.date.today(),
                                    tc_modifiedby=TC_Creator,
                                    tc_modifydate=datetime.date.today()
                                     )

    if result == True:
        LogMessage(sModuleInfo, "Entered test case %s: %s" % (TC_Id, TC_Name), 4, result)
        return "Pass"
    else:
        err_msg = LogMessage(sModuleInfo, "Failed to Enter test case %s: %s" % (TC_Id, TC_Name), 4, result)
        return err_msg

def Update_TestCaseDetails(conn, TC_Id, TC_Name, TC_Creator):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    result = DBUtil.UpdateRecordInTable(conn, "test_cases", "where tc_id = '%s'" % TC_Id,
                                    tc_name=TC_Name,
                                    tc_type='Auto',
                                    tc_localization='Yes',
                                    tc_modifiedby=TC_Creator,
                                    tc_modifydate=datetime.date.today()
                                     )

    if result == True:
        LogMessage(sModuleInfo, "Updated test case %s: %s" % (TC_Id, TC_Name), 4, result)
        return "Pass"
    else:
        err_msg = LogMessage(sModuleInfo, "Failed to update test case %s: %s" % (TC_Id, TC_Name), 4, result)
        return err_msg

def Insert_TestSteps_StepsData(conn, TC_Id, Test_Case_DataSet_Id, Steps_Data_List):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    teststepsequencelist = []
    Step_Index = 1
    for eachStepData in Steps_Data_List:
        Step_Name = eachStepData[0]
        result = DBUtil.GetData(conn, "select step_id,data_required from test_steps_list where stepname = '%s'" % Step_Name, False)
        if len(result) > 0:
            Step_Id = result[0][0]
            Step_Data_Required = result[0][1]
            Step_Data_Set = eachStepData[1]
            # Step_Description_Set=eachStepData[2]

        else:
            err_msg = LogMessage(sModuleInfo, "Incorrect step name: %s" % (Step_Name), 4)
            return err_msg

        # Insert the test step
        result = DBUtil.InsertNewRecordInToTable(conn, "test_steps",
                                        tc_id=TC_Id,
                                        step_id=Step_Id
                                         )

        # Get the sequence number of the inserted step
        if result == True:
            LogMessage(sModuleInfo, "Added test step to test case id %s: %s" % (TC_Id, Step_Name), 4, result)

            result = DBUtil.GetData(conn, "select teststepsequence from test_steps where tc_id = '%s' order by teststepsequence desc limit 1" % (TC_Id))
            if len(result) > 0:
                Step_Seq = int(result[0])
                # if this step needs data, then start inserting data, else get out of here
                if Step_Data_Required:
                    # Insert master_data - id, field, value
                    Data_Id_List = Insert_MasterData(conn, TC_Id, Step_Index, Step_Data_Set)
                    # for eachitem in Data_Id_List:
                    eachstep = Data_Id_List[0].split("_d")
                    eachstep = eachstep[0].strip()
                    print eachstep + "-" + eachStepData[2]
                    result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                              md_id=eachstep,
                                                              field="step",
                                                              value="description",
                                                              description=eachStepData[2])
                    if result == True:
                        LogMessage(sModuleInfo, "Inserted step Description in master_data", 4, result)
                    else:
                        LogMessage(sModuleInfo, "Failed insertion step Description in master_data", 4, result)
                    result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                              md_id=eachstep,
                                                              field="expected",
                                                              value="result",
                                                              description=eachStepData[3])
                    if result == True:
                        LogMessage(sModuleInfo, "Inserted expected in master_data", 4, result)
                    else:
                        LogMessage(sModuleInfo, "Failed insertion expected in master_data", 4, result)
                    
                    result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                              md_id=eachstep,
                                                              field="verification",
                                                              value="point",
                                                              description=eachStepData[4])
                    if result == True:
                        LogMessage(sModuleInfo, "Inserted verification in master_data", 4, result)
                    else:
                        LogMessage(sModuleInfo, "Failed insertion verification in master_data", 4, result)
                    
                    result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                              md_id=eachstep,
                                                              field="estimated",
                                                              value="time",
                                                              description=eachStepData[5])
                    if result == True:
                        LogMessage(sModuleInfo, "Inserted estimated in master_data", 4, result)
                    else:
                        LogMessage(sModuleInfo, "Failed insertion estimated in master_data", 4, result)
                    
                    if isinstance(Data_Id_List, list):
                        # Insert Container_Type_Data - dataid, curname
                        Container_Data_Id = Insert_ContainerTypeData(conn, TC_Id, Step_Index, Data_Id_List)
                        # if its not a verify step
                        if 'Verify' not in Step_Name:
                            # Insert Test_Steps_Data - tcdatasetid, dataid, step_seq
                            result = DBUtil.InsertNewRecordInToTable(conn, "test_steps_data",
                                                            tcdatasetid=Test_Case_DataSet_Id,
                                                            testdatasetid=Container_Data_Id,
                                                            teststepseq=Step_Seq
                                                             )

                            if result == True:
                                LogMessage(sModuleInfo, "Added test step data: %s" % (Step_Name), 4)

                            else:
                                err_msg = LogMessage(sModuleInfo, "Failed to add test step data: %s" % (Step_Name), 4)
                                return err_msg

                        # if its a verify step
                        else:
                            # insert a expected_dataset expectedrefid,tcdatasetid,step_seq
                            Expected_Data_Set_Id = Insert_ExpectedDataSet(conn, TC_Id, Step_Index, Step_Seq, Test_Case_DataSet_Id)
                            if Expected_Data_Set_Id == "Critical":
                                err_msg = LogMessage(sModuleInfo, "Failed to create expected data set: %s" % (Step_Name), 4)
                                return err_msg

                            # insert a expected_container exprefid, dataid
                            result = DBUtil.InsertNewRecordInToTable(conn, "expected_container",
                                                            exprefid=Expected_Data_Set_Id,
                                                            container_name=Container_Data_Id
                                                             )

                            if result == True:
                                LogMessage(sModuleInfo, "Added test step expected data: %s" % (Step_Name), 4)

                            else:
                                err_msg = LogMessage(sModuleInfo, "Failed to add test step expected data: %s" % (Step_Name), 4)
                                return err_msg


                    else:
                        err_msg = LogMessage(sModuleInfo, "PIM Master data could not be inserted: %s" % (Step_Name), 4)
                        return err_msg
                else:
                    LogMessage(sModuleInfo, "Added test step without data: %s" % (Step_Name), 4)
                    # Add the test steps description to the datasets and steps
                    Data_Id = "%s_s%s" % (TC_Id, Step_Index)
                    print Data_Id + " - " + eachStepData[2]
                    result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                              md_id=Data_Id,
                                                              field="step",
                                                              value="description",
                                                              description=eachStepData[2])
                    if result == True:
                        LogMessage(sModuleInfo, "Inserted step Description in master_data", 4, result)
                    else:
                        LogMessage(sModuleInfo, "Failed insertion step Description in master_data", 4, result)
                    result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                              md_id=Data_Id,
                                                              field="expected",
                                                              value="result",
                                                              description=eachStepData[3])
                    if result == True:
                        LogMessage(sModuleInfo, "Inserted expected in master_data", 4, result)
                    else:
                        LogMessage(sModuleInfo, "Failed insertion expected in master_data", 4, result)
                    result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                              md_id=Data_Id,
                                                              field="verification",
                                                              value="point",
                                                              description=eachStepData[4])
                    if result == True:
                        LogMessage(sModuleInfo, "Inserted verification in master_data", 4, result)
                    else:
                        LogMessage(sModuleInfo, "Failed insertion verification in master_data", 4, result)
                    result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                              md_id=Data_Id,
                                                              field="estimated",
                                                              value="time",
                                                              description=eachStepData[5])
                    if result == True:
                        LogMessage(sModuleInfo, "Inserted estimated in master_data", 4, result)
                    else:
                        LogMessage(sModuleInfo, "Failed insertion estimated in master_data", 4, result)
                    
            else:
                err_msg = LogMessage(sModuleInfo, "Step Sequence not found: %s" % (Step_Name), 4)
                return err_msg

        else:
            err_msg = LogMessage(sModuleInfo, "Failed to add test step to test case id %s: %s" % (TC_Id, Step_Name), 4)
            return err_msg

        Step_Index += 1
    return "Pass"


def Insert_TestCaseDataSet(conn, TC_DataSet_Id, TC_Id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    result = DBUtil.InsertNewRecordInToTable(conn, "test_case_datasets",
                                    tcdatasetid=TC_DataSet_Id,
                                    tc_id=TC_Id,
                                    execornot='Yes',
                                    data_type='Default'
                                     )

    if result == True:
        LogMessage(sModuleInfo, "Entered test case dataset %s: %s" % (TC_Id, TC_DataSet_Id), 4)
        return "Pass"
    else:
        err_msg = LogMessage(sModuleInfo, "Failed to Enter test case dataset %s: %s" % (TC_Id, TC_DataSet_Id), 4)
        return err_msg

def Insert_ContainerTypeData(conn, TC_Id, Step_Index, Data_Id_List):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    Container_Data_Id = "%s_s%s" % (TC_Id, Step_Index)

    for eachDataId in Data_Id_List:
        if isinstance(eachDataId, tuple):
            # if its a tuple, then its a edit data of (cur_data_id, new_data_id)
            result = DBUtil.InsertNewRecordInToTable(conn, "container_type_data",
                                            dataid=Container_Data_Id,
                                            curname=eachDataId[0],
                                            newname=eachDataId[1]
                                             )
        else:
            # if its not a tuple, then its cur_data_id
            result = DBUtil.InsertNewRecordInToTable(conn, "container_type_data",
                                            dataid=Container_Data_Id,
                                            curname=eachDataId
                                             )
        if result == True:
            LogMessage(sModuleInfo, "Inserted Container data set for %s" % Data_Id_List, 4, result)
        if result != True:
            err_msg = LogMessage(sModuleInfo, "Failed to add container data set for %s:" % Data_Id_List, 4)
            return err_msg

    return Container_Data_Id

def Insert_MasterData(conn, TC_Id, Step_Index, Data_Set_List):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    Data_Id_List = []
    Data_Index = 1
    # Data_Set_List will be a list like [contact1, contact2, contact3]
    # or a list like [(contact1,contact1edit), (contact2,contact2edit)] for Edit cases
    # each contact will be a list like [(first name, john),(last name, smith)]
    for eachDataList in Data_Set_List:
        if isinstance(eachDataList, list):
            Data_Id = "%s_s%s_d%s" % (TC_Id, Step_Index, Data_Index)
            result = Insert_PIMMasterData(conn, Data_Id, eachDataList)
            if result != "Pass":
                err_msg = LogMessage(sModuleInfo, "Failed to insert data: %s" % (eachDataList), 4)
                return err_msg

            Data_Id_List.append(Data_Id)
            Data_Index += 1
        elif isinstance(eachDataList, tuple) and len(eachDataList) == 2:
            From_Data_Id = "%s_s%s_d%s_fr" % (TC_Id, Step_Index, Data_Index)
            To_Data_Id = "%s_s%s_d%s_to" % (TC_Id, Step_Index, Data_Index)
            if isinstance(eachDataList[0], list):
                result = Insert_PIMMasterData(conn, From_Data_Id, eachDataList[0])
            else:
                err_msg = LogMessage(sModuleInfo, "Failed to add Master data. Incorrect format %s" % eachDataList, 4)
                return err_msg

            if isinstance(eachDataList[1], list):
                result = Insert_PIMMasterData(conn, To_Data_Id, eachDataList[1])
            else:
                err_msg = LogMessage(sModuleInfo, "Failed to add Master data. Incorrect format %s" % eachDataList, 4)
                return err_msg

            Data_Id_List.append((From_Data_Id, To_Data_Id))
            Data_Index += 1
        else:
            err_msg = LogMessage(sModuleInfo, "Failed to add Master data. Incorrect format %s" % eachDataList, 4)
            return err_msg



    return Data_Id_List

def Insert_PIMMasterData(conn, Data_Id, Data_List):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    # Data_List will be a list like [(first name, john),(last name, smith)]
    # for address field tuple will be like (Work Addres, [(city,waterloo), (Street,123 Street)])
    Addr_Data_Index = 1
    if len(Data_List) <= 0:
        err_msg = LogMessage(sModuleInfo, "Data list is empty", 4)
        return err_msg

    for eachData in Data_List:
        # Make sure each Data is a tuple
        if isinstance(eachData, tuple):
            # Check if field is address, in which case value will be a list of tuples
            if isinstance(eachData[1], list):  # 'address' in eachData[0].lower():
                # value for address should also be a list of tuples
                if isinstance(eachData[1], list):
                    Addr_Data_Id = "%s_a%s" % (Data_Id, Addr_Data_Index)
                    # Insert the Address data id
                    result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                    md_id=Data_Id,
                                                    field=eachData[0],
                                                    value=Addr_Data_Id
                                                     )
                    if result == True:
                        msg = LogMessage(sModuleInfo, "inserted data in master_data data id: %s - %s " % (eachData[0], Addr_Data_Id), 4)
                    if result != True:
                        err_msg = LogMessage(sModuleInfo, "Failed to insert list data id: %s" % (eachData), 4)
                        return err_msg
                    for eachAddrData in eachData[1]:
                        # each addr data should be tuple too
                        if isinstance(eachAddrData, tuple):
                            # Insert the Address datas each field and value
                            result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                            md_id=Addr_Data_Id,
                                                            field=eachAddrData[0],
                                                            value=eachAddrData[1]
                                                             )
                            if result != True:
                                err_msg = LogMessage(sModuleInfo, "Failed to insert list data value: %s" % (eachAddrData), 4)
                                return err_msg
                        else:
                            err_msg = LogMessage(sModuleInfo, "Data is not a tuple: %s" % (eachData), 4)
                            return err_msg

                    Addr_Data_Index += 1

                else:
                    err_msg = LogMessage(sModuleInfo, "Data is not a list of tuples: %s" % (eachData), 4)
                    return err_msg


            else:
                # Insert the test step
                result = DBUtil.InsertNewRecordInToTable(conn, "master_data",
                                                md_id=Data_Id,
                                                field=eachData[0],
                                                value=eachData[1]
                                                 )
                if result == True:
                    msg = LogMessage(sModuleInfo, "inserted data in master_data data id: %s - %s" % (eachData[0], eachData[1]), 4)
            if result != True:
                err_msg = LogMessage(sModuleInfo, "Failed to insert data: %s" % (eachData), 4)
                return err_msg

        else:
            err_msg = LogMessage(sModuleInfo, "Data is not a tuple: %s" % (eachData), 4)
            return err_msg



    return "Pass"


def Insert_ExpectedDataSet(conn, TC_Id, Step_Index, Step_Seq, Test_Case_DataSet_Id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    Expected_Data_Set_Id = "Ex%sds_%s" % (TC_Id, Step_Index)

    result = DBUtil.InsertNewRecordInToTable(conn, "expected_datasets",
                                    expectedrefid=Expected_Data_Set_Id,
                                    dataid='X',
                                    datasetid=Test_Case_DataSet_Id,
                                    stepsseq=Step_Seq
                                     )


    if result == True:
        LogMessage(sModuleInfo, "Added test expected data set: %s" % (Expected_Data_Set_Id), 4)
    else:
        err_msg = LogMessage(sModuleInfo, "Failed to add test expected data set: %s" % (Expected_Data_Set_Id), 4)
        return err_msg

    return Expected_Data_Set_Id

def Insert_TestCase_Tags(conn, TC_Id, Platform, Manual_TC_Id, TC_Type, Custom_Tag_List, Dependency_List, Priority, Associated_Bugs_List, Status, Section_Path, Feature_Path, Requirement_ID_List):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    Tag_List = []
    # Add test case id tag
    Tag_List.append(('%s' % TC_Id, 'tcid'))
    ManualTCIDFound = False
    for eachManual_Id in Manual_TC_Id:
        if eachManual_Id.strip() != '':
            Tag_List.append(('%s' % eachManual_Id, 'MKS'))
            ManualTCIDFound = True
    if ManualTCIDFound == False:
        Tag_List.append(('%s' % TC_Id, 'MKS'))

    # hard coded tags for now
    Tag_List.append(('Default', 'Data_Type'))

    # Add Section names & initialize variables
    if Platform.lower() == 'pc':
        Tag_List.append(('PC', 'machine_os'))
        Section_Tag = 'Section'
        Custom_Tag = 'CustomTag'
        Section_Path_Tag = 'section_id'
        TestRunType_Tag = 'test_run_type'
        Priority_Tag = 'Priority'
        Dependency_Tag = 'Dependency'
        Tag_List.append(('Status', Status))
        if Status == "Forced":
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
        if Status == "Forced":
            Tag_List.append(('Status', 'Ready'))
    else:
        err_msg = LogMessage(sModuleInfo, "Unknown platform value for the test case: %s" % (Platform), 4)
        return err_msg

    # Add test case type, priority, Data Type
    for each_TC_Type in TC_Type:
        Tag_List.append(('%s' % each_TC_Type, TestRunType_Tag))
    Tag_List.append(('%s' % Priority, Priority_Tag))

    # Add custom tags
    for eachTag in Custom_Tag_List:
        Tag_List.append(('%s' % eachTag, Custom_Tag))

    # Add Section id based on hierarchy
    Section_Id = DBUtil.GetData(conn, "select section_id from product_sections where section_path = '%s'" % Section_Path)
    if len(Section_Id) > 0:
        Tag_List.append(('%d' % Section_Id[0], Section_Path_Tag))

    # Work around to display section names in run page
    for eachSection in Section_Path.split('.'):
        Tag_List.append(('%s' % eachSection, Section_Tag))

    # Add Dependency tags
    for eachDependency in Dependency_List:
        Tag_List.append(('%s' % Dependency_Tag, eachDependency))
        if eachDependency in ['Outlook', 'MacNative', 'iTunes', 'iPhoto', 'WMP', 'Chrome', 'FireFox', 'IE']:
            Tag_List.append(('%s' % eachDependency, 'client'))
        elif eachDependency in ['BBX', 'SD']:
            Tag_List.append(('%s' % eachDependency, 'device_memory'))

    # Add Associated Bugs
    for eachBugId in Associated_Bugs_List:
        Tag_List.append(('%s' % eachBugId, 'JiraId'))

    # Add Associated Requirements
    for eachReqId in Requirement_ID_List:
        Tag_List.append(('%s' % eachReqId, 'PRDId'))

    for eachTag in Tag_List:
        result = AddTag(conn, TC_Id, eachTag[0], eachTag[1])
        if result == "Critical":
            err_msg = LogMessage(sModuleInfo, "Failed to add tag %s: %s" % (eachTag[0], eachTag[1]), 4)
            return err_msg

    if result == "Pass":
        LogMessage(sModuleInfo, "Entered test case tags %s" % (TC_Id), 4)
        return "Pass"
    else:
        err_msg = LogMessage(sModuleInfo, "Failed to Enter test case tags %s" % (TC_Id), 4)
        return err_msg

def AddTag(conn, TC_Id, name, property):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    try:
        result = DBUtil.InsertNewRecordInToTable(conn, 'test_case_tag',
            tc_id='%s' % TC_Id,
            name='%s' % name,
            property='%s' % property)
        # print "Tag: %s with Property: %s added." %(name, property)
        if result == True:
            LogMessage(sModuleInfo, "Inserted %s - %s in test_case_tag table" % (name, property), 4)
        return "Pass"
    except Exception, e:
        err_msg = LogMessage(sModuleInfo, "Failed to Enter tag for test case %s:%s:%s" % (TC_Id, name, property), 4)
        return err_msg

def Cleanup_TestCase(conn, TC_Id, EditFlag=False, OldFormat=False, New_TC_Id=False):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    LogMessage(sModuleInfo, "Cleaning up:%s" % (TC_Id), 4)
    cur = conn.cursor()

    # 1 - Clean up all tags
    cur.execute("delete from test_case_tag where tc_id = '%s'" % TC_Id)
    conn.commit()

    # 2 - Clean up all expected container, expected datasets, container type data used by expected and master data used by expected
    # Find the test case dataset id for this test case
    Test_Case_DataSet_Id_List = DBUtil.GetData(conn, "select tcdatasetid from test_case_datasets where tc_id = '%s'" % TC_Id)
    for each_Test_Case_DataSet_Id in Test_Case_DataSet_Id_List:

        # find the expected dataset id for this test case
        Expected_Data_Set_Id_List = DBUtil.GetData(conn, "select expectedrefid from expected_datasets where datasetid = '%s'" % each_Test_Case_DataSet_Id)

        for each_Expected_Data_Set_Id in Expected_Data_Set_Id_List:

            if OldFormat == False:

                # Find all the container id's used for this test case's expected
                Container_Data_Id_List = DBUtil.GetData(conn, "select container_name from expected_container where exprefid = '%s'" % each_Expected_Data_Set_Id)

                for each_Container_Data_Id in Container_Data_Id_List:

                    # Find all the container id's used for this test case's expected
                    Master_Data_Id_List = DBUtil.GetData(conn, "select curname from container_type_data where dataid = '%s'" % each_Container_Data_Id)

                    for each_Master_Data_Id in Master_Data_Id_List:

                        # Check if there is address data for this master data id, if yes delete that first
                        Address_Data_Id_List = DBUtil.GetData(conn, "select value from master_data where md_id = '%s' and value ilike '%s%%'" % (each_Master_Data_Id, each_Master_Data_Id))

                        for each_Address_Data_Id in Address_Data_Id_List:

                            # Find and delete the master data entry
                            cur.execute("delete from master_data where md_id = '%s'" % each_Address_Data_Id)
                            conn.commit()

                        # Find and delete the master data entry
                        cur.execute("delete from master_data where md_id = '%s'" % each_Master_Data_Id)
                        conn.commit()

                    # Find and delete the master data entry
                    cur.execute("delete from container_type_data where dataid = '%s'" % each_Container_Data_Id)
                    conn.commit()


            # Find and delete the expected container entries for this test case
            cur.execute("delete from expected_container where exprefid = '%s'" % each_Expected_Data_Set_Id)
            conn.commit()

        # Find and delete the expected container entries for this test case
        cur.execute("delete from expected_datasets where datasetid = '%s'" % each_Test_Case_DataSet_Id)
        conn.commit()

    # 3 - Clean up all test steps data, container type data used for input and master data
    # Find the test case dataset id for this test case
    for each_Test_Case_DataSet_Id in Test_Case_DataSet_Id_List:

        if OldFormat == False:

            # find the container type data id's used for this test case
            Test_Step_Data_Set_Id_List = DBUtil.GetData(conn, "select testdatasetid from test_steps_data where tcdatasetid = '%s'" % each_Test_Case_DataSet_Id)

            for each_Test_Step_Data_Set_Id in Test_Step_Data_Set_Id_List:

                # Find all the container id's used for this test case's in curname field
                Master_Data_Id_List = DBUtil.GetData(conn, "select curname from container_type_data where dataid = '%s'" % each_Test_Step_Data_Set_Id)

                for each_Master_Data_Id in Master_Data_Id_List:

                    # Check if there is address data for this master data id, if yes delete that first
                    Address_Data_Id_List = DBUtil.GetData(conn, "select value from master_data where md_id = '%s' and value ilike '%s%%'" % (each_Master_Data_Id, each_Master_Data_Id))

                    for each_Address_Data_Id in Address_Data_Id_List:

                        # Find and delete the master data entry
                        cur.execute("delete from master_data where md_id = '%s'" % each_Address_Data_Id)
                        conn.commit()

                    # Find and delete the master data entry
                    cur.execute("delete from master_data where md_id = '%s'" % each_Master_Data_Id)
                    conn.commit()

                # Find all the container id's used for this test case's in newname field
                Master_Data_Id_List = DBUtil.GetData(conn, "select newname from container_type_data where dataid = '%s'" % each_Test_Step_Data_Set_Id)

                for each_Master_Data_Id in Master_Data_Id_List:

                    # Check if there is address data for this master data id, if yes delete that first
                    Address_Data_Id_List = DBUtil.GetData(conn, "select value from master_data where md_id = '%s' and value ilike '%s%%'" % (each_Master_Data_Id, each_Master_Data_Id))

                    for each_Address_Data_Id in Address_Data_Id_List:

                        # Find and delete the master data entry
                        cur.execute("delete from master_data where md_id = '%s'" % each_Address_Data_Id)
                        conn.commit()

                    # Find and delete the master data entry
                    cur.execute("delete from master_data where md_id = '%s'" % each_Master_Data_Id)
                    conn.commit()

                # Find and delete the master data entry
                cur.execute("delete from container_type_data where dataid = '%s'" % each_Test_Step_Data_Set_Id)
                conn.commit()

        # Find and delete the master data entry
        cur.execute("delete from test_steps_data where tcdatasetid = '%s'" % each_Test_Case_DataSet_Id)
        conn.commit()

    # 4 - Clean up all test case datasets for this test case
    # Find the test case dataset id for this test case
    cur.execute("delete from test_case_datasets where tc_id = '%s'" % TC_Id)
    conn.commit()

    # 5 - Clean up all test steps
    cur.execute("delete from test_steps where tc_id = '%s'" % TC_Id)
    conn.commit()
    # 6- Clean up all the test  step description from master_data
    cur.execute("delete from master_data where md_id Ilike '%s%%' and field='step' and value='description'" % TC_Id)
    conn.commit()
    
    # 7-Clean up all the test expected result from master_data
    cur.execute("delete from master_data where md_id Ilike '%s%%' and field='expected' and value='result'" % TC_Id)
    conn.commit()
    
    # 8-Clean up all the test verification points in master_data
    cur.execute("delete from master_data where md_id Ilike '%s%%' and field='verification' and value='point'" % TC_Id)
    conn.commit()
    
    # 9-Clean up all the test step estimated time in master_data
    cur.execute("delete from master_data where md_id Ilike '%s%%' and field='estimated' and value='time'" % TC_Id)
    conn.commit()
    if EditFlag == False:

        # 6 - Clean up all test step results
        cur.execute("delete from test_step_results where tc_id = '%s'" % TC_Id)
        conn.commit()

        # 6 - Clean up all test step results
        cur.execute("delete from test_case_results where tc_id = '%s'" % TC_Id)
        conn.commit()

        # 6 - Clean up all test step results
        cur.execute("delete from test_run where tc_id = '%s'" % TC_Id)
        conn.commit()

        # 6 - Clean up all test step results
        cur.execute("delete from test_cases where tc_id = '%s'" % TC_Id)
        conn.commit()
    else:
        if OldFormat:
            # 6 - Update all test step results with new test case id
            DBUtil.UpdateRecordInTable(conn, 'test_step_results', "where tc_id = '%s'" % TC_Id, tc_id=New_TC_Id)

            # 6 - Clean up all test step results
            DBUtil.UpdateRecordInTable(conn, 'test_case_results', "where tc_id = '%s'" % TC_Id, tc_id=New_TC_Id)

            # 6 - Clean up all test step results
            DBUtil.UpdateRecordInTable(conn, 'test_run', "where tc_id = '%s'" % TC_Id, tc_id=New_TC_Id)

            # 6 - Clean up all test step results
            cur.execute("delete from test_cases where tc_id = '%s'" % TC_Id)
            conn.commit()


    LogMessage(sModuleInfo, "Completed Cleaning up:%s" % (TC_Id), 4)

def LogMessage(sModuleInfo, msg, level, debug=True):
        if debug:
            print msg
            CommonUtil.ExecLog(sModuleInfo, msg, level)
        return msg

def Get_PIM_Data_By_Id(conn, Data_Id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    Data_List = []
    SQLQuery = ("select "
    " pmd.md_id,"
    " pmd.field,"
    " pmd.value"
    " from master_data pmd"
    " where"
    " pmd.md_id = '%s';" % (Data_Id))

    Data_List = DBUtil.GetData(conn, SQLQuery, False)
    Data_List = [tuple(x[1:3])for x in Data_List]

    AddressList = []
    for i in range(len(Data_List) - 1, -1, -1):
        eachTuple = Data_List[i]
        if eachTuple[1].startswith(Data_Id):  # or eachTuple[0] == 'Home Address' or eachTuple[0] == 'Other Address':
            if eachTuple[1] != "":
                address_find_SQLQuery = ("select "
                " pmd.field,"
                " pmd.value"
                " from master_data pmd"
                " where"
                " pmd.md_id = '%s'"
                " ;" % (eachTuple[1]))
                AddressData = DBUtil.GetData(conn, address_find_SQLQuery, False)
            else:
                AddressData = ''
            Data_List.pop(i)
            AddressList.append((eachTuple[0], AddressData))
    for eachAddrData in AddressList:
        Data_List.append(eachAddrData)

    return Data_List

def Generate_TCId(Section_Path, tmp_TC_Id):
    # Prefix a 3 letter section name to the tc_id
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        TC_ID_Prefix = ''
        if 'Contacts' in Section_Path:
            TC_ID_Prefix = 'Con'
        elif 'Calendar' in Section_Path:
            TC_ID_Prefix = 'Cal'
        elif 'Backup' in Section_Path or 'Restore' in Section_Path:
            TC_ID_Prefix = 'Bak'
        elif 'Music' in Section_Path:
            TC_ID_Prefix = 'Mus'
        elif 'Video' in Section_Path:
            TC_ID_Prefix = 'Vid'
        elif 'Picture' in Section_Path:
            TC_ID_Prefix = 'Pic'
        elif 'Document' in Section_Path:
            TC_ID_Prefix = 'Doc'
        elif 'PIM' in Section_Path:
            TC_ID_Prefix = 'Pim'
        elif 'Media' in Section_Path:
            TC_ID_Prefix = 'Med'
        elif 'Settings' in Section_Path:
            TC_ID_Prefix = 'Set'
        else:
            TC_ID_Prefix = Section_Path.split('.')[len(Section_Path.split('.')) - 1][:3].upper()

        TC_Id = "%s-%s" % (TC_ID_Prefix.upper(), str(tmp_TC_Id).lstrip('0').zfill(4))

        return TC_Id

    except Exception, e:
        print "Exception:", e
        return tmp_TC_Id

def TestCase_DataValidation(Platform, TC_Name, TC_Type, Priority, Tag_List, Dependency_List, Steps_Data_List, Section_Path, Feature_Path):
     ##########Data Validation: Check if all required input fields have data
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    if Platform == '':
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case Platform", 4)
        return err_msg


    if TC_Name == '':
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case name", 4)
        return err_msg

    if TC_Type == '':
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case type", 4)
        return err_msg

    if Priority == '':
        print "Error. Test case Priority cannot be empty"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case Priority", 4)
        return err_msg

    if Section_Path == '':
        print "Error. Test Section cannot be empty"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case Section", 4)
        return err_msg
    
    if Feature_Path == '':
        print "Error. Test Feature cannot be empty"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case Feature", 4)
        return err_msg

    if not isinstance(Tag_List, list):
        print "Error. Test case tag format is incorrect"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case tag format. It should be a list.", 4)
        return err_msg

    if not isinstance(Dependency_List, list):
        print "Error. Test case dependency format is incorrect"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case dependency format. It should be a list.", 4)
        return err_msg

    if not isinstance(Steps_Data_List, list):
        print "Error. Test case steps format is incorrect"
        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case steps format. It should be a list.", 4)
        return err_msg
    else:
        for eachstepdata in Steps_Data_List:
            if not isinstance(eachstepdata, tuple):
                print "Error. Test case steps format is incorrect for one of the step"
                err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case steps format for one of the step:%s." % eachstepdata, 4)
                return err_msg
            else:
                # first element of tuple should be a string and second element a list
                if not isinstance(eachstepdata[0], basestring) and not isinstance(eachstepdata[1], list) and not isinstance(eachstepdata[2], basestring) and not isinstance(eachstepdata[3], basestring) and not isinstance(eachstepdata[4], basestring):
                    print "Error. Test case steps format is incorrect for one of the step"
                    err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case steps format for one of the step:%s." % eachstepdata, 4)
                    return err_msg

                # stepdata should be a list of lists
                for stepdatalist in eachstepdata[1]:

                    if not isinstance(stepdatalist, list):
                        print "Error. Test case steps format is incorrect for one of the step"
                        err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case steps format for one of the step:%s." % stepdatalist, 4)
                        return err_msg
                    else:

                        for eachdatalist in stepdatalist:

                            if not isinstance(eachdatalist, tuple):
                                print "Error. Test case steps format is incorrect for one of the step"
                                err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case steps format for one of the step:%s." % eachstepdata, 4)
                                return err_msg
                            else:

                                # first element of tuple should be a string and second element a string or list
                                if not (isinstance(eachdatalist[0], basestring) and (isinstance(eachdatalist[1], basestring) or isinstance(eachdatalist[1], list))):
                                    print "Error. Test case steps format is incorrect for one of the step"
                                    err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case steps format for one of the step:%s. It should be a list." % eachdatalist, 4)
                                    return err_msg

                                if isinstance(eachdatalist[1], list):
                                    for eachsubitem in eachdatalist[1]:
                                        if not isinstance(eachsubitem, tuple):
                                            print "Error. Test case steps format is incorrect for one of the step"
                                            err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case steps format for one of the step:%s. It should be a list." % eachsubitem, 4)
                                            return err_msg
                                        else:
                                            if not isinstance(eachdatalist[0], basestring) and not isinstance(eachdatalist[1], basestring):
                                                print "Error. Test case steps format is incorrect for one of the step"
                                                err_msg = LogMessage(sModuleInfo, "TEST CASE CREATION Failed:Invalid test case steps format for one of the step:%s. It should be a list." % eachdatalist, 4)
                                                return err_msg


#        for step in Steps_Data_List:
#            if not isinstance(step,tuple):
#                print "Error. Test case steps format is incorrect (step level)"
#                error = "TEST CASE CREATION Failed:Invalid test case steps format is incorrect. It should be a list."
#                return returnResult(error)
#            if not isinstance(step[1],list):
#                print "Error. Test case steps format is incorrect (data level)"
#                error = "TEST CASE CREATION Failed:Invalid test case steps format is incorrect. It should be a list."
#                return returnResult(error)
#            for data in step[1]:
#                if not isinstance(data,list):
#                    print "Error. Test case steps format is incorrect (data level)"
#                    error = "TEST CASE CREATION Failed:Invalid test case steps format is incorrect. It should be a list."
#                    return returnResult(error)
#                for normalTuple in data:
#                    if not isinstance(normalTuple,tuple):
#                        print "Error. Test case steps format is incorrect (normal tuple level)"
#                        error = "TEST CASE CREATION Failed:Invalid test case steps format is incorrect. It should be a list."
#                        return returnResult(error)
#                    if isinstance(normalTuple[1],list):
#                        for addressTuple in normalTuple[1]:
#                            if not isinstance(addressTuple,tuple):
#                                print "Error. Test case steps format is incorrect (address tuple level)"
#                                error = "TEST CASE CREATION Failed:Invalid test case steps format is incorrect. It should be a list."
#                                return returnResult(error)

    return "Pass"
