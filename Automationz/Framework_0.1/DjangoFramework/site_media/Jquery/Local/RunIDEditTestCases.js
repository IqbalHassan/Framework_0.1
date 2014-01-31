/**
 * Created by lent400 on 1/15/14.
 */
/*$(document).ready(function(){
    DataFetch();
    $('.flip[title="TestStepName"]').live('click',function(){
        $('#TestStepDetail').slideToggle("slow");
    });
    $("p.flip[title =  'TestStepChange']").each(function(){
        $(this).css("display","inline-block")
    });
    $('#changeStatus').live('click',function(){
        $('#change_div').html("");
        $(this).css({'display':'none'});
        $('#passAll').css({'display':'none'});
        $('#failReason').css({'display':'none'});
        var message="";
        var count=0;
        $('#RunIDTestCaseData tr td:first-child').each(function(){
            count++;
            message+='<option value="'+count+'">'+$(this).text().trim()+'</option>'
        });
        $('#change_div').html('<table>' +
            '<tr>' +
            '   <td>' +
            '       <span><b>Test Step Name:</b></span>' +
            '       <select id="test_step_list">' +
            '           <option value="0">Select a Step</option> ' +
            '       </select>' +
            '   </td>' +
            '   <td>' +
            '       <table>' +
            '           <tr>' +
            '               <td>' +
            '                   <span id="status_label" style="display: none"><b>Status:</b></span>' +
            '               </td>' +
            '               <td>' +
            '                   <select id="status" name="status" style="display: none"></select>' +
            '               </td>' +
            '           </tr>' +
            '       </table>' +
            '   </td>' +
            '</tr>' +
            '<tr>' +
            '   <td colspan="2" align="center">' +
            '       <input type="submit" name="submit_button" id="submit_button" value="Submit" style="display: none"/> ' +
            '   </td>' +
            '</tr>' +
            '</table>' +
            //'<input name="runid" style="display: none" value="'+runid+'"/>' +
            //'<input name="testcaseid" style="display: none" value="'+testcaseid+'"/>' +
            '<input name="step_name" id="step_name" value="" style="display: none"/>');
        $('#test_step_list').append(message);
        $('#test_step_list').live('change',function(){
            //console.log($('#teststeplist option:selected').val());
            if($('#test_step_list option:selected').val()!=0){
                var statusMessage="";
                var lineNumber=$('#test_step_list option:selected').val();
                lineNumber++;
                var linestatus=$('#RunIDTestCaseData tr:nth-child('+lineNumber+') td:nth-child(2)').text().trim();
                var linename=$('#RunIDTestCaseData tr:nth-child('+lineNumber+') td:nth-child(1)').text().trim();
                $('#step_name').val(linename);
                //console.log(linestatus+'-'+linename);
                var statusArray=['Pass','Failed','Critical','Skipped','null'];
                for(var i=0;i<statusArray.length;i++){
                    if(statusArray[i]==linestatus){
                        statusMessage+='<option selected>'+statusArray[i]+'</option>';
                    }
                    else{
                        statusMessage+='<option>'+statusArray[i]+'</option>';
                    }

                }
                $('#status').html(statusMessage);
                $('#status_label').css({'display':'block'});
                $('#status').css({'display':'block'});
                $('#submit_button').css({'display':'block'});
            }
        })
    })
    $('#submit_button').live('click',function(){
        updateStatus();
    });
    $('#passAll').live('click',function(){
        var run_id=$('#runid').text().trim();
        var test_case_id=$('#testcaseid').text().trim();
        var test_step_name='all';
        var test_step_status="Pass";
        /*console.log(run_id);
         console.log(test_case_id);
         console.log(test_step_name);
         console.log(test_step_status);
        $.get("Edit/",{
            'run_id':run_id,
            'test_case_id':test_case_id,
            'test_step_name':test_step_name,
            'test_step_status':test_step_status
        },function(data){
            console.log(data);
            if(data=="true"){
                var message='/Home/RunID/'+run_id+'/TC/'+test_case_id+'/'
                window.location=message;
            }
        });
    });
    $('#failReason').live('click',function(){
        $('#change_div').html("");
        $(this).css({'display':'none'});
        $('#passAll').css({'display':'none'});
        $('#changeStatus').css({'display':'none'});
        var run_id=$('#runid').text().trim();
        var test_case_id=$('#testcaseid').text().trim();
        $('#change_div').html('<table>' +
            '<tr>' +
            '   <td>' +
            '       <span><b>Previous Fail Reason:</b></span>' +
            '   </td>' +
            '   <td>' +
            '       <input type="text" value="" id="old_reason" size="135" readonly="readonly"/>' +
            '   </td>' +
            '</tr>' +
            '<tr>' +
            '   <td>' +
            '       <span><b>Modify Reason:</b></span>' +
            '   </td>' +
            '   <td>' +
            '       <input type="text" value="" id="new_reason" size="135"/>' +
            '   </td>' +
            '</tr>' +
            '<tr>' +
            '   <td>' +
            '       &nbsp;' +
            '   </td>' +
            '   <td>' +
            '       <input type="button" value="Cancel" id="cancel_button"/>       ' +
            '       <input type="button" value="Change" id="change_button"/>' +
            '   </td>' +
            '</tr>' +
            '</table>');
        $.get("RunIDFailReason",{
            'run_id':run_id,
            'test_case_id':test_case_id
        },function(data){
            console.log(data);
            $('#old_reason').val(data);
        });
    });
    $('#cancel_button').live('click',function(){
        var run_id=$('#runid').text().trim();
        var test_case_id=$('#testcaseid').text().trim();
        var location='/Home/RunID/'+run_id+'/TC/'+test_case_id+'/';
        window.location=location;
    });
    $('#change_button').live('click',function(){
        var run_id=$('#runid').text().trim();
        var test_case_id=$('#testcaseid').text().trim();
        var reason=$('#new_reason').val().trim();
        $.get("UpdateFailReason",{
            'run_id':run_id,
            'test_case_id':test_case_id,
            'reason':reason
        },function(data){
            console.log(data);
            if(data=="true"){
                var location='/Home/RunID/'+run_id;
                window.location=location;
            }
        });
    });
    x
});
function updateStatus(){
    var run_id=$('#runid').text().trim();
    var test_case_id=$('#testcaseid').text().trim();
    var test_step_name=$('#step_name').val().trim();
    var test_step_status=$('#status option:selected').text().trim();
    /*console.log(run_id);
     console.log(test_case_id);
     console.log(test_step_name);
     console.log(test_step_status);
    $.get("Edit/",{
        'run_id':run_id,
        'test_case_id':test_case_id,
        'test_step_name':test_step_name,
        'test_step_status':test_step_status
    },function(data){
        console.log(data);
        if(data=="true"){
            var message='/Home/RunID/'+run_id+'/TC/'+test_case_id+'/'
            window.location=message;
        }
    });
}
function DataFetch(){
    var RunID=$('#runid').text().trim();
    var TestCaseID=$('#testcaseid').text().trim();
    var TestCaseName=$('#testcasename').text().trim();
    $.get("TestCase_Detail_Table",{RunID : RunID,TestCaseName : TestCaseID},function(data){
        ResultTable('#RunIDTestCaseData',data['TestCase_Detail_Col'],data['TestCase_Detail_Data'],"");
        $('#RunIDTestCaseData tr td:first-child').css({
            'color':'blue',
            'cursor':'pointer'
        });
        $('#RunIDTestCaseData tr td:first-child').live('click',function(){
            $('#TestStepDetail').html("" +
                "<div id='' title='Execution Log'>" +
                    "<p class='flip' name='execution_log' style='display: block'>Execution Log</p>" +
                    "<div id='TestStep_ExecutionLog'>" +
                    "</div>" +
                "</div>" +
                "<div id='' title='Step Data and Info'>" +
                    "<p class='flip' name='General_Description' style='display: block'>General Description</p>" +
                    "<div id='TestStep_InfoData'>" +
                    "</div>"+
                "</div>" +
                "<div id=''>" +
                    "<p class='flip' name='Data' style='display: block'>Data</p>" +
                    "<div id='Data' align='center'>" +
                    "</div>" +
                "</div>"
            );
            var RunID = $('#runid').text();
            var TestStepName = $(this).text();
            var TestStepSeqID = ($(this).parent().parent().children().index($(this).parent()));
            $.get("TestStep_Detail_Table/", {
                RunID : RunID,
                TestCaseName : TestCaseName,
                TestStepName : TestStepName,
                TestStepSeqID : TestStepSeqID
            },function(data){
                ResultTable('#TestStep_ExecutionLog',data['TestStep_Col'],data['TestStep_Details'],"");
                ResultTable('#TestStep_InfoData',data['TestStep_Description_Col'],data['TestStep_Description'],"");
                if(data['data_required']=="no"){
                    $("#Data").html("");
                    $("#Data").html("<b>Data is not required for this step</b>")
                }
                if(data['data_required']=="yes"){
                    //console.log(data['data_val_comp']);
                    $("#Data").html("");
                    ResultTable('#Data',data['data_col'],data['data_val'], "");
                    for(var i=0;i<data['data_val'].length;i++){
                        var col= "row"+(i+2)+"col"+(i+2);
                        $('#Data tr:nth-child('+(i+2)+')>td:nth-child(2)').attr({'id':col});
                    }
                    var dataset=data['data_val_comp'];
                    for(var i=0;i<dataset.length;i++){
                        var col= "#row"+(i+2)+"col"+(i+2);
                        ResultTable(col,["Field","Value"],dataset[i],"");
                    }
                }
            });
            $('#stepname').html('<b>Details for </b>'+TestStepName);
            $('#stepname').css({'display':'block'});
            $('#TestStepDetail').slideDown("slow");
        });
        $('.flip[name="execution_log"]').live('click',function(){
            $('#TestStep_ExecutionLog').slideToggle("slow");
        })
        $('.flip[name="General_Description"]').live('click',function(){
            $('#TestStep_InfoData').slideToggle("slow");
        })
        $('.flip[name="Data"]').live('click',function(){
            $('#Data').slideToggle("slow");
        })

    });
}*/

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
            step_status:"Pass",
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
    $('#data_table tr td:nth-child(3)').each(function(){
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
        $('#RunIDTestCaseData').html(message);
        TestDataFetch();
        MakeStatusSelectable();
        InputFailReason();
        ExecutionLog();
    });
}
function ExecutionLog(){
    $('#data_table tr td:nth-child(7)').each(function(){
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
    $('#data_table tr td:nth-child(5)').each(function(){
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
    $('#data_table tr td:nth-child(6)').each(function(){
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
                /*'<option value="Blocked">Blocked</option>' +*/
                '<option value="Skipped">Skipped</option>' +
                //'<option value="Warning">Warning</option>' +
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
        message+=('<td class="ui-widget-header">'+column[i]+'</td> ')
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