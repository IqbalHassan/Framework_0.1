/**
 * Created by minar09 on 2/15/14.
 */

$(document).ready(function(){

    $("#git_pull").click(function(){
        var command = 'Pull';
        if(command != 0)
        {
            $.get("Process_Git",{command : command},function(data)
            {
                //ResultTable(git_result, data['Heading'],data['TableData'],"Git Pull");

            });
        }
    });

    $("#git_log").click(function(){
        var command = 'Log';
        if(command != 0)
        {
            $.get("Process_Git",{command : command},function(data)
            {
                //ResultTable(git_result, data['Heading'],data['TableData'],"Git Pull");

            });
        }
    });

});
