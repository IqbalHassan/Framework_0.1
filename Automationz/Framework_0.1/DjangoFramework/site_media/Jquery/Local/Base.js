/**
 * Last modified by: sazid on 4/27/14.
 */
$(document).ready(function(){

	// Remember the path so that after the login, the user is redirected back to the same page he/she was trying to view
	current_path = window.location.pathname;
	// Save it to session storage rather than local storage
	sessionStorage.setItem("path_to_redirect", current_path);
	
    if($.session.get('log') !== 'logged' && $(this).attr('title') !== 'Log In')
    {
        window.location = '/Home/Login/';
    }
    
    $(".welcome").text($.session.get('fullname'));

    [].slice.call( document.querySelectorAll( '.progress-button' ) ).forEach( function( bttn, pos ) {
		new UIProgressButton( bttn, {
			callback : function( instance ) {
				s_loadData(instance);
				progress = 0,
					interval = setInterval( function() {
						
						progress = Math.min( progress + Math.random() * 0.1, 1 );
						instance.setProgress( progress );
				        
						if (window.user === "" || window.pwd === "")
				        {
							clearInterval( interval );
				            instance.stop( -1 );
				            $("#loginFieldset").css("border", "6px solid #FB797E");
			            	$("#loginLegened").css({
			            		"border": "6px solid #FB797E",
			            		"background": "#FB797E"
			            	});
				        }

						if ( s_success === true ) {
							clearInterval( interval );
						}
					}, 40 );
			}
		} );
	} );
});


function desktop_notify(message){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    //var button = document.getElementById('submit_button');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification("Logged In!",{body:message, icon:"/site_media/noti.ico"});
    }

    // If the user hasn't told if he wants to be notified or not
    // Note: because of Chrome, we are not sure the permission property
    // is set, therefore it's unsafe to check for the "default" value.
    else if (Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }

            // If the user said okay
            if (status === "granted") {
                var n = new Notification("Logged In!",{body:message, icon:"/site_media/noti.ico"});
            }

            // Otherwise, we can fallback to a regular modal alert
            else {
                alertify.log(message,"",0);
            }
        });
    }

    // If the user refuses to get notified
    else {
        // We can fallback to a regular modal alert
        alertify.log(message,"",0);
    }
}
