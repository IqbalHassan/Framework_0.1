/**
 * Created by J on 2/2/2015.
 */

var itemPerPage=10;
var PageCurrent=1;

$(document).ready(function(){
	$("#simple-menu").sidr({
        name: 'sidr',
        side: 'left'
    });

    itemPerPage = $("#perpageitem").val();
    get_steps(itemPerPage, PageCurrent);
    
    $('#perpageitem').on('change',function(){
        if($(this).val()!=''){
            itemPerPage=$(this).val();
            current_page=1;
            $('#pagination_tab').pagination('destroy');
            window.location.hash = "#1";
            get_steps(itemPerPage, PageCurrent);
        }
    });

});


function get_steps(itemPerPage,PageCurrent){
    $.get("Steps_List",{'itemPerPage':itemPerPage ,'PageCurrent':PageCurrent},function(data)
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
            $('#pagination_tab').pagination({
                items:data['count'],
                itemsOnPage:itemPerPage,
                cssStyle: 'dark-theme',
                currentPage:PageCurrent,
                displayedPages:2,
                edges:2,
                hrefTextPrefix:'#',
                onPageClick:function(PageNumber){
                    //PerformSearch(project_id,team_id,user_text,itemPerPage,PageNumber);
                    get_steps(itemPerPage,PageNumber);
                }
            });


        }
        else{
            $("#allsteps").html('<h2>No Steps Available</h2>')
        }

        //$('#allsteps').html(message);
        
    });
}