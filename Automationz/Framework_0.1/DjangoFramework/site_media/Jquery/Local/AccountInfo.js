/**
 * Created by lent400 on 8/21/14.
 */
var user_name="";
var full_name="";
var project_id="";
var team_id="";
$(document).ready(function(){
    //get all the other information
    user_name=$('#user_name').val().trim();
    full_name=$('#full_name').val().trim();
    project_id=$('#project_id  option:selected').val();
    team_id=$('#team_id option:selected').val();
    Submit_button_preparation();
});
function Submit_button_preparation(){
    $('#selected_project_id').on('change',function(){
        $.get('GetTeamInfoPerProject/',{
            'project_id':$(this).val().trim()
        },function(data){
            var team_info=data['teams'];
            var message=createOption(team_info);
            $('#team_info').html(message);
        });
    });
    $('#update').click(function(){
        var last_user_name=$('#user_name').val().trim();
        var last_full_name=$('#full_name').val().trim();
        var last_project_id=$('#project_id option:selected').val();
        var last_team_id=$('#team_id option:selected').val();

        if(user_name===last_user_name){
            user_name="";
        }
        else{
            user_name=last_user_name;
        }
        if(full_name===last_full_name){
            full_name="";
        }
        else{
            full_name=last_full_name;
        }
        if(project_id===last_project_id){
            project_id="";
        }
        else{
            project_id=last_project_id;
        }
        if(team_id=last_team_id){
            team_id="";
        }
        else{
            team_id=last_team_id;
        }
        $.get('UpdateAccountInfo/',{
            'user_name':user_name.trim(),
            'full_name':full_name.trim(),
            'project_id':project_id.trim(),
            'team_id':team_id.trim()
        },function(data){

        });
    });
}
function createOption(team_info){
    var message="";
    message+=('<option>Select Teams</option>');
    for(var i=0;i<team_info.length;i++){
        message+=('<option value="'+team_info[i][0]+'">'+team_info[i][1]+'</option>');
    }
    return message;
}