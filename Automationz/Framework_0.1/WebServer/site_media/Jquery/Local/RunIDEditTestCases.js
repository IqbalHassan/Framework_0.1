/**
 * Created by lent400 on 1/15/14.
 */
function ConvertTime(date){
    var Year=date.getFullYear();
    var Month=date.getMonth()+1;
    var day=date.getDate();
    var minuate=date.getMinutes();
    var seconds=date.getSeconds();
    var hour=date.getHours();
    var miliseconds=date.getMilliseconds();
    var time=(Year+"-"+Month+'-'+day+' '+hour+":"+minuate+":"+seconds+'.'+miliseconds).trim();
    return time;
}
var time_start=ConvertTime(new Date());
var test_case_name=$('#testcasename').text().trim();
$(document).ready(function(){
    DataFetch();
    $('#changeStatus').live('click',function(event){
        var time_ended=ConvertTime(new Date());
        var run_id=$('#runid').text().trim();
        var test_case_id=$('#testcaseid').text().trim();
        var step_name=[];
        $('#data_table tr td:nth-child(2)').each(function(){
            var step=$(this).text().trim();
            console.log(step);
            step_name.push(step);
        });
        //step_name.shift();
        var step_status=[];
        $('#data_table tr td:nth-child(6)').each(function(){
            var step_no=$(this).closest("tr").find("td:first-child").text().trim();
            var tc_id=$('#testcaseid').text().trim();
            var step_id=tc_id+"_s"+step_no+"_status";
            step_id=step_id.trim();
            var status=$('#'+step_id+' option:selected').text().trim();
            step_status.push(status);
        });
        //step_status.shift();
        var step_reason=[];
        $('#data_table tr td:nth-child(5)').each(function(){
            var step_no=$(this).closest("tr").find("td:first-child").text().trim();
            var tc_id=$('#testcaseid').text().trim();
            var step_id=tc_id+"_s"+step_no+"_reason";
            var reason=$('#'+step_id).val();
            step_reason.push(reason);
        });
        //step_reason.shift();
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
            test_case_id:test_case_id,
            start_time:time_start,
            end_time:time_ended
        },function(data){
            if(data=="true"){
                //var message = "All Step status changed as submitted";
                //change_notify(message);
                //var message = "All Step status changed as submitted";
                //change_notify(message);
                window.location="/Home/RunID/"+run_id+"/TC/"+test_case_id+"/Execute/";
            }
        });
        event.stopPropagation();
    });
    $('#passAll').live('click',function(event){
        var time_ended=ConvertTime(new Date());
        var run_id=$('#runid').text().trim();
        var test_case_id=$('#testcaseid').text().trim();
        var step_name=[];
        $('#data_table tr td:nth-child(2)').each(function(){
            var step=$(this).text().trim();
            console.log(step);
            step_name.push(step);
        });
        //step_name.shift();
        var step_reason=[];
        $('#data_table tr td:nth-child(5)').each(function(){
            var step_no=$(this).closest("tr").find("td:first-child").text().trim();
            var tc_id=$('#testcaseid').text().trim();
            var step_id=tc_id+"_s"+step_no+"_reason";
            var reason=$('#'+step_id).val();
            step_reason.push(reason);
        });
        //step_reason.shift();
        $.get("UpdateData",{
            step_name:step_name.join('|'),
            step_status:"Passed",
            step_reason:step_reason.join('|'),
            run_id:run_id,
            test_case_id:test_case_id,
            start_time:time_start,
            end_time:time_ended
        },function(data){
            //console.log(data);
            if(data=="true"){
                //var message = "All Test Steps Status are changed to 'Passed'";
                //pass_notify(message);
                //var message = "All Test Steps Status are changed to 'Passed'";
                //pass_notify(message);
                window.location="/Home/RunID/"+run_id+"/TC/"+test_case_id+"/Execute/";
            }
        });
        event.stopPropagation();
    });

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
        else if(value=="true"){
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
                        width : 780,
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
    var column_data=['field','subfield','value','keyfield','ignorefield']
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
                    if(group_data[j][k] && (k==3 || k==4)){
                        message+='<td style="text-align: center;"><a class="notification-indicator tooltipped downwards" data-gotokey="n"><span class="mail-status filled"></span></a></td>';
                    }
                    else if(!group_data[j][k] &&(k==3 || k==4)){
                        message+='<td style="text-align: center;"><a class="notification-indicator tooltipped downwards" data-gotokey="n"><span class="mail-status"></span></a></td>';
                    }
                    else{
                        message+='<td>'+group_data[j][k]+'</td>';
                    }
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

var image_list=['jpg','jpeg','gif','tiff','png','bitmap'];
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
        var attachement_list=data['attachment'];

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
        if(attachement_list.length>0){
            var message='';
            message+='<table class="two-column-emphasis">';
            for(var i=0;i<attachement_list.length;i++){
                if(image_list.indexOf(attachement_list[i][2])!=-1){
                    message+='<tr><td>'+attachement_list[i][1]+'.'+attachement_list[i][2]+'<img src="'+attachement_list[i][0]+'"/></td></tr>';
                }
                else{
                    message+='<tr><td><a target="_blank" href="'+attachement_list[i][0]+'">'+attachement_list[i][1]+'.'+attachement_list[i][2]+'</a> </td></tr>';
                }
            }
            message+='</table>';
            $('#attachement_div').empty();
            $('#attachement_div').html(message);
        }
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
                    step_name:step_name,
                    index:step_no
                },function(data){
                    var message=form_table(data['column'],data['log']);
                    $('#inside_back').html(message);
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
                        width : 720,
                        height : 620,
                        title:'#'+step_no+' - '+div_name

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
colors = {
    'pass' : '#65bd10',
    'fail' : '#fd0006',
    'block' : '#ff9e00',
    'submitted' : '#808080',
    'in-progress':'#0000ff',
    'skipped':'#cccccc',
    'dev': '#aaaaaa',
    'ready': '#65bd10'
};

function form_table(column,log){
    var matching_regex= new RegExp(/Matching Records: (\d+)/i);
    var missing_regex=new RegExp(/Missing Records: (\d+)/i);
    var extra_regex=new RegExp(/Extra Records: (\d+)/i);
    var matching_group_entry=new RegExp(/Matching Group Entry Count: (\d+)/i);
    var non_match_group_entry=new RegExp(/Non Match Group Entry Count: (\d+)/i);
    var missing_group_entry=new RegExp(/Missing Group Entry Count: (\d+)/i);
    var extra_group_entry=new RegExp(/Extra Group Entry Count: (\d+)/i);

    var missing_tuple_data_entry_count=new RegExp(/Missing Tuple Data Entry Count: (\d+)/i);
    var extra_tuple_data_entry_count=new RegExp(/Extra Tuple Data Entry Count: (\d+)/i);
    var keyfield_missing_tuple_data_entry_count=new RegExp(/KeyField Missing Tuple Data Entry Count: (\d+)/i);
    var keyfield_extra_tuple_data_entry_count=new RegExp(/KeyField Extra Tuple Data Entry Count: (\d+)/i);
    var duplicate_in_expected_data_entry_count=new RegExp(/Duplicate in Expected Tuple Data Entry Count: (\d+)/i);
    var duplicate_in_actual_data_entry_count=new RegExp(/Duplicate in Actual Tuple Data Entry Count: (\d+)/i);


    var missing_group_data_entry_count=new RegExp(/Missing Group Data Entry Count: (\d+)/i);
    var extra_group_data_entry_count=new RegExp(/Extra Group Data Entry Count: (\d+)/i);
    var keyfield_missing_group_data_entry_count=new RegExp(/KeyField Missing Group Data Entry Count: (\d+)/i);
    var keyfield_extra_group_data_entry_count=new RegExp(/KeyField Extra Group Data Entry Count: (\d+)/i);
    var duplicate_in_expected_group_data_entry_count=new RegExp(/Duplicate in Expected Group Data Entry Count: (\d+)/i);
    var duplicate_in_actual_group_data_entry_count=new RegExp(/Duplicate in Actual Group Data Entry Count: (\d+)/i);

    var message="";
    message+='<table width="100%" class="two-column-emphasis">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<td>'+column[i]+'</th>';
    }
    message+='</tr>';
    for (var i=0;i<log.length;i++){
        message+='<tr>';
        if(matching_regex.test(log[i])|| missing_regex.test(log[i])||extra_regex.test(log[i])||matching_group_entry.test(log[i])||non_match_group_entry.test(log[i])||missing_group_entry.test(log[i])||extra_group_entry.test(log[i])){
            for(var j=0;j<log[i].length;j++){
                if(j==0){
                    if(log[i][j]=='Passed'){
                        var color=colors['pass'];
                    }
                    if(log[i][j]=='Error'){
                        var color=colors['fail'];
                    }
                    message+='<td style="border-left: 4px solid '+color+'">'+log[i][j]+'</td>'
                }
                else{
                    message+='<td>'+log[i][j]+'</td>';
                }

            }
            if(matching_regex.test(log[i])){
                var column_length=matching_regex.exec(log[i][2]);
            }
            if(missing_regex.test(log[i])){
                var column_length=missing_regex.exec(log[i][2]);
            }
            if(extra_regex.test(log[i])){
                var column_length=extra_regex.exec(log[i][2]);
            }
            if(matching_group_entry.test(log[i])){
                var column_length=matching_group_entry.exec(log[i][2]);
            }
            if(non_match_group_entry.test(log[i])){
                var column_length=non_match_group_entry.exec(log[i][2]);
            }
            if(missing_group_entry.test(log[i])){
                var column_length=missing_group_entry.exec(log[i][2]);
            }
            if(extra_group_entry.test(log[i])){
                var column_length=extra_group_entry.exec(log[i][2]);
            }
            column_length=parseInt(column_length[1]);
            if (column_length>0){
                message+='<tr>';
                message+='<td style="border-left: 4px solid '+color+'">'+log[i][0]+'</td>';
                message+='<td>'+log[i][1]+'</td>';
                message+='<td><table width="100%">';
                message+='<tr><th>&nbsp;</th><th>Field</th><th>Expected</th><th>Actual</th></tr>'
                for(var j=i+1;j<(i+1+column_length);j++){
                    var table_row=log[j][2].split(" : ");
                    message+='<tr>';
                    for (var k=0;k<table_row.length;k++){
                        message+='<td>'+table_row[k]+'</td>';
                    }
                    message+='</tr>';
                }
                message+='</table></td>';
                message+='</tr>';
                i=(i+column_length);
            }
        }

        else if(missing_group_data_entry_count.test(log[i])||extra_group_data_entry_count.test(log[i])||keyfield_missing_group_data_entry_count.test(log[i])||keyfield_extra_group_data_entry_count.test(log[i])||duplicate_in_expected_group_data_entry_count.test(log[i])||duplicate_in_actual_group_data_entry_count.test(log[i])||keyfield_missing_tuple_data_entry_count.test(log[i])||missing_tuple_data_entry_count.test(log[i])||duplicate_in_actual_data_entry_count.test(log[i])||keyfield_extra_tuple_data_entry_count.test(log[i])||extra_tuple_data_entry_count.test(log[i])){
            for(var j=0;j<log[i].length;j++){
                if(j==0){
                    if(log[i][j]=='Passed'){
                        var color=colors['pass'];
                    }
                    if(log[i][j]=='Error'){
                        var color=colors['fail'];
                    }
                    message+='<td style="border-left: 4px solid '+color+'">'+log[i][j]+'</td>'
                }
                else{
                    message+='<td>'+log[i][j]+'</td>';
                }
            }
            if(duplicate_in_expected_data_entry_count.test(log[i])){
                var column_length=duplicate_in_expected_data_entry_count.exec(log[i][2]);
            }
            if(keyfield_missing_tuple_data_entry_count.test(log[i])){
                var column_length=keyfield_missing_tuple_data_entry_count.exec(log[i][2]);
            }
            if(missing_tuple_data_entry_count.test(log[i])){
                var column_length=missing_tuple_data_entry_count.exec(log[i][2]);
            }
            if(extra_tuple_data_entry_count.test(log[i])){
                var column_length=extra_tuple_data_entry_count.exec(log[i][2]);
            }
            if(keyfield_extra_tuple_data_entry_count.test(log[i])){
                var column_length=keyfield_extra_tuple_data_entry_count.exec(log[i][2]);
            }
            if(duplicate_in_actual_data_entry_count.test(log[i])){
                var column_length=duplicate_in_actual_data_entry_count.exec(log[i][2]);
            }

            //Group Data are Here
            if(duplicate_in_actual_group_data_entry_count.test(log[i])){
                var column_length=duplicate_in_actual_group_data_entry_count.exec(log[i][2]);
            }
            if(duplicate_in_expected_group_data_entry_count.test(log[i])){
                var column_length=duplicate_in_expected_group_data_entry_count.exec(log[i][2]);
            }

            if(keyfield_extra_group_data_entry_count.test(log[i])){
                var column_length=keyfield_extra_group_data_entry_count.exec(log[i][2]);
            }
            if(keyfield_missing_group_data_entry_count.test(log[i])){
                var column_length=keyfield_missing_group_data_entry_count.exec(log[i][2]);
            }

            if(extra_group_data_entry_count.test(log[i])){
                var column_length=extra_group_data_entry_count.exec(log[i][2]);
            }
            if(missing_group_data_entry_count.test(log[i])){
                var column_length=missing_group_data_entry_count.exec(log[i][2]);
            }
            column_length=parseInt(column_length[1]);
            if (column_length>0){
                message+='<tr>';
                message+='<td style="border-left: 4px solid '+color+'">'+log[i][0]+'</td>';
                message+='<td>'+log[i][1]+'</td>';
                message+='<td><table width="100%">';
                message+='<tr><th>&nbsp;</th><th>Field</th><th>Value</th></tr>'
                for(var j=i+1;j<(i+1+column_length);j++){
                    var table_row=log[j][2].split(" : ");
                    message+='<tr>';
                    for (var k=0;k<table_row.length;k++){
                        message+='<td>'+table_row[k]+'</td>';
                    }
                    message+='</tr>';
                }
                message+='</table></td>';
                message+='</tr>';
                i=(i+column_length);
            }
        }

        else{
            for(var j=0;j<log[i].length;j++){
                if(j==0){
                    if(log[i][j]=='Passed'){
                        var color=colors['pass'];
                    }
                    if(log[i][j]=='Error'){
                        var color=colors['fail'];
                    }
                    message+='<td style="border-left: 4px solid '+color+'">'+log[i][j]+'</td>'
                }
                else{
                    message+='<td>'+log[i][j]+'</td>';
                }
            }
        }
        message+='</tr>';
    }
    message+='</table>';
    return message;
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
            $(this).html('<textarea id="'+step_id+'" column="100" maxlength="200"/></textarea>');
            $('#'+step_id).val(failreason);
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
            $(this).html('<select class="select-drop" id="'+step_id+'">' +
                '<option value="Passed">Passed</option>' +
                '<option value="Failed">Failed</option>' +
                //'<option value="Not Run">Not Run</option>' +
                '<option value="Skipped">Skipped</option>' +
                '<option value="Submitted">Submitted</option>' +
                '<option value="In-Progress">In-Progress</option>' +
                '</select>'
            );
            $('#'+step_id+' option[value="'+value+'"]').attr({'selected':'selected'});
        }

    });
    $(".select-drop").selectBoxIt();
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
                    var location='/Home/RunID/'+run_id+'/TC/'+json[0]+'/Execute/';
                    window.location = location;
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
                    var location='/Home/RunID/'+run_id+'/TC/'+json[0]+'/Execute/';
                    window.location = location;
                }
            }
        });

    });
}