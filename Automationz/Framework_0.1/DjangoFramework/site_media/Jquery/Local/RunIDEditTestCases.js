/**
 * Created by lent400 on 1/15/14.
 */

var test_case_name=$('#testcasename').text().trim();
$(document).ready(function(){
    DataFetch();
    $('#changeStatus').live('click',function(event){
        var run_id=$('#runid').text().trim();
        var test_case_id=$('#testcaseid').text().trim();
        var step_name=[];
        $('#data_table tr td:nth-child(2)').each(function(){
            var step=$(this).text().trim();
            console.log(step);
            step_name.push(step);
        });
        step_name.shift();
        var step_status=[];
        $('#data_table tr td:nth-child(6)').each(function(){
            var step_no=$(this).closest("tr").find("td:first-child").text().trim();
            var tc_id=$('#testcaseid').text().trim();
            var step_id=tc_id+"_s"+step_no+"_status";
            step_id=step_id.trim();
            var status=$('#'+step_id+' option:selected').text().trim();
            step_status.push(status);
        });
        step_status.shift();
        var step_reason=[];
        $('#data_table tr td:nth-child(5)').each(function(){
            var step_no=$(this).closest("tr").find("td:first-child").text().trim();
            var tc_id=$('#testcaseid').text().trim();
            var step_id=tc_id+"_s"+step_no+"_reason";
            var reason=$('#'+step_id).val();
            step_reason.push(reason);
        });
        step_reason.shift();
        console.log(step_name);
        console.log(step_status);
        console.log(step_reason);
        console.log(run_id);
        console.log(test_case_id);
        $.get("UpdateData",{
            step_name:step_name.join('|'),
            step_status:step_status.join('|'),
            step_reason:step_reason.join('|'),
            run_id:run_id,
            test_case_id:test_case_id
        },function(data){
            if(data=="true"){
                window.location="/Home/RunID/"+run_id+"/TC/"+test_case_id+"/";
            }
        });
        event.stopPropagation();
    });
    $('#passAll').live('click',function(event){
        var run_id=$('#runid').text().trim();
        var test_case_id=$('#testcaseid').text().trim();
        var step_name=[];
        $('#data_table tr td:nth-child(2)').each(function(){
            var step=$(this).text().trim();
            console.log(step);
            step_name.push(step);
        });
        step_name.shift();
        var step_reason=[];
        $('#data_table tr td:nth-child(5)').each(function(){
            var step_no=$(this).closest("tr").find("td:first-child").text().trim();
            var tc_id=$('#testcaseid').text().trim();
            var step_id=tc_id+"_s"+step_no+"_reason";
            var reason=$('#'+step_id).val();
            step_reason.push(reason);
        });
        step_reason.shift();
        $.get("UpdateData",{
            step_name:step_name.join('|'),
            step_status:"Passed",
            step_reason:step_reason.join('|'),
            run_id:run_id,
            test_case_id:test_case_id
        },function(data){
            //console.log(data);
            if(data=="true"){
                window.location="/Home/RunID/"+run_id+"/TC/"+test_case_id+"/";
            }
        });
        event.stopPropagation();
    });
    $('.flip[title="BackPage"]').live('click',function(){
        var runid=$('#runid').text().trim();
        window.location='/Home/RunID/'+runid+'/';
    });
});
function TestDataFetch(){
    $('#data_table tr td:nth-child(4)').each(function(){
        $(this).css({'textAlign':'center'});
        var value=$(this).text().trim();
        console.log(value);
        if(value!="DataRequired"){
            if(value=="false"){
                $(this).html("");
            }
            else{
                $(this).html("see data");
                $(this).css({
                    'color':'blue',
                    'cursor':'pointer'
                });
            }
        }
        $(this).live('click',function(){
            var data_required=$(this).text().trim();
            if(data_required=="see data"){
                var tc_id=$('#testcaseid').text().trim();
                var step_no=$(this).closest("tr").find("td:first-child").text().trim();
                var step_name=$(this).closest("tr").find("td:nth-child(2)").text().trim();
                var datasetid=tc_id+"_s"+step_no;
                $.get("TestDataFetch",{
                    'data_set_id':datasetid.trim()
                },function(data){
                    console.log(data['row_array']);
                    console.log(data['data_array']);
                    var column=["DataSet","Data"];
                    var message=draw_table(data['row_array'],column);
                    $('#inside_back').html("");
                    var div_name=step_name+"(Data Details)";
                    $('#inside_back').append(message);
                    $('#data_detail tr td:nth-child(2)').each(function(){
                        if($(this).text().trim()!="Data"){
                            var data_column=["Field","Value"];
                            var data_detail=data['data_array'];
                            var message=draw_table(data_detail[0],data_column);
                            $(this).html(message);
                            data['data_array'].shift();
                        }
                    });
                    $("#inside_back").dialog({
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
                        title:div_name

                    });
                });
            }
        });
    });
}

function draw_table(row,column){
    var message=""
    message+='<table id="data_detail" class="ui-widget" style="font-size:small; border-collapse:collapse;" width="100%">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<td class="ui-widget-header">'+column[i]+'</td>';
    }
    message+='</tr>';
    for(var i=0;i<row.length;i++){
        message+='<tr>';
        for(var j=0;j<row[i].length;j++){
            message+='<td class="ui-widget-content">'+row[i][j]+'</td>';
        }
        message+='</tr>';
    }
    message+='</table>';
    return message;
}
function DataFetch(){
    var run_id=$('#runid').text().trim();
    var test_case_id=$('#testcaseid').text().trim();
    console.log(run_id);
    console.log(test_case_id);
    $.get("DataFetchForTestCases/",{
        'run_id':run_id,
        'test_case_id':test_case_id
    },function(data){
        /*console.log(data['data_collected']);
        console.log(data['data_column']);*/
        var datatable=data['data_collected'];
        var datacolumn=data['data_column'];
        var message=table_message(datacolumn,datatable);
        //console.log(message);
        $('#testcasestatus').html(data['test_case_status']);
        $('#RunIDTestCaseData').html(message);
        TestDataFetch();
        MakeStatusSelectable();
        InputFailReason();
        ExecutionLog();
    });
}
function ExecutionLog(){
    $('#data_table tr td:nth-child(9)').each(function(){
       $(this).closest("tr").find("td:first-child").css({'textAlign':'center'});
       $(this).closest("tr").find("td:nth-child(3)").css({'textAlign':'center'});
       if($(this).text().trim()=="Log"){
           $(this).html("see log");
           $(this).css({
               'color':'blue',
               'cursor':'pointer',
               'text-align':'center'
           });
       }
       $(this).live('click',function(e){
           var run_id=$('#runid').text().trim();
           var test_case_id=$('#testcaseid').text().trim();
           var step_no=$(this).closest("tr").find("td:first-child").text().trim();
           var step_name=$(this).closest("tr").find("td:nth-child(2)").text().trim();
           var div_name=step_name+"(Execution Log)";
           console.log(div_name+"-"+step_name);
           $('#inside_back').html("");
           $.get("LogFetch",{
                run_id:run_id,
                test_case_id:test_case_id,
                step_name:step_name
           },function(data){
               ResultTable("#inside_back",data['column'],data['log'],"");
               $("#inside_back").dialog({
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
                   title:div_name

               });
           });
           e.stopPropagation();
       });
    });
}
function InputFailReason(){
    $('#data_table tr td:nth-child(7)').each(function(){
        $(this).css({'textAlign':'center'});
        var failreason=$(this).text().trim();
        var step_no=$(this).closest("tr").find("td:first-child").text().trim();
        var tc_id=$('#testcaseid').text().trim();
        var step_id=tc_id+"_s"+step_no+"_reason";
        step_id=step_id.trim();
       if($(this).text().trim()!="FailReason"){
           $(this).html('<textarea id="'+step_id+'" column="100" style="align:center"/></textarea>');
           $('#'+step_id).val(failreason);
       }
    });
}
function MakeStatusSelectable(){
    $('#data_table tr td:nth-child(8)').each(function(){
        $(this).css({'textAlign':'center'});
        var value=$(this).text().trim();
        var step_no=$(this).closest("tr").find("td:first-child").text().trim();
        var tc_id=$('#testcaseid').text().trim();
        var step_id=tc_id+"_s"+step_no+"_status";
        step_id=step_id.trim();
        console.log(value);
        if(value!="Status"){
            $(this).html('<select id="'+step_id+'" style="align:center">' +
                '<option value="Passed">Passed</option>' +
                '<option value="Failed">Failed</option>' +
                '<option value="Skipped">Skipped</option>' +
                '<option value="Submitted">Submitted</option>' +
                '<option value="In-Progress">In-Progress</option>' +
                '</select>'
            );
            $('#'+step_id+' option[value='+value+']').attr({'selected':'selected'});
        }

    });
}
function table_message(column,tabledata){
    var message="";
    message+='<table id="data_table" class="ui-widget" style="font-size:small; border-collapse:collapse;" width="100%">';
    var header_message=header_print(column);
    message+=header_message;
    var data_message=data_print(tabledata);
    message+=data_message;
    message+='</table>';
    return message;
}

function header_print(column){
    var message="";
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+=('<td class="ui-widget-header" style="text-align: center">'+column[i]+'</td> ')
    }
    message+='</tr>';
    return message;
}
function data_print(data){
    var message="";
    for(var i=0;i<data.length;i++){
        message+='<tr>';
        for(var j=0;j<data[i].length;j++){
            var value=data[i][j];
            if(value==null){
                value="&nbsp;";
            }
            message+=('<td class="ui-widget-content">'+value+'</td>')
        }
        message+='</tr>';
    }
    return message;
}