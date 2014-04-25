/**
 * Last modified by: sazid on 4/25/14.
 */
$(document).ready(function(){

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