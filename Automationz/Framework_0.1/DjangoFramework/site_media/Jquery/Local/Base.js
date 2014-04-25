/**
 * Last modified by: sazid on 4/25/14.
 */
$(document).ready(function(){
<<<<<<< HEAD
=======
    //login
    $('#loginbtn').click(function(e) {
        var user = $('.username').val();
        var pwd = $('.password').val();
        var logged = false;
        var data = [];

        if (user=="" || pwd=="")
        {
            //alert("Fields are empty");
            alertify.log("Fields are empty","",0);
        }
        else
        {
            $.ajax({
                url:'GetUsers/',
                dataType : "json",
                type : "GET",
                data : {
                    user : user,
                    pwd : pwd
                },
                success: function( json ) {
                    //alert(json);
                    /*if(json.length > 0)
                     logged = true;
                     /*for(var i = 0; i < json.length; i++)
                     json[i] = json[i][0].replace(/_/g,' ')
                     $.each(json, function(i, value) {
                     //if(i == 0)return;
                     $(".username[data-level='']").append($('<option>').text(value).attr('value', value));
                     });*/
                    if(json!="User Not Found!")
                    {
                        alertify.log("Logged in as '"+json+"'","",0);
                        desktop_notify("Logged in as '"+json+"'");
                        //location.reload();
                        $.session.set('username', user);
                        $.session.set('fullname', json);
                        $.session.set('log', 'logged');
                        //setTimeout(function(){window.location='/Home/';},3000);
                        window.location.href = '/Home/';
                        $(".welcome").text($.session.get('fullname'));
                        //$("#nav").show();
                    }
                    else{
                        alertify.log("'"+json+"'","",0);
                    }
                },
                error: function(json){
                    alertify.log("Error","",0);}
            });
            /*if(data.length > 0)
             {
             logged = true;
             }*/
            /*if(logged==true)
             {
             alert("Logged In");
             }
             else
             {
             alert("Not Found")
             }*/

        }
        return e.preventDefault();
    });
>>>>>>> df54d7313c25a907112e5f8b61e7f3a52f2a3a9d

	window.interval = 0;
	s_success = false;
	
	function s_loadData(instance) {
		window.user = $('#username').val();
	    window.pwd = $('#password').val();
	    window.logged = false;
	    window.data = [];
		
		$.ajax({
            url:'GetUsers/',
            dataType : "json",
            type : "GET",
            data : {
                user : user,
                pwd : pwd
            },
            success: function( json ) {
                if(json!="User Not Found!")
                {
                	s_success = true;
                	
                	instance.stop( 1 );
                	clearInterval( interval );
                	
                    setTimeout(function(){
                    	window.location='/Home/';
                    }, 1500);
					
					$.session.set('username', user);
                    $.session.set('fullname', json);
                    $.session.set('log', 'logged');
                    
                    $("#loginFieldset").css("border", "6px solid #1ECD97");
                	$("#loginLegened").css({
                		"border": "#1ECD97",
                		"background": "#1ECD97"
                	});
                    
                    $(".welcome").text($.session.get('fullname'));
                }
                else
                {
                	instance.stop( -1 );
                	
                	clearInterval( interval );
                	s_success = false;
                	progress = 0;
                	
                	$("#loginFieldset").css("border", "6px solid #FB797E");
                	$("#loginLegened").css({
                		"border": "#FB797E",
                		"background": "#FB797E"
                	});
                }
            },
            error: function(json){
            	$("#loginFieldset").css("border", "6px solid #FB797E");
            	$("#loginLegened").css({
            		"border": "#FB797E",
            		"background": "#FB797E"
            	});
            	instance.stop( -1 );
            	clearInterval( interval );
            	s_success = false;
            }
        });
	}
	
    $('#username , #password').keypress(function (e) {
        var key = e.which;
        if(key === 13)  // the enter key code
        {
            $("#loginbtn").trigger('click');
        }
    });


    if($.session.get('log') !== 'logged' && $(this).attr('title') !== 'Log In')
    {
        window.location = '/Home/Login/';
    }
    
    $(".welcome").text($.session.get('fullname'));

    $(".logout").click(function(){
        $.session.remove('username');
        $.session.remove('fullname');
        $.session.remove('log');
        window.location = '/Home/Login/';
        $(".welcome").text("");
    });
    
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
			            		"border": "#FB797E",
			            		"background": "#FB797E"
			            	});
				        }

						if ( s_success === true ) {
							clearInterval( interval );
						}
					}, 80 );
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
