/**
 * Created by J on 9/11/14.
 */
$(document).ready(function(){

    $("#simple-menu").sidr({
        name: 'sidr',
        side: 'left'
    });

    $.get("GetMileStones",{term : ''},function(data)
    {
        if(data['TableData'].length>0) {
            //make a table column
            var message = "";
            message += '<table class="one-column-emphasis">';
            message += '<tr>';
            for (var i = 0; i < data['Heading'].length; i++) {
                message += '<th align="left">' + data['Heading'][i] + '</th>';
            }
            message += '</tr>';
            for (var i = 0; i < data['TableData'].length; i++) {
                //msid.push(data['TableData'][i][0]);
                message += '<tr>';
                for (var j = 0; j < data['TableData'][i].length; j++) {
                    message += '<td align="left">' + data['TableData'][i][j] + '</td>';
                }
                message += '</tr>';
            }
            message += '</table>';
            $('#allMilestones').html(message);
            make_clickable('#allMilestones');

        }
    });


});


function make_clickable(divname) {
    $(divname + ' tr>td:first-child').each(function () {
        $(this).css({
            'color': 'blue',
            'cursor': 'pointer',
            'textAlign': 'left'
        });
        $(this).click(function(){
            $.get("GetMileStoneID",{term : $(this).text().trim()},function(data)
            {
                var location='/Home/EditMilestone/'+data+'/';
                window.location=location;
            });
        });
    });
}