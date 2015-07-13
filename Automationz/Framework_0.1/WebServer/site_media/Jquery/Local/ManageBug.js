/**
 * Created by lent400 on 5/23/14.
 */


var label_per_page=10;
var label_page_current=1;
var project_id= $.session.get('project_id');
var team_id= $.session.get('default_team_identity');
var user = $.session.get('fullname');

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
    $("#header").html($.session.get('project_id')+' / Manage Bugs');

    $("#simple-menu").sidr({
        name: 'sidr',
        side: 'left'
    });

    $.get("Bugs_List/",{project:project_id,team:team_id},function(data) {
        /*$(data['bugs']).each(function(i){

            per_bug = '<div style="padding-top: 10px;padding-bottom: 10px;padding: 1px 10px;background: #fff;border: 1px solid #d8d8d8;border-top: 0px;border-bottom-left-radius: 3px;border-bottom-right-radius: 3px;color: #666;font-size: 13px;">' +

            '<table style="width: 100%; margin: 0.8%">' +
            '<tr>'+
            '<td>'+
            '<a href="/Home/EditBug/' +
            data['bugs'][i][0] +
            '" class="bugs-title">' +
            data['bugs'][i][1] +
            '</a>&nbsp;&nbsp;';
            $(data['labels']).each(function(j){
                 if(data['labels'][j][0]==data['bugs'][i][0]){
                     per_bug += '<a href="" class="label" style="background-color: ' +
                     data['labels'][j][3] +
                     ';padding: 3px 4px;font-size: 11px; min-width: 10px">' +
                     data['labels'][j][2] +
                     '</a>&nbsp;';
                 }
            });
            //per_bug += '<a href="" class="label" style="background-color: #fbda04;padding: 3px 4px;font-size: 11px; min-width: 10px">' +
            //'minar' +
            //'</a>' +
            per_bug += '</td>' +
            '</tr>'+
            '<tr>'+
            '<td style="font-size: 12px">' +
            data['bugs'][i][0] +
            ' opened on ' +
            data['bugs'][i][8] +
            ' by ' +
            data['bugs'][i][7] +
            '</td>' +
            '</tr>' +
            '</table>' +

            '</div>';
            $("#bugs_list").append(per_bug);
        })*/

        if(data['bugs'].length>0) {
            //make a table column
            var message = "";
            message += '<table class="one-column-emphasis">';
            message += '<tr>';
            for (var i = 0; i < data['Heading'].length; i++) {
                message += '<th align="left">' + data['Heading'][i] + '</th>';
            }
            message += '</tr>'
            for (var i = 0; i < data['bugs'].length; i++) {
                message += '<tr>';
                for (var j = 0; j < data['bugs'][i].length; j++) {
                    message += '<td align="left">' + data['bugs'][i][j] + '</td>';

                }
                message += '</tr>';
            }
            message += '</table>';
            $('#allBugs').html(message);
            make_clickable('#allBugs');

        }
        else{
            $("#allBugs").html('<h2>No Data Available</h2>')
        }
    });


    get_labels(project_id,team_id,label_per_page,label_page_current);

    label_per_page = $("#perpageitem").val();
    $('#perpageitem').on('change',function(){
        if($(this).val()!=''){
            label_per_page=$(this).val();
            label_page_current=1;
            $('#pagination_div').pagination('destroy');
            window.location.hash = "#1";
            get_labels(project_id,team_id,label_per_page,label_page_current);
        }
    });


});


function make_clickable(divname) {
    $(divname + ' tr>td:first-child').each(function () {
        $(this).css({
            'color': 'blue',
            'cursor': 'pointer',
            'textAlign': 'left'
        });
        $(this).click(function(){
            var location='/Home/EditBug/'+$(this).text().trim()+'/';
            window.location=location;
        });
    });
}


function get_labels(project_id,team_id,label_per_page,label_page_current){
    $.get("Show_Bugs",{'project_id':project_id ,'team_id':team_id,'label_per_page':label_per_page,'label_page_current':label_page_current},function(data){
        form_table("AllMSTable",data['Heading'],data['TableData'],data['Count'],"Bugs");
        
        $('#pagination_div').pagination({
            items:data['Count'],
            itemsOnPage:label_per_page,
            cssStyle: 'dark-theme',
            currentPage:label_page_current,
            displayedPages:2,
            edges:2,
            hrefTextPrefix:'#',
            onPageClick:function(PageNumber){
                get_labels(project_id,team_id,label_per_page,PageNumber);
            }
        });
    });
}


function form_table(divname,column,data,total_data,type_case){
    var tooltip=type_case||':)';
    var message='';
    message+= "<p class='Text hint--right hint--bounce hint--rounded' data-hint='" + tooltip + "' style='color:#0000ff; font-size:14px; padding-left: 12px;'>" + total_data + " " + type_case+"</p>";
    message+='<table class="two-column-emphasis">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<th>'+column[i]+'</th>';
    }
    message+='</tr>';
    for(var i=0;i<data.length;i++){
        message+='<tr>';
        for(var j=0;j<data[i].length;j++){
            switch(data[i][j]){
                case 'Dev':
                    message+='<td style="background-color: ' + colors['dev'] + '; color: #fff;">' + data[i][j] + '</td>';
                    continue;
                case 'Ready':
                    message+='<td style="background-color: ' + colors['ready'] + '; color: #fff;">' + data[i][j] + '</td>';
                    continue;
                default :
                    message+='<td>'+data[i][j]+'</td>';
                    continue;
            }
        }
        message+='</tr>';
    }
    message+='</table>';
    $('#'+divname).html(message);
    make_clickable('#'+divname);
}

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