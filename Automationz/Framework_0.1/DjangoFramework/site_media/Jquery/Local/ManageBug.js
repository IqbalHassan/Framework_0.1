/**
 * Created by lent400 on 5/23/14.
 */
$(document).ready(function(){
    /*$('#new_task').click(function(event){
        event.preventDefault();
        $.get('FetchProject',{},function(data){
            $('#msg').slideUp("fast");
            $('#RunTestResultTable').html(initCreateDiv(data['project'],data['team'],data['manager']));
            ActivateNecessaryButton();
            ButtonSet();
        });
    });*/



});



/*function initCreateDiv(project,team,manager){
    var message="";
    message+='<table width="100%" style="margin-top: 2%;padding-bottom: 1%;">';
    message+='<tr>';
    message+='<td align="right"><b class="Text" style="text-align: right">Project Name:</b></td>';
    message+='<td><select id="project_name">';
    message+='<option selected>Select Project</option>';
    for(var i=0;i<project.length;i++){
        message+=('<option value="'+project[i].replace(/ /g,'_')+'">'+project[i]+'</option>');
    }
    message+='</select></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Team:</b></td>';
    message+='<td><select id="team_name">';
    message+='<option selected>Select Team</option>';
    for(var i=0;i<team.length;i++){
        message+=('<option value="'+team[i].replace(/ /g,'_')+'">'+team[i]+'</option>');
    }
    message+='</select></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Title:</b></td>';
    message+='<td><input type="text" class="textbox" placeholder="Title Here" id="title"></td>';
    message+='</tr>'
    message+='<tr>';
    message+='<td align="right"><b class="Text">Description:</b></td>';
    message+='<td><textarea  rows="5" cols="70" placeholder="Description for the task within 150 words"></textarea></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Starting Date:</b></td>';
    message+='<td><input type="text"  class="textbox" id="start_date" placeholder="Starting Date Here"></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">End Date:</b></td>';
    message+='<td><input type="text"  class="textbox" id="end_date" placeholder="Completion Date Here"></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Created By:</b></td>';
    message+='<td><select id="created_by"><option selected>Select name from the list</option>';
    for(var i=0;i<manager.length;i++){
        message+=('<option value="'+manager[i].replace(/ /g,'_')+'">'+manager[i]+'</option>');
    }
    message+='</select></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Assigned To:</b></td>';
    message+='<td><input class="textbox" id="assigned_tester" placeholder="Select Testers Here"></td>';
    message+='<td><table><tr id="tester"></tr></table></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Priority:</b></td>';
    message+='<td><select id="priority" class="selectdrop"><option selected value="1">P1(Highest)</option>';
    message+='<option value="2">P2</option>';
    message+='<option value="3">P3</option>';
    message+='<option value="4">P4</option>';
    message+='</select></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Milestone</b></td>';
    message+='<td><input type="text" id="milestone_list" class="textbox" placeholder="Milestone Here"></td>';
    message+='<td><table><tr id="milestone"></tr></table></td>'
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">Status:</b></td>';
    message+='<td><select id="status" class="selectdrop"><option selected value="Unconfirmed">Unconfirmed</option>';
    message+='<option value="New">New</option>';
    message+='<option value="Assigned">Assigned</option>';
    message+='<option value="Reopened">Reopened</option>';
    message+='<option value="Ready">Ready</option>';
    message+='<option value="Resolved">Resolved</option>';
    message+='<option value="Verified">Verified</option>';
    message+='</select></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td>&nbsp;</td>';
    message+='<td><input type="button" class="button primary" value="Submit"/></td>';
    message+='</tr>';
    message+='</table>';
    return message;
}*/