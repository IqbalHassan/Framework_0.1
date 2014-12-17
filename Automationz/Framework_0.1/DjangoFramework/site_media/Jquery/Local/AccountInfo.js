/**
 * Created by lent400 on 8/21/14.
 */
var user_name="";
var full_name="";
var project_id="";
var team_id="";
$(document).ready(function(){
    //get all the other information
    user_name=$('#username').val().trim();
    full_name=$('#full_name').val().trim();
    var old_full_name=full_name;
    project_id=$('#selected_project_id  option:selected').val();
    team_id=$('#selected_team_id option:selected').val();

    $('#update').click(function(){
        var last_user_name=$('#username').val().trim();
        var last_full_name=$('#full_name').val().trim();
        var last_project_id=$('#selected_project_id option:selected').val();
        var last_team_id=$('#selected_team_id option:selected').val();

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
        if(team_id===last_team_id){
            team_id="";
        }
        else{
            team_id=last_team_id;
        }
        $.get('UpdateAccountInfo',{
            'old_full_name':old_full_name,
            'user_name':user_name,
            'full_name':full_name,
            'project_id':project_id,
            'team_id':team_id,
            'user_id': $.session.get('user_id')
        },function(data){
            if(data=='true'){
                window.location.reload(true);
            }
        });
    });
    Submit_button_preparation();
    
    $('#remove_profile_picture').on('click', function() {
    	var username = $('#username').val().trim();
//    	console.log('Remove profile picture:', username);
		$.get('/Home/RemoveProfilePicture', {'username': username})
		.done(function(data) {
			 alertify.success('Profile picture removed successfully.<br><span style="font-size: 0.8em;">Reloading in 3 seconds.</span>', 3000);
			 setTimeout(function() {
				 window.location.reload();
			 }, 3000);
		})
		.fail(function() {
			alertify.error('Could not remove profile picture.<br><span style="font-size: 0.8em;">Click to dismiss</span>');
		});
    });
});
function Submit_button_preparation(){
    $('#selected_project_id').on('change',function(){
        $.get('GetTeamInfoPerProject/',{
            'project_id':$(this).val().trim()
        },function(data){
            var team_info=data['teams'];
            var message=createOption(team_info);
            $('#selected_team_id').html(message);
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