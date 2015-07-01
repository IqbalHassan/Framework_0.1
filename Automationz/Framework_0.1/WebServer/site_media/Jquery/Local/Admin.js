/**
 * Created by minar09 on 2/15/14.
 */

$(document).ready(function(){

    $("#git_pull").click(function(){
        var command = 'Pull';
        if(command != 0)
        {
            $.ajax({
                url:'Process_Git/',
                dataType : "json",
                data : {
                    command : command
                },
                success: function( json ) {
                    $("#error").html("<p><b> Git  '"+command+"'</b></p>");
                    alertify.log("Git pulled.","",0);
                },
                error: function(){
                    alertify.set({ delay: 300000 });
                    alertify.error("Service Unavailable!");
                }
            });
        }
    });

    $("#git_log").click(function(){
        var command = 'Log';
        if(command != 0)
        {
            $.get('Process_Git',{command:command},function(json){
                alertify.log(json,"",0);
                    //$("#error").html("<p><b> Git  '"+command+"'</b></p>");
                    /*if(json==""){
                        $('#error_git').html('<b style="color:red;">'+json+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                        $('#error_git').slideDown('slow');
                        setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    }
                    else{
                        $('#error_git').html('<b style="color:green;">'+json+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                        $('#error_git').slideDown('slow');
                        setTimeout(function(){window.location='/Home/RunTest/';},4000);
                    }*/

            });
        }
    });

});
