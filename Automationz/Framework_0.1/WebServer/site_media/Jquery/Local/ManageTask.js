/**
 * Created by lent400 on 5/22/14.
 */
/*$(document).ready(function(){
    $('#new_task').click(function(event){
        event.preventDefault();
        $.get('FetchProject',{},function(data){
            $('#msg').slideUp("fast");
            $('#RunTestResultTable').html(initCreateDiv(data['project'],data['team'],data['manager']));
            ActivateNecessaryButton();
            ButtonSet();
        });
    });
});
function ButtonSet(){
    $("#assigned_tester").autocomplete({

        source : 'AutoCompleteTesterSearch',
        select : function(event, ui) {

            var value = ui.item.value
            $("#tester").append('<td><img class="delete" id = "DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                + '<td class="Text">'
                + value
                + ":&nbsp"
                + '</td>');

            //$("#tester th").css('display', 'block');

            $("#assigned_tester").val("");
            return false;

        }
    });
    $("#assigned_tester").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteTester").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
    $('#milestone_list').autocomplete({
        source:function(request,response){
            $.ajax({
                url:"AutoMileStone",
                dataType:"json",
                data:{term:request.term},
                success:function(data){
                    response(data);
                }
            });
        },
        select:function(request,ui){
            var value=ui.item[0].trim();
            if (value!=""){
                //$(this).val(value.trim());
                $("#milestone").html('<td><img class="delete" id = "DeleteMileStone" title = "Delete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                    + '<td class="Text">'
                    + value
                    + ":&nbsp"
                    + '</td>');

                //$("#MileStoneHeader th").css('display', 'block');

                $("#milestone_list").val("");
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
            .appendTo( ul );
    };
    $("#milestone_list").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteMileStone").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
}
function ActivateNecessaryButton(){
    $('#start_date').datepicker({ dateFormat: "dd-mm-yy" });
    $('#start_date').datepicker("option", "showAnim", "slide" );
    $('#end_date').datepicker({ dateFormat: "dd-mm-yy" });
    $('#end_date').datepicker("option", "showAnim", "slide" );
}
function initCreateDiv(project,team,manager){
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
    message+='<td><input type="text"  class="textbox" id="start_date" placeholder="Project Starting Date Here"></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b class="Text">End Date:</b></td>';
    message+='<td><input type="text"  class="textbox" id="end_date" placeholder="Project Completion Date Here"></td>';
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
    message+='<td><select id="priority"><option selected value="1">P1(Highest)</option>';
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
    message+='<td><select id="status"><option selected value="not_started">Not Started</option>';
    message+='<option value="started">Started</option>';
    message+='<option value="completed">Complete</option>';
    message+='<option value="over_due">OverDue</option>';
    message+='</select></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td>&nbsp;</td>';
    message+='<td><input type="button" class="button primary" value="Submit"/></td>';
    message+='</tr>';
    message+='</table>';
    return message;
}*/
var label_per_page=5;
var label_page_current=1;
var project_id= $.session.get('project_id');
var team_id= $.session.get('default_team_identity');
var user = $.session.get('fullname');
$(document).ready(function(){
    primarySettings();

    $("#simple-menu").sidr({
        name: 'sidr',
        side: 'left'
    });

    $('#project_identity').on('change',function(){
        $.session.set('project_id',$(this).val());
        window.location.reload(true);
    });

    $('#default_team_identity').on('change',function(){
        $.session.set('default_team_identity',$(this).val());
        window.location.reload(true);
    });

    $.get("Tasks_List",{project_id : project_id, team_id:team_id},function(data)
    {
        if(data['tasks'].length>0) {
            //make a table column
            var message = "";
            message += '<table class="one-column-emphasis">';
            message += '<tr>';
            for (var i = 0; i < data['Heading'].length; i++) {
                message += '<th align="left">' + data['Heading'][i] + '</th>';
            }
            message += '</tr>';
            for (var i = 0; i < data['tasks'].length; i++) {
                message += '<tr>';
                for (var j = 0; j < data['tasks'][i].length; j++) {
                    message += '<td align="left">' + data['tasks'][i][j] + '</td>';


                }
                message += '</tr>';
            }
            message += '</table>';
            $('#allTasks').html(message);
            make_clickable('#allTasks');


        }
        else{
            $("#allTasks").html('<h2>No Data Available</h2>')
        }
    });


    get_labels(project_id,team_id,label_per_page,label_page_current);

    label_per_page = $("#perpageitem").val();
    $('#perpageitem').on('change',function(){
        if($(this).val()!=''){
            label_per_page=$(this).val();
            label_page_current=1;
            $('#pagination_tab').pagination('destroy');
            window.location.hash = "#1";
            get_labels(project_id,team_id,label_per_page,label_page_current);
        }
    });

});

function primarySettings(){
    $('#project_code').text($.session.get('project_id'));
    $('#create_new_task').click(function(event){
        event.preventDefault();
        window.location=('/Home/'+ $.session.get('project_id')+'/CreateTask/');
    });
}

function make_clickable(divname) {
    $(divname + ' tr>td:first-child').each(function () {
        $(this).css({
            'color': 'blue',
            'cursor': 'pointer',
            'textAlign': 'left'
        });
        $(this).click(function(){
            var location='/Home/'+$.session.get('project_id')+'/EditTask/'+$(this).text().trim()+'/';
            window.location=location;
        });
    });


    $(divname + ' tr>td:last-child').each(function () {
        /*if($(this).text()!=("None")){
            $(this).css({
                'color': 'blue',
                'cursor': 'pointer',
                'textAlign': 'left'
            });
        }*/
        var divider = $(this).lastIndexOf("/");
        
        console.log(divider);

    });
}

function get_labels(project_id,team_id,label_per_page,label_page_current){
    $.get("Show_Tasks",{'project_id':project_id ,'team_id':team_id,'label_per_page':label_per_page,'label_page_current':label_page_current},function(data){
        form_table("AllMSTable",data['Heading'],data['TableData'],data['Count'],"Tasks");
        
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