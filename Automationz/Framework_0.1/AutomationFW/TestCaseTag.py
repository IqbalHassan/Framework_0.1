'''
Created on Apr 10, 2012

@author: jnibumon3e03
'''
import DataBaseUtilities as DB

def AddTag(conn, tcid, name, property):
    try:
        DB.InsertNewRecordInToTable(conn, 'test_case_tag',
            tc_id='%s' % tcid,
            name='%s' % name,
            property='%s' % property)
        print "Tag: %s with Property: %s added." % (name, property)
        return True
    except Exception, e:
        print "Exception : ", e
        return False

def RemoveTag(conn, tcid, name=None, property=None):
    try:
        if name:
            DB.DeleteRecord(conn, 'test_case_tag',
                            tc_id='%s' % tcid,
                            name='%s' % name
                            )
            print "Tag: %s removed." % (name)
        else:
            DB.DeleteRecord(conn, 'test_case_tag',
                            tc_id='%s' % tcid
                            )
            print "All Tags removed."
        return True
    except Exception, e:
        print "Exception : ", e
        return False

def GetTag(conn, tcid):
    try:
        dataset = DB.GetData(conn, "Select * from test_case_tag where tc_id = '%s' order by name" % tcid, False)
        print "Tags for TCID: %s" % (tcid)
        print dataset
        return True
    except Exception, e:
        print "Exception : ", e
        return False

try:
    conn = DB.ConnectToDataBase()
    #action = raw_input("Enter A to Add Tag, R to Remove Tag or G to Get Tag : ")
    #tcid = raw_input("Enter test case id : ")
    #taglist1 = raw_input("Enter [(tagname1,property1),(tagname2,property3)] :")
    #if tcid:
    tcidlist = [


            ]



    for tcid in tcidlist:
        print "Adding tag for TCID: ", tcid

        taglist = [('%s' % tcid, 'tcid'),
                   ('%s' % tcid, 'MKS'),
        ###########PC TAGS Section#############
                   #('SectionName','Section'),
                   #('Smoke','test_run_type'),
                   ('SI', 'test_run_type'),
                   ('P1', 'Priority'),
                   ('PC', 'machine_os'),
                   ('Default', 'Data_Type'),
                   #('Performance','Data_Type'),
                   #('Localization','Data_Type'),
                   #('SD','device_memory'),
                   #('eMMC','device_memory'),
                   #('iTunes','client'),
                   #('WMP','client'),
                   ('Outlook', 'client'),
                   #('Dependency','SD'),
                   #('Dependency','eMMC'),
                   #('Dependency','iTunes'),
                   #('Dependency','WMP'),
                   ('Dependency', 'Outlook'),
                   ('Status', 'Dev'),

        ###########MAC TAGS Section#############
                   ##('SectionName','MacSection'),
                   #('SI','Mac_test_run_type'),
                   ##('SI','Mac_test_run_type'),
                   #('SVV','Mac_test_run_type'),
                   #('P2','MacPriority'),
                   #('Mac','machine_os'),
                   ##('Performance','Data_Type'),
                   ##('Localization','Data_Type'),
                   ##('SD','device_memory'),
                   ##('eMMC','device_memory'),
                   ##('iTunes','client'),
                   ##('WMP','client'),
                   #('MacNative','client'),
                   ##('MacDependency','SD'),
                   ##('MacDependency','eMMC'),
                   ##('MacDependency','iTunes'),
                   ##('MacDependency','WMP'),
                   #('MacDependency','MacNative'),
                   #('MacStatus','Dev')
                   ]

        for eachtag in taglist:
            name = eachtag[0]
            property = eachtag[1]
            AddTag(conn, tcid, name, property)

    #GetTag(conn,tcid)
    #print "Removing tag for TCID: ",tcid
    #RemoveTag(conn,tcid)

    conn.close()
except Exception, e:
    print "Exception: ", e
