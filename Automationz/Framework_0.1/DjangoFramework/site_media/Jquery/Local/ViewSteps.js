/**
 * Created by J on 2/2/2015.
 */

$(document).ready(function(){
	$("#simple-menu").sidr({
        name: 'sidr',
        side: 'left'
    });

    $.get("Steps_List",{term : ''},function(data)
    {
        if(data['steps'].length>0) {
            //make a table column
            var message = "";
            message += '<table class="one-column-emphasis">';
            message += '<tr>';
            for (var i = 0; i < data['Heading'].length; i++) {
                message += '<th align="left">' + data['Heading'][i] + '</th>';
            }
            message += '</tr>';
            for (var i = 0; i < data['steps'].length; i++) {
                message += '<tr>';
                for (var j = 0; j < data['steps'][i].length; j++) {
                    message += '<td align="left">' + data['steps'][i][j] + '</td>';


                }
                message += '</tr>';
            }
            message += '</table>';
            $('#allsteps').html(message);


        }
        else{
            $("#allsteps").html('<h2>No Steps Available</h2>')
        }
    });

});