/**
 * Created by lent400 on 1/15/14.
 */
$(document).ready(function(){
    DataFetch();
    $('.flip[title="TestStepName"]').live('click',function(){
        $('#TestStepDetail').slideToggle("slow");
    });
    $("p.flip[title =  'TestStepChange']").each(function(){
        $(this).css("display","inline-block")
    });
    $('#changeStatus').live('click',function(){
        $(this).css({'display':'none'});
        $('#passAll').css({'display':'none'});
        var message="";
        var count=0;
        $('#RunIDTestCaseData tr td:first-child').each(function(){
            count++;
            message+='<option value="'+count+'">'+$(this).text().trim()+'</option>'
        });
        var runid=$("#runid").text().trim();
        var testcaseid=$('#testcaseid').text().trim();
        $('#change_div').html('' +
            '<input name="runid" style="display: none" value="'+runid+'"/>' +
            '<input name="testcaseid" style="display: none"value="'+testcaseid+'"/>' +
            '<span><b>TestStepName:</b></span>' +
            '<select id="teststeplist">' +
            '   <option value="0">Select a step</option>' +
            '</select>' +
            '<span id="statusspan" style="display: none;"><b>Status:</b></span>' +
            '<select id="status" name="status" style="display: none"></select>' +
            '<input type="submit" name="submit_button" id="submit_button" style="display: none" value="Submit"> '

        );
        $('#teststeplist').append(message);
        $('#teststeplist').live('change',function(){
            //console.log($('#teststeplist option:selected').val());
            if($('#teststeplist option:selected').val()!=0){
                var statusMessage="";
                var lineNumber=$('#teststeplist option:selected').val();
                lineNumber++;
                var linestatus=$('#RunIDTestCaseData tr:nth-child('+lineNumber+') td:nth-child(2)').text().trim();
                var linename=$('#RunIDTestCaseData tr:nth-child('+lineNumber+') td:nth-child(1)').text().trim();
                $("#change_div").append('<input name="stepname" style="display: none" value="'+linename+'"/>')
                console.log(linestatus+'-'+linename);
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
                $('#statusspan').css({'display':'block'});
                $('#status').css({'display':'block'});
                $('#submit_button').css({'display':'block'});
            }
        })
    })
});
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
}