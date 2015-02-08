/**
 * Created by lent400 on 8/21/14.
 */
var user_name="";
var full_name="";
var project_id="";
var team_id="";

var projects=[]
$(document).ready(function(){
    //get all the other information
    user_name=$('#username').val().trim();
    full_name=$('#user_full_name').val().trim();
    var old_full_name=full_name;
    project_id=$('#selected_project_id  option:selected').val();
    team_id=$('#selected_team_id option:selected').val();
    get_all_info($.session.get('user_id'))
    $('#update').click(function(){
        var last_user_name=$('#username').val().trim();
        var last_full_name=$('#user_full_name').val().trim();
        var last_project_id=$('#selected_project_id option:selected').val();
        var last_team_id=$('#selected_team_id option:selected').val();
        $.get('UpdateAccountInfo/',{
            'user_name':last_user_name,
            'full_name':last_full_name,
            'project_id':last_project_id,
            'team_id':last_team_id,
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
        //get the project_id
        var project_id=$(this).val();
        var message="";
        message+='<option value="">Teams</option>'
        for(var i=0;i<projects.length;i++){
            if(projects[i][0]==project_id){
                var team_list=projects[i][2];
                for(var j=0;j<team_list.length;j++){
                    message+='<option value="'+team_list[j][0]+'">'+team_list[j][1]+'</option>';
                }
            }
        }
        $('#selected_team_id').html(message);
        /*$.get('GetTeamInfoPerProject/',{
            'project_id':$(this).val().trim()
        },function(data){
            var team_info=data['teams'];
            var message=createOption(team_info);
            $('#selected_team_id').html(message);
        });*/
    });
}

function get_all_info(user_id){
    $.get('ProfileDetail/',{user_id:user_id},function(data){
        console.log(data);
        projects=data['projects'];
        $('#user_full_name').val(data['FullName']);
        $('#designation').val(data['Designation']);
        $('#username').val(data['Username']);
        $('#image_username').val(data['Username']);
        $('#image_user_id').val(data['UserID']);
        var message='';
        message+='<option value="">Project ID</option>';
        for (var i=0;i<projects.length;i++){
            message+='<option value="'+projects[i][0]+'">'+projects[i][1]+'</option>';
        }
        $('#selected_project_id').html(message);
        $('#selected_project_id').val(data['selected_project_id']);
        var message="";
        message+='<option value="">Teams</option>'
        for(var i=0;i<projects.length;i++){
            if(projects[i][0]==data['selected_project_id']){
                var team_list=projects[i][2];
                for(var j=0;j<team_list.length;j++){
                    message+='<option value="'+team_list[j][0]+'">'+team_list[j][1]+'</option>';
                }
                break;
            }
        }
        $('#selected_team_id').html(message);
        $('#selected_team_id').val(data['selected_team_id']);
    });
}