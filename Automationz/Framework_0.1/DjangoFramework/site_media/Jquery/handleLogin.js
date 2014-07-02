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
						alertify.error("No user found with the provided details.");
						$("#password").val("");
					} else {
						alertify.success("Welcome, " + data['message']);
						var path_to_redirect = sessionStorage.getItem("path_to_redirect");
						
						setTimeout(function() {
							alertify.success("Redirecting you to the previous page.");
						}, 1000);
						
						
						$.session.set('username', username);
	                    $.session.set('fullname', data['message']);
	                    $.session.set('log', 'logged');
	                    //$.session.set('project_id', 'PROJ-15');
						setTimeout(function() {
							window.location.href = path_to_redirect;
						}, 1500);
					}
				}
		});
	});
});
