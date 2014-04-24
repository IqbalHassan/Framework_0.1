/**
 * Created by minar09 on 3/15/14.
 */
$(document).ready(function(){
    //login
    $('#loginbtn').click(function(e) {
        var user = $('.username').val();
        var pwd = $('.password').val();
        var logged = false;
        var data = [];

        if (user=="" || pwd=="")
        {
            //alert("Fields are empty");
            alertify.error("Fields are empty");
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
                        alertify.success("Logged in as '"+json+"'");
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
                        alertify.error("'"+json+"'");
                    }
                },
                error: function(json){
                    alertify.error("Error");}
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

    $('#username , #password').keypress(function (e) {
        var key = e.which;
        if(key == 13)  // the enter key code
        {
            $("#loginbtn").trigger('click');
        }
    });


    if($.session.get('log')!='logged' && $(this).attr('title')!='Log In')
    {
        //$(".welcome").text("Hello Guest!");
        //$(".open").text("Log In");
        //$("#modaltrigger").show();
        //setTimeout(function(){window.location='/Home/Login/';},4000);
        window.location.href = '/Home/Login/';
        //$("#nav").hide();
    }
    $(".welcome").text($.session.get('fullname'));

    /*else
    {

        //$(".welcome").text(user);
        //$(".open").text("Log Out");
        //$("#modaltrigger").hide();
    }*/

    /*if($(".welcome").text()=="Hello Guest!" || $(".welcome").text()=="Hello undefined!")
    {
        $(".open").text("Log In");
        $("#nav").click(function(){
            location.reload();
        });
    }
    else
    {
        $(".open").text("Log Out");
    }*/

    /*if($(".open").text()=="Log In")
    {
        $('.open').leanModal({ top: 110, overlay: 0.45, closeButton: ".hidemodal" });
    }
    else if($(".open").text()=="Log Out")
    {
        $(".open").click(function(){
            $.session.remove('username');
            $.session.clear();
            location.reload();
        });
    }*/
    $(".logout").click(function(){
        $.session.remove('username');
        $.session.remove('fullname');
        $.session.remove('log');
        //$.session.clear();
        location.reload();
        //window.location.href = '/Home/Login/';
        $(".welcome").text("");
    });

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

    var button = document.getElementById('submit_button');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification(message);
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
                var n = new Notification(message);
            }

            // Otherwise, we can fallback to a regular modal alert
            else {
                alertify.log(message);
            }
        });
    }

    // If the user refuses to get notified
    else {
        // We can fallback to a regular modal alert
        alertify.log(message);
    }


}