# -*- coding: cp1252 -*-

'''
Created on 2011-10-06
@author: ihossain
'''
#import xlrd # Excel file need this: http://pypi.python.org/pypi/xlrd
import sys
#import glob
import os
import subprocess as sp
if os.name == 'nt':
    import WinCommonFoldersPaths as wincom
elif os.name == 'posix':
    import MacCommonFoldersPaths as wincom
    
            
"""
    Description:
    - This module can be used to find all related devtask item for the test case
    - It will return you list of MKS id and their status as a list

    Parameter Description:
    - tc_list = You will need to send a list of MKS item to the module Find_DevTask

    Example: 
    All_Issues = Find_DevTask(['5720171','4973387'])
    returns:
    [[['5884423', 'Verification (Closed)'], ['5908980', 'Closed'], ['5783869', 'Closed'], ['5722747', 'Closed']], []]
    
    ======= End of Instruction: =========
"""    
    

def single_dev_task (tc_id): 
    try:
#        filepath = r'C:\Program Files\Integrity'
        #filepath = r"%s\%s" %( wincom.Get_Program_Files_Path(), "Integrity" )
        #Existinance_of_Library = os.path.exists(filepath)
        #if Existinance_of_Library != True:
        if os.path.exists(wincom.Get_Program_Files_Path() + os.sep + 'Integrity') or os.path.exists(r'C:\Program Files\Integrity'):
            print "Integrity is installed"
        else: 
            print "Integrity is not installed"
            return False
        
        global related_issues
        related_issues=[]
        #in this block we find all the sessions
        failed_session_id = []
        session_id = "tm results --caseID=" + tc_id
        p = sp.Popen(session_id, stdout=sp.PIPE)
        session_id_output = p.communicate()[0]
        session_id_array_with_empty = session_id_output.split("\n" )
        #print session_id_array_with_empty
        
        #cleanup any empty run and complie list of non passed session id
        session_id_array = []
        for item in session_id_array_with_empty:
            if item != '':
                session_id_array.append(item)            
        for item in session_id_array:
            #if not "Passed" in item:
            session_id_temp =item.split("\t")
            verify_session_id = session_id_temp[0]
            digit_or_not = verify_session_id.isdigit()
            if digit_or_not == True:
                failed_session_id.append(session_id_temp[0])
        #print failed_session_id
        
        #in this block we find related item in each session id from above
        related_issues=[]
        for each_session_result in failed_session_id:
            #print "session results %s" %each_session_result
            session_results_command = "tm viewresult --sessionid" +" "+ each_session_result + " " +tc_id
            #get full output to session_result
            p = sp.Popen(session_results_command, stdout=sp.PIPE)
            session_results = p.communicate()[0]
            #converting to array by splitting each line
            session_results_array = session_results.split("\n" ) 
            #calculating if there is any devtask item present 
            start_index = session_results_array.index('Related Items: ')
            end_index = session_results_array.index('Attachments: ')
            total_item_in_btween = end_index-start_index 
            if total_item_in_btween != 1:
                i = 1
                while (i!=total_item_in_btween):
                    temp_devtask = session_results_array[(start_index+i)]
                    if temp_devtask not in related_issues:
                        related_issues.append(temp_devtask)
                    i = i + 1
        #in this block we find out the status of all the issues we collected
        all_issues_status = []
        #print "related issues"
        if related_issues != []:
            #print "No related issues found for TC: %s"  %tc_id
            for item in related_issues: 
                single_issue = []
                issue_status = "im issues --fields=id,summary,type,state,'dev task component' " + item
                p = sp.Popen(issue_status, stdout=sp.PIPE)
                issue_status_output = p.communicate()[0]
                
                issue_status_array = issue_status_output.split("\t")
                #print issue_status_array
                #devtask= issue_status_array[0].replace("\n", "")
                #status= issue_status_array[2].replace("\n", "")
                state= issue_status_array[3]
                devtaskcomponent = issue_status_array[4]
                if os.name == 'nt' and 'Mac' not in devtaskcomponent:               
                    if "Closed" not in state:
                        single_issue.append((issue_status_array[0].replace("\n", "")))
                        single_issue.append((issue_status_array[1].replace("\n", "")))
                        single_issue.append(issue_status_array[3].replace("\n", ""))
                        all_issues_status.append(single_issue)
                        #print "no closed items"
                        #print state
                        #return
                elif os.name == 'posix' and 'Mac' in devtaskcomponent:               
                    if "Closed" not in state:
                        single_issue.append((issue_status_array[0].replace("\n", "")))
                        single_issue.append((issue_status_array[1].replace("\n", "")))
                        single_issue.append(issue_status_array[3].replace("\n", ""))
                        all_issues_status.append(single_issue)
                        #print "no closed items"
                        #print state
                        #return
    
                
                '''
                if state contains 'closed':
                    print "closed"
                else:
                    print "not closed"

                single_issue.append((issue_status_array[0].replace("\n", "")))
                single_issue.append((issue_status_array[1].replace("\n", "")))
                single_issue.append(issue_status_array[3].replace("\n", ""))
                all_issues_status.append(single_issue)
                '''
        print "Issues found for TC: %s --> %s" %(tc_id, all_issues_status)
        return all_issues_status

    except Exception, e:
        print "Unable to retrieve MKS information: %s"  %e
        return False
    

#All_Issues = dev_task("5682071")

def Find_DevTask(tc_list):
    all_dev_task_tc=[]
    for item in tc_list:
        dev_task_list = single_dev_task (item)
        if dev_task_list == False:
            return False
        all_dev_task_tc.append(dev_task_list)
    return all_dev_task_tc

#All_Issues = Find_DevTask(['4413066', '4407278', '4435108', '4434955', '4407264', '4407316', '4407336', '4972995', '4435107', '4407333', '4406465', '4434954', '4407329'])
#All_Issues = Find_DevTask(['4434730'])

#print All_Issues


