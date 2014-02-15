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
                }
            });
        }
    });

    $("#git_log").click(function(){
        var command = 'Log';
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
                }
            });
        }
    });

});
