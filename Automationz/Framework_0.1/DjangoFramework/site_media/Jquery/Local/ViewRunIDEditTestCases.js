/**
 * Created by lent400 on 1/15/14.
 */

var test_case_name=$('#testcasename').text().trim();
$(document).ready(function(){
    DataFetch();
    related_items();
    history();
    go_change();
});
function UIChange(){
    /*$('#data_table tr td:nth-child(5)').each(function(){
     $(this).css({
     'textAlign':'left'
     })
     });
     $('#data_table tr td:nth-child(6)').each(function(){
     $(this).css({
     'textAlign':'left'
     })
     });*/
    $('#data_table, .two-column-emphasis').each(function(){
        $(this).css({
            'textAlign':'left',
            'text-align':'left'
        })
    });
    $('#data_table tr td:nth-child(4)').each(function(){
        $(this).css({
            'textAlign':'center'
        })
    });
    $('#data_table tr td:nth-child(9)').each(function(){
        $(this).css({
            'textAlign':'center'
        })
        var value=$(this).text().trim();
        if(value=="false"){
            //$(this).html("");
            $(this).html("<a class=\"notification-indicator tooltipped downwards\" data-gotokey=\"n\"><span id=\"platform-flag\" class=\"mail-status\"></span></a>");
        }
        if(value=="true"){
            //$(this).html("see data");
            $(this).html("<a class=\"notification-indicator tooltipped downwards\" data-gotokey=\"n\"><span id=\"platform-flag\" class=\"mail-status filled\"></span></a>");
        }
    });
    $('#data_table tr td:nth-child(10)').each(function(){
        $(this).css({
            'textAlign':'center'
        })
        var value=$(this).text().trim();
        if(value=="false"){
            //$(this).html("");
            $(this).html("<a class=\"notification-indicator tooltipped downwards\" data-gotokey=\"n\"><span id=\"platform-flag\" class=\"mail-status\"></span></a>");
        }
        else if(value=="true"){
            //$(this).html("see data");
            $(this).html("<a class=\"notification-indicator tooltipped downwards\" data-gotokey=\"n\"><span id=\"platform-flag\" class=\"mail-status filled\"></span></a>");
        }
    });
    $('#data_table tr td:nth-child(11)').each(function(){
        /*$(this).css({
         'textAlign':'center'
         })*/
        var value=$(this).text().trim();
        $(this).html(convertToString(value));
    });
    $('#data_table tr td:nth-child(12)').each(function(){
        $(this).css({
            'textAlign':'center'
        })
        var value=$(this).text().trim();
        if(value=="false"){
            //$(this).html("");
            $(this).html("<a class=\"notification-indicator tooltipped downwards\" data-gotokey=\"n\"><span id=\"platform-flag\" class=\"mail-status\"></span></a>");
        }
        else if(value=="true"){
            //$(this).html("see data");
            $(this).html("<a class=\"notification-indicator tooltipped downwards\" data-gotokey=\"n\"><span id=\"platform-flag\" class=\"mail-status filled\"></span></a>");
        }
    });

}
function TestDataFetch(){
    $('#data_table tr td:nth-child(4)').each(function(){
        //$(this).css({'textAlign':'center'});
        var value=$(this).text().trim();
        console.log(value);
        if(value!="DataRequired"){
            if(value=="false"){
                //$(this).html("");
                $(this).html("<a class=\"notification-indicator tooltipped downwards\" data-gotokey=\"n\"><span id=\"platform-flag\" class=\"mail-status\"></span></a>");
            }
            else{
                //$(this).html("see data");
                $(this).html("<a class=\"notification-indicator tooltipped downwards\" data-gotokey=\"n\"><span id=\"platform-flag\" class=\"mail-status filled\"></span></a>");
                $(this).addClass("see_data");
                $(this).css({
                    'color':'blue',
                    'cursor':'pointer'
                });
            }
        }
        $(this).live('click',function(){
            //var data_required=$(this).text().trim();
            var data_required=$(this).hasClass("see_data");
            if(data_required==true){
                var tc_id=$('#testcaseid').text().trim();
                var step_no=$(this).closest("tr").find("td:first-child").text().trim();
                var step_name=$(this).closest("tr").find("td:nth-child(2)").text().trim();
                var datasetid=tc_id+"_s"+step_no;
                $.get("TestDataFetch",{
                    'run_id':$('#runid').text().trim(),
                    'tc_id':tc_id.trim(),
                    'step_sequence':step_no
                },function(data){
                    console.log(data);
                    var column=["DataSet","Data"];
                    var message=drawPopUp(data,column);
                    $('#inside_back').html("");
                    var div_name=step_name+"(Data Details)";
                    $('#inside_back').append(message);
                    /*console.log(data['row_array']);
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
                    $('#data_detail tr>td:first-child:eq(0)').each(function(){
                        //$(this).css({'textAlign':'center'});
                    })*/;

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

function drawPopUp(data,column){
    var message="";
    message+='<table id="data_detail" class="two-column-emphasis" width="100%">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<th>'+column[i]+'</th>';
    }
    message+='</tr>';
    var column_data=['field','subfield','value']
    for (var i=0;i<data.length;i++){
        for(var l=0;l<data[i].length;l++){
            message+='<tr>';
            var dataset=data[i][l][0];
            message+='<td>'+dataset+'</td>';
            var group_data=data[i][l][1];
            message+='<td>';
            message+='<table class="two-column-emphasis" width="100%">';
            message+='<tr>';
            for(var j=0;j<column_data.length;j++){
                message+='<th>'+column_data[j]+'</th>';
            }
            message+='</tr>';
            for(var j=0;j<group_data.length;j++){
                message+='<tr>';
                for(var k=0;k<group_data[j].length;k++){
                    message+='<td>'+group_data[j][k]+'</td>';
                }
                message+='</tr>';
            }
            message+='</table>';
            message+='</td>';
            message+='</tr>';
        }
    }
    message+='</table>';
    return message;
}
function draw_table(row,column){
    var message=""
    message+='<table id="data_detail" class="two-column-emphasis" width="100%">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<th>'+column[i]+'</th>';
    }
    message+='</tr>';
    for(var i=0;i<row.length;i++){
        message+='<tr>';
        for(var j=0;j<row[i].length;j++){
            message+='<td style="text-align: left">'+row[i][j]+'</td>';
        }
        message+='</tr>';
    }
    message+='</table>';
    return message;
}
colors = {
    'pass' : '#65bd10',
    'fail' : '#fd0006',
    'block' : '#ff9e00',
    'submitted' : '#808080',
    'in-progress':'#0000ff',
    'skipped':'#cccccc'
};

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
        $('#testcase').append(data['test_case_status']);

        var css = '';
        switch (data['test_case_status']) {
            case 'Passed':
                css = "4px solid " + colors['pass'];
                break;
            case 'Failed':
                css = "4px solid " + colors['fail'];
                break;
            case 'Blocked':
                css = "4px solid " + colors['block'];
                break;
            case 'In-Progress':
                css = "4px solid " + colors['in-progress'];
                break;
            case 'Submitted':
                css = "4px solid " + colors['submitted'];
                break;
            case 'Skipped':
                css = "4px solid " + colors['skipped'];
                break;
        }

        $("#breadcrumb_header").css("border-left", css);

        $('#RunIDTestCaseData').html(message);
        TestDataFetch();
        MakeStatusSelectable();
        InputFailReason();
        ExecutionLog();
        UIChange();
    })
}
function ExecutionLog(){
    $('#data_table tr td:nth-child(2)').each(function(){
        if($(this).text().trim()!='StepName'){
            $(this).css({
                'color':'blue',
                'cursor':'pointer',
                'text-align':'left'
            });
            $(this).live('click',function(e){
                var run_id=$('#runid').text().trim();
                var test_case_id=$('#testcaseid').text().trim();
                var step_no=$(this).closest("tr").find("td:first-child").text().trim();
                var step_name=$(this).closest("tr").find("td:nth-child(2)").text().trim();
                var div_name=step_name;
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
        }
    });
    /*$('#data_table tr td:nth-child(3)').each(function(){
     $(this).css({'text-align':'left'});
     })*/
}
function InputFailReason(){
    $('#data_table tr td:nth-child(7)').each(function(){
        //$(this).css({'textAlign':'center'});
        var failreason=$(this).text().trim();
        var step_no=$(this).closest("tr").find("td:first-child").text().trim();
        var tc_id=$('#testcaseid').text().trim();
        var step_id=tc_id+"_s"+step_no+"_reason";
        step_id=step_id.trim();
        if($(this).text().trim()!="FailReason"){
            if(failreason!=''){
                $(this).html(failreason);
            }
            else{
                $(this).html('N/A');
            }

        }
    });
}

function MakeStatusSelectable(){
    $('#data_table tr td:nth-child(8)').each(function(){
        //$(this).css({'textAlign':'center'});
        var value=$(this).text().trim();
        var step_no=$(this).closest("tr").find("td:first-child").text().trim();
        var tc_id=$('#testcaseid').text().trim();
        var step_id=tc_id+"_s"+step_no+"_status";
        step_id=step_id.trim();
        console.log(value);
        if(value!="Status"){
            $(this).html(value);
        }

    });
}
function table_message(column,tabledata){
    var message="";
    message+='<table id="data_table" class="two-column-emphasis" style="text-align: left;" width="100%">';
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
        message+=('<th>'+column[i]+'</th> ')
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
            message+=('<td>'+value+'</td>')
        }
        message+='</tr>';
    }
    return message;
}

function related_items(){
    var defectid = $("#defectid").text();
    var mksid = $("#mksid").text();
    var requirementid = $("#requirementid").text();

    $("#edit").click(function(){
        $(this).hide();
        $("#edit_div").show();

        $("#defectid").html('<input class="textbox defectid" style="width: 100%">');
        $(".defectid").val(defectid);
        $("#mksid").html('<input class="textbox mksid" style="width: 100%">');
        $(".mksid").val(mksid);
        $("#requirementid").html('<input class="textbox requirementid" style="width: 100%">');
        $(".requirementid").val(requirementid);
    });

    $("#cancel").click(function(){
        $("#edit_div").hide();
        $("#edit").show();

        $("#defectid").html(defectid);
        $("#mksid").html(mksid);
        $("#requirementid").html(requirementid);
    });

    $("#update").click(function(){
        var testcaseid=$("#testcaseid").text();
        var defect_Id=$('.defectid').val().trim();
        var test_case_Id=$('.mksid').val().trim();
        var required_Id=$('.requirementid').val().trim();

        $.get("Update_RelatedItems/",{
            TC_Id:testcaseid,
            Associated_Bugs_List:defect_Id,
            Manual_TC_Id:test_case_Id,
            Requirement_ID_List:required_Id},function(data) {
            //alert(data);
            var message = "Related Items are updated!";
            desktop_notify(message);
            var location = window.location.pathname;
            window.location=location;
        });
    });
}

function history(){
    var testcaseid=$("#testcaseid").text();
    var testcasename=$("#testcasename").text();
    $("#show_history").click(function(){
        $("#title").text(testcasename);
        PopulateResultDiv(testcaseid);
    });
}

function PopulateResultDiv(tc_id){
    $.get("Selected_TestCaseID_History",{Selected_TC_Analysis : tc_id},function(data){
        ResultTable(Resultdiv,data['Heading'],data['TestCase_Analysis_Result'],"Test Analysis Result");
        makeRunClickable();
        $(".two-column-emphasis").each(function(){
            $(this).css({
                'textAlign':'left'
            })
        });
    });

}
function makeRunClickable(){
    $('#Resultdiv tr>td:first-child').each(function(){
        $(this).css({
            'color':'blue',
            'cursor':'pointer'
        });
        $(this).click(function(){
            var run_id=$(this).text().trim();
            var location='/Home/RunID/'+run_id;
            window.location=location;
        });
    });
}
function convertToString(intTime){
    var hour=Math.floor(intTime/3600);
    intTime=intTime%3600;
    var minuate=Math.floor(intTime/60);
    intTime=intTime%60;
    if(hour<10){
        hour="0"+hour;
    }
    if(minuate<10){
        minuate="0"+minuate;
    }
    if(intTime<10){
        intTime="0"+intTime;
    }
    var stringTime=hour+":"+minuate+":"+intTime;
    return stringTime.trim();
}
function desktop_notify(message){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    var button = document.getElementById('update');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification(message,{body:message, icon:"/site_media/noti.ico"});
    }

    // If the user hasn't told if he wants to be notified or not
    // Note: because of Chrome, we are not sure the permission property
    // is set, therefore it's unsafe to check for the "default" value.
    else if (Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }

            // If the user said okay
            if (status === "granted") {
                var n = new Notification(message,{body:message, icon:"/site_media/noti.ico"});
            }

            // Otherwise, we can fallback to a regular modal alert
            else {
                alertify.log(message,"",0);
            }
        });
    }

    // If the user refuses to get notified
    else {
        // We can fallback to a regular modal alert
        alertify.log(message,"",0);
    }


}
function pass_notify(message){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    var button = document.getElementById('passAll');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification("Status changed to 'Passed'",{body:message, icon:"/site_media/noti.ico"});
    }

    // If the user hasn't told if he wants to be notified or not
    // Note: because of Chrome, we are not sure the permission property
    // is set, therefore it's unsafe to check for the "default" value.
    else if (Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }

            // If the user said okay
            if (status === "granted") {
                var n = new Notification("Status changed to 'Passed'",{body:message, icon:"/site_media/noti.ico"});
            }

            // Otherwise, we can fallback to a regular modal alert
            else {
                alertify.log(message,"",0);
            }
        });
    }

    // If the user refuses to get notified
    else {
        // We can fallback to a regular modal alert
        alertify.log(message,"",0);
    }
}
function change_notify(message){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    var button = document.getElementById('changeStatus');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification("Status changes",{body:message, icon:"/site_media/noti.ico"});
    }

    // If the user hasn't told if he wants to be notified or not
    // Note: because of Chrome, we are not sure the permission property
    // is set, therefore it's unsafe to check for the "default" value.
    else if (Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }

            // If the user said okay
            if (status === "granted") {
                var n = new Notification("Status changes",{body:message, icon:"/site_media/noti.ico"});
            }

            // Otherwise, we can fallback to a regular modal alert
            else {
                alertify.log(message,"",0);
            }
        });
    }

    // If the user refuses to get notified
    else {
        // We can fallback to a regular modal alert
        alertify.log(message,"",0);
    }


}

function go_change(){
    var run_id = $("#runid").text();
    var tcid = $("#testcaseid").text();

    $.ajax({
        url:'Go_TestCaseStatus/',
        dataType : "json",
        data : {
            runid : run_id,
            tcid : tcid
        },
        success: function( json ) {

            if(json[0] == '1'){
                $("#go_previous").hide();
            }
            if(json[0] == json[1]){
                $("#go_next").hide();
            }

            $("#go_status").text(json[0]+'/'+json[1]);
        }
    });

    $("#go_next").click(function(){
        $.ajax({
            url:'Go_TestCaseID/',
            dataType : "json",
            data : {
                runid : run_id,
                tcid : tcid,
                go : 'next'
            },
            success: function( json ) {

                if(json[0] != undefined){
                    window.location = '/Home/RunID/'+run_id+'/TC/'+json[0]+'/View/';
                }
            }
        });

    });

    $("#go_previous").click(function(){
        $.ajax({
            url:'Go_TestCaseID/',
            dataType : "json",
            data : {
                runid : run_id,
                tcid : tcid,
                go : 'previous'
            },
            success: function( json ) {

                if(json[0] != undefined){
                    window.location = '/Home/RunID/'+run_id+'/TC/'+json[0]+'/View/';
                }
            }
        });

    });
}