$(document).ready(function(){
   GetProjects("");
   ButtonPreparation();
});
function GetProjects(team_name){
    $.get('Get_Projects',{
        'team_name':team_name.trim()
    },function(data){
        var message="";
        message+='<table>';
        if(data.length>0){
            for(var i=0;i<data.length;i++){
                message+=('<tr><td style="cursor: pointer;" class="projects"><b>'+data[i].trim()+'</b></td></tr>');
            }
            message+='</table>';

        }
        else{
            window.location.reload(true);
        }
        $('#projects').html(message);
        PrepareOtherButton();
    });
}
function PrepareOtherButton(){
    $('.projects').click(function(){
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
    $('#id').html('<b class="Text" style="cursor: pointer;color: #4183c4;">'+data['project_id']+' - </b>');
    $('#name').html('<b class="Text" style="cursor: pointer;color: #4183c4">'+data['project_name']+'</b>');
    message+='';
    message+='<table align="left">';
    message+='<tr>';
    message+='<td align="right"><b style="color: #4183c4">Description:</b></td><td>'+data['project_description']+'</td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b style="color: #4183c4">Due in:</b></td><td>'+data['due_message']+'</td>';
    message+='</tr>';
    message+='<tr>';
    message+=('<td align="right"><b style="color: #4183c4">Owners:</b></td><td>'+data['testers'].join(","));
    if(data['managers'].length>0){
        message+=(','+data['managers'].join(',')+'</td>');
    }
    message+='</tr>';
    message+='<tr>';
    message+=('<td align="right"><b style="color: #4183c4">Assigned Teams:</b></td><td>');
    for(var i=0;i<data['team_name'].length;i++){
        var team_name=data['team_name'][i].trim().replace(/ /g,'_').trim();
        var location=("/Home/Team/"+team_name+"/");
        message+=('<a href="'+location +'" style="text-decoration:none">'+data['team_name'][i]+'</a>');
        if(i!=(data['team_name'].length-1)){
            message+=" , ";
        }
    }
    message+='</td>'
    message+='</tr>';
    message+='<tr>';
    message+='<td align="left"><a href="/Home/Project/'+data['project_id'].trim()+'/" style="text-decoration: none;">see details...</a> </td><td>&nbsp;</td>';
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