/**
 * Last modified by: sazid on 4/25/14.
 */

/******** For menu bar *********/
(function($) {

  $.fn.menumaker = function(options) {
      
      var cssmenu = $(this), settings = $.extend({
        title: "Menu",
        format: "dropdown",
        sticky: false
      }, options);

      return this.each(function() {
        cssmenu.find('li ul').parent().addClass('has-sub');
        // if (settings.sticky === true) cssmenu.css('position', 'fixed');
        
        return;

      });
  };
})(jQuery);

/**********************************/

$(document).ready(function(){

	// Initialize the desktop navigation menu
	$("#cssmenu").menumaker({
	   title: "Menu",
	   format: "multitoggle"
	});
	
	$("#cssmenu").slicknav({
		label: 'Automation Solutionz'
	});
	
	$("#team_project_menu").sidr({
		name: 'team_project_panel',
		side: 'right'
	});
	
//	$(window).on('resize', function(e) {
//		$("#cssmenu").slicknav();
//	});
	
	// Remember the path so that after the login, the user is redirected back to the same page he/she was trying to view
	current_path = window.location.pathname;
	// Save it to session storage rather than local storage
	if (current_path === '/Home/Login/' || current_path === '/' || current_path === '/Home/') {
		sessionStorage.setItem("path_to_redirect", '/Home/Dashboard/');
	} else {
        //sessionStorage.setItem("path_to_redirect", '/Home/User/');
		sessionStorage.setItem("path_to_redirect", current_path);
	}

    if($.session.get('log') !== 'logged' && $(this).attr('title') !== 'Log In')
    {
        window.location = '/Home/Login/';
    }
    
    // Set the '.welcome'-class elements' text to the user's name
    $(".welcome").text($.session.get('fullname'));
    
    $.get('GetProjectNameForTopBar',{
        'user_id': $.session.get('user_id')
    },function(data){
        var message="";
        var projects=data['projects'];
        for(var i=0;i<projects.length;i++){
            message+=('<option value="'+projects[i][0]+'">'+projects[i][0]+'</option> ');
        }
        $('#project_identity').append(message);
        $('#project_identity').val($.session.get('project_id'));
        var message="";
        var teams=data['teams'];
        for(var i=0;i<teams.length;i++){
            message+=('<option value="'+teams[i][0]+'">'+teams[i][1]+'</option>');
        }
        $('#default_team_identity').append(message);
        $('#default_team_identity').val($.session.get('default_team_identity'));
    });
    
    // -------------- Mobile navigation ------------------ //
	
//    // Create and attach a 'select' element
//    $('<select />').appendTo('#mobile-menu');
//	
//    // Add the default option in case everything else fails
//	$('<option />', {
//		'selected': 'selected',
//		'value': '#',
//		'text': 'Select a page...'
//	}).appendTo('#mobile-menu select');
//	
//	/*
//	 * Create the required 'option' elements and set their
//	 * 'value' and 'text' attributes accordingly, from the
//	 * desktop navigation menu
//	 */
//	$('#cssmenu ul a').each(function() {
//		var el = $(this);
//		if (el.parents('.has-sub').length && !(el.attr('href') === '#')) {
//			$('<option />', {
//				'value': el.attr('href'),
//				'text': el.text()
//			}).appendTo('nav select');
//		} else if (el.text() === '') {
//			$('<option />', {
//				'value': el.attr('href'),
//				'text': 'Home'
//			}).appendTo('nav select');
//		}
//		/* else if (el.parents('.has-sub').length == 1) {
//			$('<option />', {
//				'value': el.attr('href'),
//				'text': '- ' + el.text()
//			}).appendTo('nav select');
//		} else {
//			if (el.text().length !== 0) {
//				$('<option />', {
//					'value': el.attr('href'),
//					'text': el.text()
//				}).appendTo('nav select');	
//			}
//		}
//		*/
//	});
//	
//	/*
//	 * If any item from the menu is selected, direct the user's
//	 * browser to the requested page
//	 */
//	$('nav select').on('change', function() {
//		window.location = $(this).find('option:selected').val();
//	});
//	
//	/*
//	 * ~ Set the initial width of the header and navigation menu
//	 * ~ Attach an event listener, so that the width also changes
//	 *   as the user resizes the browser or for example: the user
//	 *   has changed the orientation from 'portrait' to 'landscape'
//	 */
//	$('nav select').css('width', $(this).width());
//	$('.site-title').css('width', $(this).width());
//	$(window).on('resize', function(e) {
//		$('nav select').css('width', $(this).width());
//		$('.site-title').css('width', $(this).width());
//	});
//	
//	/*
//	 * Set the selected menu as the 'selected' item
//	 * in the menu
//	 */
//	var pathname = window.location.pathname;
//	$('nav select option').each(function() {
//		var value = $(this).attr('value');
//		
//		if (value === pathname) {
//			$(this).attr('selected', 'selected');
//		}
//	});
	
	// -------------- Mobile navigation ------------------ //
    
    $('#project_identity').on('change',function(){
        $.session.set('project_id',$(this).val());
        if($(this).val()!=""){
            $.get('UpdateDefaultProjectForUser',{
                'user_id': $.session.get('user_id'),
                'project_id': $(this).val()
            },function(data){
                if(data==true){
                    //window.location.reload(true);
                    console.log('changed');
                }
            });
        }
    });
    $('#default_team_identity').on('change',function(){
        $.session.set('default_team_identity',$(this).val());
        //$.session.set('default_team_name',$('#default_team_identity option:selected').text().trim());
        if($(this).val()!=""){
            $.get('UpdateDefaultTeamForUser',{
                'user_id': $.session.get('user_id'),
                'team_id': $(this).val()
            },function(data){
                if(data==true){
                    //window.location.reload(true);
                    console.log('changed');
                }
            });
        }
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
