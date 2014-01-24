/**
 * Created by lent400 on 1/22/14.
 */
$(document).ready(function(){
    $('.flip[title="RunIDHeader"]').text("Show All");
    var searchText="limit";
    show_Results(searchText);
    $('.flip[title="RunIDHeader"]').live('click',function(){
        show_Results("all");
    });
});
function Make_RunID_Click(){
    $('#ResultPane tr td:first-child').each(function(){
       if($(this).text().trim()!='Run ID'){
           $(this).css({
               'color':'blue',
               'cursor':'pointer'
           })
           $(this).click(function(){
               var runid=$(this).closest("tr").find("td:first-child").text().trim();
               window.location='/Home/RunID/'+runid+'/';
           });
       }

    });

}
function drawTable(column,row){
    var message="";
    message+='<table id="data_table" class="ui-widget" style="font-size:small; border-collapse:collapse;" width="100%">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<td class="ui-widget-header">'+column[i]+'</td> ';
    }
    message+='</tr>';
    for(var i=0;i<row.length;i++){
        message+='<tr>';
        for(var j=0;j<row[i].length;j++){
            if(row[i][j]=="status"){
                message+='<td class="ui-widget-content" id="status'+i+'"></td>'
            }
            else{
                message+='<td class="ui-widget-content">'+row[i][j]+'</td> ';
            }
        }
    }
    message+='</tr>';
    message+='</table>';
    return message;
}
function show_Results(searchText){
    $.get("ResultTableFetch",{
        'searchText':searchText
    },function(data){
        var message=drawTable(data['column'],data['data']);
        //console.log(message);
        $('#ResultPane').html(message);
        for(var i=0;i<data['status_list'].length;i++){
            var array=data['status_list'][i];
            var message="";
            pass=(array[1]/array[0])*100;
            fail=(array[2]/array[0])*100;
            progress=(array[3]/array[0])*100;
            skip=(array[4]/array[0])*100;
            pending=(array[5]/array[0])*100;
            console.log(pass);
            console.log(fail);
            console.log(progress);
            console.log(skip);
            message+='<table style="border-collapse:collapse" width="100%" height="100%"><tr width="100%" height="100%">';
            if(pass!=0){
                message+='<td style="background-color: green;" width="'+pass+'%">&nbsp;</td>';
            }
            if(fail!=0){
                message+='<td style="background-color: red;" width="'+fail+'%">&nbsp;</td>';
            }
            if(progress!=0){
                message+='<td style="background-color: blue;" width="'+progress+'%">&nbsp;</td>';
            }
            if(skip!=0){
                message+='<td style="background-color: silver;" width="'+skip+'%">&nbsp;</td>';
            }
            if(pending!=0){
                message+='<td style="background-color: yellow;" width="'+pending+'%">&nbsp;</td>';
            }
            message+='</tr></table>';
            $('#status'+i).html(message);
        }
        Make_RunID_Click();
//        Make_Status_Bar();
    });
}
