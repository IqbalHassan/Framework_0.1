# -*- coding: cp1252 -*-
from jira.client import JIRA

def Jira_Get_Open(jira_id_list):
    JIRA(options={'server': 'https://jiraurl'})
    jira = JIRA(basic_auth=('username', 'password'))
    jira_open_list = []
    jira_id_title = []
    for each_issue in jira_id_list:
        jira_id_title = []
        try:
            issue = jira.issue(each_issue)
            current_status = issue.fields.status.name
            issue_summary = issue.fields.summary
            if not "Close" in current_status:
                jira_id_title.append(each_issue)
                jira_id_title.append(issue_summary)
                jira_open_list.append(jira_id_title)

        except:
            print "Not a valid Jira"
    return jira_open_list

