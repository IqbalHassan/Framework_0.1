/**
 * Created by lent400 on 1/22/14.
 */
$(document).ready(function(){
    $('.flip[title="SeeLess"]').css({'display':'none'});
    $('.flip[title="RunIDHeader"]').text("Show All");
    var searchText="limit";
    show_Results(searchText);
    $('.flip[title="RunIDHeader"]').live('click',function(){
        show_Results("all");
        $(this).css({'display':'none'});
        $('.flip[title="SeeLess"]').css({'display':'block'});
    });
    $('.flip[title="SeeLess"]').live('click',function(){
        show_Results("limit");
        $(this).css({'display':'none'});
        $('.flip[title="RunIDHeader"]').css({'display':'block'});
    });
});
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
                message+='<td class="ui-widget-content status-table" id="status'+i+'"></td>'
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
function Clickable_RunID(){
    $('#ResultPane tr>td:first-child').each(function(){
       if($(this).text().trim()!="Run ID"){
           $(this).css({
               'color':'blue',
               'cursor':'pointer'
           });
           $(this).live('click',function(){
              var run_id=$(this).text().trim();
              if(run_id!=""){
                  window.location='/Home/RunID/'+run_id+'/';
              }

           });
       }
    });
}
function make_table(array){
    console.log(array);
    var message="";
    var column=["Legend","Status","No of Cases","Percentage"];
    var tag=["Passed","Failed","In-Progress","Skipped","Pending"];
    var color=["green","red","blue","silver","yellow"];
    message+='<table class="ui-widget" style="font-size: small;border-collapse: collapse">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<td class="ui-widget-header" style="text-align: center">'+column[i]+'</td>';
    }
    message+='</tr>';
    for(var i=0;i<color.length;i++){
        var percentage=(array[i+1]/array[0])*100;
        if(percentage!=0){
            percentage=percentage-0.01;
        }
        percentage=percentage+"%";
        console.log(percentage);
        message+='<tr>';
        message+='<td width="40%" class="ui-widget-content"><table width="100%" height="100%"><tr><td style="background-color: '+color[i]+'">&nbsp;&nbsp;</td></tr></table></td>';
        message+='<td width="30%" class="ui-widget-content" style="text-align:center;color:'+color[i]+'"><b>'+tag[i]+'</b></td>';
        message+='<td class="ui-widget-content"  style="text-align: center;font-weight:bolder;color:'+color[i]+'" width="100%">'+array[i+1]+'</td>';
        message+='<td class="ui-widget-content" style="text-align: center;font-weight:bolder;color:'+color[i]+'" width="100%">'+percentage+'</td>';
        message+='</tr>'
    }
    message+='<tr>';
    message+='<td class="ui-widget-content" style="text-align: center"><b>Total</b></td> ';
    message+='<td class="ui-widget-content" style="text-align: center" colspan="3"><b>'+array[0]+'</b></td> ';
    message+='</tr>'
    message+='</table> ';
    /*message_inner=""
    message_inner+='<br><br><br><br><br><br><div id="inner-right" align="right"><table class="ui-widget" style="font-size: small;border-collapse: collapse;">';
    message_inner+='<tr><th class="ui-widget-header" colspan="2">Legend Information</th></tr>'
    for(var i=0;i<color.length;i++){
        message_inner+='<tr>';
        message_inner+='<td class="ui-widget-content" width="50%"><table width="100%" height="100%"><tr><td style="background-color: '+color[i]+'">&nbsp;&nbsp;</td></tr></table></td>';
        message_inner+='<td class="ui-widget-content" width="50%" style="text-align: center">'+tag[i]+'</td>';
        message_inner+='</tr>';
    }
    message_inner+='</table></div>';
    message+=message_inner;*/
    return message;
}
function Make_Detail_Status(){
    $('#ResultPane tr td:nth-child(3)').each(function(){
        if($(this).text().trim()!="Report Status"){
            $(this).css({
                'cursor':'pointer'
            }) ;
            $(this).live('click',function(){
                var run_id=$(this).closest("tr").find("td:first-child").text().trim();
                var data_got=0;
                var message="";
                $.get("RunIDStatus",{
                    'run_id':run_id
                },function(data){
                    data_got=data['message'];
                    console.log(data_got);
                    message=make_table(data_got);
                    $('#inner').html(message);
                    $("#inner").dialog({
                        buttons : {
                            "OK" : function() {
                                $(this).dialog("close");
                            }
                        },
                        show : {
                            effect : 'drop',
                            direction : "up"
                        },
                        modal : true,
                        width : 500,
                        height : 620,
                        title:"Result Summary"
                    });
                });

            });
        }
    });
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
            $('#status'+i).html(message+'Total:'+array[0]);
        }
        Make_Detail_Status();
        Clickable_RunID();
    });
}
