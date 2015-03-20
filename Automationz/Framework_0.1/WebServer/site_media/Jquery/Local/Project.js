$(document).ready(function(){
   GetProjects();
   ButtonPreparation();
});
function GetProjects(){
    $.get('Get_Projects',{
        user_id: $.session.get('user_id')
    },function(data){
        var message="";
        if(data.length>0){
            for(var i=0;i<data.length;i++){
                message+=('<tr><td style="cursor: pointer;" class="projects"><b>'+data[i][1].trim()+'</b></td></tr>');
            }
        }
        $('#projects').html(message);
        PrepareOtherButton();
    });
}
function PrepareOtherButton(){
    $('.projects').on('click',function(){
        $('.projects').css({'background-color':'#fff'});
        $(this).css({'background-color':'#ccc'});

        $('.projects').removeClass('selected');
        $(this).addClass('selected');
        $.get("Small_Project_Detail",{
                'name':$(this).text().trim()
            },function(data){
            console.log(data);
            $('#detail_div').html(Small_Project_Detail(data));
        });
    });
}
function Small_Project_Detail(data){
    var message="";
    message+='<table align="left" class="two-column-emphasis">';
    message+='<tr>';
    message+='<td align="right"><b style="color: #4183c4">Description:</b></td><td>'+data['project_description']+'</td><td width="50%;">&nbsp;</td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b style="color: #4183c4">Due in:</b></td><td>'+data['due_message']+'</td>';
    message+='</tr>';
    message+='<tr>';
    message+=('<td align="right"><b style="color: #4183c4">Owners:</b></td><td>'+data['project_owners']);
    message+='</tr>';
    message+='<tr>';
    message+=('<td align="right" style="vertical-align: 0%;"><b style="color: #4183c4">Assigned Teams:</b></td><td style="vertical-align: 0%;"><table>');
    if(data['team_name'].length>0 && data['team_name'][0]!='Team Not Set'){
        for(var i=0;i<data['team_name'].length;i++){
            var team_name=data['team_name'][i].trim().replace(/ /g,'_').trim();
            var location=("/Home/"+data['project_id']+"/Team/"+team_name+"/");
            message+=('<tr><td><a href="'+location +'" style="text-decoration:none">'+data['team_name'][i]+'</a></td></tr>');
        }
    }
    else{
        message+='<tr><td><b>No Team Set</b></td></tr>';
    }
    message+='</table>'
    message+='</td>'
    message+='</tr>';
    message+='</table>';
    return message;
}
function ButtonPreparation(){
    $('#start_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#end_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#create_project').click(function(){
        var project_name=$('#project_name').val().trim();
        var project_desc=$('#project_desc').val().trim();
        var start_date=$('#start_date').val().trim();
        var end_date=$('#end_date').val().trim();
        var team=[];
        $('input[name="team"]:checked').each(function(){
            team.push($(this).val().trim());
        });
        var managers=[];
        var testers=[];
        $('input[name="owner"]:checked').each(function(){
            if($(this).attr('data-id')=='assigned_tester'){
                testers.push($(this).val().trim());
            }
            if($(this).attr('data-id')=='manager'){
                managers.push($(this).val().trim());
            }
        });
        var owners=('assigned_tester:'+testers.join(',')+('-')+('managers:')+managers.join(','));
        $.get("Create_New_Project",{
            'name':project_name.trim(),
            'description':project_desc.trim(),
            'start_date':start_date.trim(),
            'end_date':end_date.trim(),
            'team':team.join('|').trim(),
            'owners':owners.trim(),
            'user_name':$('#user_name').text().trim()
        },function(data){
            if(data['message'].indexOf('Failed')!=0){
                window.location=("/Home/Project/"+data['project_id']+"/");
            }
            else{
                window.location.reload(true);
            }
        });
    });

}