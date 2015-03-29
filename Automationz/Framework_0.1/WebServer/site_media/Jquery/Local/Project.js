$(document).ready(function(){
    $('body').css({'font-size':'100%'});
    GetProjects();
});


function GetProjects(){
    $.get('Get_Projects',{
        user_id: $.session.get('user_id')
    },function(data){
        var message="";
        message+='<option value="">Select Projects</option>';
        if(data.length>0){
            for(var i=0;i<data.length;i++){
                message+='<option value="'+data[i][0]+'">'+data[i][1]+'</option>';
            }
        }
        $('#projects').html(message);

        $('#projects').on('change',function(){
            var project_id=$(this).val().trim();
            var project_name=$('#projects option:selected').text().trim();
            get_all_detail(project_id,project_name,$.session.get('user_id'));
        });
    });
}

function get_all_detail(project_id,project_name,user_id){
    $.get("Small_Project_Detail",{
        'name':project_name
    },function(data){
        var project_name=data['project_name'];
        var project_description=data['project_description'];
        var project_due=data['due_message'];
        var project_owners=data['project_owners'];
        var teams=data['team_name'];
        var message='';
        message+='<table class="two-column-emphasis" width="50%;">';
        message+='<tr><td align="right" style="vertical-align: 0%;"><b>Project Name:</b></td><td align="left">'+project_name+'</td><td width="50%;">&nbsp;</td></tr>';
        message+='<tr><td align="right" style="vertical-align: 0%;"><b>Description:</b></td><td align="left">';
        if(project_description!=''){
            message+=project_description;
        }
        else{
            message+='Project Description not set';
        }
        message+='</td><td width="50%;">&nbsp;</td></tr>';
        message+='<tr><td align="right" style="vertical-align: 0%;"><b>Due In:</b></td><td align="left">'+project_due+'</td><td width="50%;">&nbsp;</td></tr>';
        message+='<tr><td align="right" style="vertical-align: 0%;"><b>Project Owners:</b></td><td align="left">'+project_owners+'</td><td width="50%;">&nbsp;</td></tr>';
        message+='<tr><td align="right" style="vertical-align: 0%;"><b>Teams:</b></td><td align="left">';
        message+='<table>';
        for(var i=0;i<teams.length;i++){
            message+='<tr><td>'+teams[i]+'</td></tr>';
        }
        message+='</table>';
        message+='</td><td width="50%;">&nbsp;</td></tr>';
        message+='<tr><td>&nbsp;';
        message+='</td><td>';
        if(data['owner_tag']){
            message+='<input type="button" id="edit_project" value="Edit Project" class="m-btn purple"/>';
        }
        message+='<input type="button" id="team_manage" value="Manage Teams" class="m-btn green"/></td><td width="50%;">&nbsp;</td></tr>'
        message+='</table>';
        $("#detail_div").html(message);
        $('#team_manage').on('click',function(){
            window.location='/Home/'+project_id+'/ManageTeam/';
        });
        $('#edit_project').on('click',function(){
           window.location='/Home/Project/'+project_id+'/';
        });
    });
}
