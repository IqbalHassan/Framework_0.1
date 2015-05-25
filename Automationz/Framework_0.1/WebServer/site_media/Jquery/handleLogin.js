/**
 * Bismillahir Rahmanir Rahim, ALLAHU AKBAR
 * Author: Sazid
 */

$(document).ready(function() {
	$("#loginbtn").click(function(e) {
		e.preventDefault();
		
		var username = $("#username").val();
		var password = $("#password").val();
		
		// Code for checkbox and username state storage
		if ($("#username_checkbox").prop("checked")) {
			localStorage.setItem("username", username);
			localStorage.setItem("username_saved", true);
		} else {
			localStorage.removeItem("username");
			localStorage.removeItem("username_saved");
		}
		
		$.ajax({
				url: "GetUsers/",
				data: {"user" : username, "pwd" : password},
				type: "GET",
				dataType: "json",
				success: function(data) {
					if (data['message'] === 'User Not Found!') {
						alertify.error("Incorrect User Name");
						$("#password").val("");
					} 
					else if (data['message'] === 'Incorrect Password') {
						alertify.error("Incorrect Password");
						$("#password").val("");
					} 
					
					
					else {
						alertify.success("Welcome, " + data['message'][1]);
						var path_to_redirect = sessionStorage.getItem("path_to_redirect");
						if(data['message'][2]=='admin'){
                            var path_to_redirect="/Home/superAdmin/";
                        }
                        else{
                            if (path_to_redirect == null){
                                var path_to_redirect = "/Home/Dashboard/"
                            }
                        }
                        /*
						setTimeout(function() 
						{
                           alertify.success("Redirecting you to the previous page.");
						}, 1000);
						*/
						
						$.session.set('username', username);
	                    $.session.set('fullname', data['message'][1]);
                        $.session.set('user_type',data['message'][2]);
	                    $.session.set('log', 'logged');
	                    $.session.set('project_id', data['project_id']);
						$.session.set('project_name',data['project_name']);
                        $.session.set('default_team_identity',data['team_id']);
                        //$.session.set('default_team_name',data['team_name']);
                        $.session.set('user_id',data['message'][0]);
                        $('#project_identity').val(data['project_id']);
                        $('#default_team_identity').val(data['team_id']);
                        setTimeout(function() {
							window.location.href = path_to_redirect;
						}, 1500);
					}

                    /*var user = $.session.get('fullname');
                    $.get("GetAssignedTests",{user : user},function(data)
                    {
                        $.session.set('testing',data['TableData'].length);
                        //ResultTable(ass_tasks,data['Heading'],data['TableData'],"Assigned Tasks");
                    });
                    $.get("GetRequirements",{user : user},function(data)
                    {
                        $.session.set('requires',data['TableData'].length);
                    });*/
				}
		});
	});
});
