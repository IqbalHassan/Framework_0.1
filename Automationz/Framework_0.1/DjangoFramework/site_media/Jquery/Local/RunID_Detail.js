var current_page=1;
var itemPerPage=5;
var UserText='';
$(document).ready(function(){
    RESPONSIVEUI.responsiveTabs();
    itemPerPage=$('#filterCount option:selected').val().trim();
    GetAllData(current_page,itemPerPage,UserText);
    EnableAutocomplete();
    DeleteFilterData();
    $('#filterCount').on('change',function(){
        if($(this).val()!=''){
            itemPerPage=$(this).val();
            current_page=1;
            $('#pagination_tab').pagination('destroy');
            window.location.hash = "#1";
            GetAllData(current_page,itemPerPage,UserText);
        }
    });
    var RunID=$("#fetch_run_id").text().trim();
    $('#run_id').text(RunID.trim());
    //drawChart(RunID);
    $('#run_id').live('click',function(){
        window.location='/Home/RunID/'+RunID.trim();
    });
    //drawGraph(RunID);
    $("#show_chart").click(function(){
        drawGraph(RunID);
    });
    ReRunTab();
    Report();
});
function EnableAutocomplete(){
    $('#searchinput').autocomplete({
        source:function(request,response){
            $.ajax({
                url:"FilterDataForRunID",
                dataType:"json",
                data:{
                    term:request.term,
                    run_id:$('#run_id').text().trim()
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select:function(request,ui){
            var value=ui.item[0].trim();
            if(value!=""){
                $('#searchedFilter').append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>' +
                    '<td class="Text"><b>'+value+':<b style="display: none;">'+ui.item[1].trim()+'</b>&nbsp;</b></td>');
                GetAllData(current_page,itemPerPage,UserText);
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - "+item[1]+"</a>" )
            .appendTo( ul );
    };
}
function DeleteFilterData(){
    $('#searchedFilter td .delete').live('click',function(){
        $(this).parent().next().remove();
        $(this).remove();
        GetAllData(current_page,itemPerPage,UserText);
    });
}
function GetAllData(current_page,itemPerPage,UserText){
    $('#searchedFilter').each(function(){
        UserText = $(this).find("td").text();
        //UserText+='|';
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "");
        console.log(UserText);
        var pathname=window.location.pathname;
        pathname=pathname.split("/")[3];
        $.get("RunID_New",{run_id:pathname.trim(),pagination:current_page,UserText:UserText, capacity:itemPerPage},function(data){
            if(data['runData'].length>0){
                var message=makeTable(data['runData'],data['runCol']);
                $('#allData').html(message);
                $('#pagination_div').pagination({
                    items:data['total'],
                    itemsOnPage:itemPerPage,
                    cssStyle: 'dark-theme',
                    currentPage:current_page,
                    displayedPages:2,
                    edges:2,
                    hrefTextPrefix:'#',
                    onPageClick:function(PageNumber){
                        GetAllData(PageNumber,itemPerPage,UserText);
                    }
                });
                LoadAllTestCases("allData");
                connectLogFile("allData");
                $('#pass_selected').on('click',function(){
                    var list=[];
                    $('.auto_pass:checked').each(function(){
                        if($(this).parent().prev().prev().prev().prev().prev().prev().prev().text().trim()!='Passed'){
                            list.push($(this).val());
                        }
                    });
                    $.get('AutoTestCasePass',{
                        run_id:$('#fetch_run_id').text().trim(),
                        test_cases:list.join("|")
                    },function(data){
                        if(data==true){
                            window.location=('/Home/RunID/'+pathname+'/');
                        }
                    });
                });

            }
            else{
                $('#allData').html('<div align="center" style="margin-top: 20%"><b style="font-size: 200%;font-weight: bolder">No Data Available</b></div>');
            }

        });
    });
}
function makeTable(data,col){
    var message="";
    message+='<table class="two-column-emphasis">';
    message+='<tr>';
    for(var i=0;i<col.length;i++){
        message+='<th align="left">'+col[i]+'</th>';
    }
    message+='</tr>';
    for(var i=0;i<data.length;i++){
        message+='<tr>';
        once = true;
        colors = {
        	'pass' : '#65bd10',
        	'fail' : '#fd0006',
        	'block' : '#ff9e00',
        	'submitted' : '#808080',
            'in-progress':'#0000ff',
            'skipped':'#cccccc'
        };
        for(var j=0;j<data[i].length;j++){
        	if (once === true) {
	        	switch (data[i][3]) {
        		case 'Passed':
        			message+='<td style="border-left: 4px solid ' + colors['pass'] + '">' + data[i][j]+'</td>';
        			break;
        		case 'Failed':
        			message+='<td style="border-left: 4px solid ' + colors['fail'] + '">' + data[i][j]+'</td>';
        			break;
        		case 'Submitted':
        			message+='<td style="border-left: 4px solid ' + colors['submitted'] + '">' + data[i][j]+'</td>';
        			break;
        		case 'Blocked':
        			message+='<td style="border-left: 4px solid ' + colors['block'] + '">' + data[i][j]+'</td>';
        			break;
                case 'In-Progress':
                	message+='<td style="border-left: 4px solid ' + colors['in-progress'] + '">' + data[i][j]+'</td>';
                   break;
                case 'Skipped':
                	message+='<td style="border-left: 4px solid ' + colors['skipped'] + '">' + data[i][j]+'</td>';
                    break;
                }
	        	
        		once = false;
        		continue;
        	}
    		message+='<td>'+data[i][j]+'</td>';
        }
        message+='<td><input type="checkbox" class="auto_pass" value="'+data[i][0]+'"></td>';
        message+='</tr>';
    }
    message+='</table>';
    return message;
}
function MakingReRunClickable(){
    $('#rerun tr>td:nth-child(3)').each(function(){
        $(this).css({
            'color':'blue',
            'cursor':'pointer'
        }) ;
        var test_case_id=$(this).closest('tr').find('td:nth-child(2)').text().trim();
        var name=$(this).text().trim();
        $(this).html('<div id="'+test_case_id+'">'+name+'</div><div id="'+test_case_id+'detail" style="display:none"></div>');
        var name=$(this).closest('tr').find('td:nth-child(2)').text().trim();
        $.get('TestStepWithTypeInTable',{RunID:name},function(data){
            var column=data['column'];
            var resultdata=data['Result'];
            var message="";
            message+='<table class="two-column-emphasis">';
            message+='<tr>';
            for(var i=0;i<column.length;i++){
                message+=('<th align="left">'+column[i]+'</th>');
            }
            message+='</tr>';
            for(var i=0;i<resultdata.length;i++){
                message+='<tr>';
                for(var j=0;j<resultdata[i].length;j++){
                    message+=('<td align="left">'+resultdata[i][j]+'</td>');
                }
                message+='</tr>';
            }
            message+='</table> ';
            $('#rerun '+'#'+test_case_id+'detail').html(message);
        });
        $('#rerun '+'#'+test_case_id).live('click',function(){
            $('#rerun '+'#'+test_case_id+'detail').fadeToggle(500);
        });
    });
}
function ReRunTab(){
    $('.rerunTab').click(function(){
        $(this).toggleClass('down');
        //Making the status known to all
        var statusList=[]
        $('.rerunTab').each(function(){
            if($(this).hasClass('down')){
                var temp=$(this).text().trim();
                statusList.push(temp);
            }
        });
            //console.log(temp);
            $.get('ReRun',{
                status:statusList.join(','),
                RunID:$('#fetch_run_id').text().trim()
            },function(data){
                var column=data['col'];
                var data_list=data['list'];
                if(data_list.length==0){
                    $('#rerun').css({'marginTop':'20%'});
                    $('#rerun').html('<b style="color:#ccc;font-size:400%;font-weight:bolder;">No Test Cases</b>');
                    $('#additional_data').fadeOut(100);
                }
                else{
                    var message="";
                    message+='<table class="two-column-emphasis"><tr><th>Select</th>';
                    for(var i=0;i<column.length;i++){
                        message+='<th>'+column[i]+'</th>';
                    }
                    message+='</tr>';
                    for(var i=0;i<data_list.length;i++){
                        message+='<tr><td><input type="checkbox" name="checklist" value="'+data_list[i][0]+'"/></td>';
                        for(var j=0;j<data_list[i].length;j++){
                            message+='<td>'+data_list[i][j]+'</td>';
                        }
                        message+='</tr>';
                    }
                    message+='</table>';
                    $('#rerun').css({'marginTop':'0%'});
                    $('#rerun').html(message);
                    MakingReRunClickable();
                    $('input[name="checklist"]').attr('checked','true');
                    $('#additional_data').fadeIn(500);
                }
            });

        console.log(statusList);
    });
    MakingReRunClickable();
    $('#selectall').live('click',function(){
        $('input[name="checklist"]').attr('checked','true');
    });
    $('#submit_button').live('click',function(){
        var tc_list=[];
        $('input[name="checklist"]:checked').each(function(){
            tc_list.push($(this).val());
        });
        if(tc_list.length==0){
            //alert('Test Cases are not selected');
            alertify.log('Test Cases are not selected',"",0);
            return false;
        }
        var queryText="";
        for(var i=0;i<tc_list.length;i++){
            queryText+=tc_list[i].trim();
            queryText+=": ";
        }
        $.get("Run_Test",{
            RunTestQuery:queryText,
            //EmailIds:emailText,
            //TesterIds:testerText,
            //DependencyText:dependencyText,
            //TestObjective:objective,
            //Env:environment,
            ReRun:"rerun",
            RunID:$('#fetch_run_id').text().trim()
            //project_id:project_id.trim(),
            //team_id:team_id
        },function(data){
            if(data['Result']){
                var oldid = $("#run_id").text().trim();
                var message = "Re-run Executed with ID - '"+data['runid']+"' from the previous run ID - '"+oldid+"'!";
                desktop_notify(message);
                var location='/Home/RunID/'+data['runid']+'/';
                window.location=location;
            }
        });
    });
}
function drawGraph(RunID){
    $.get("chartDraw",
        {
            runid:RunID
        },
        function(data){
            console.log(data);
            /***************pie chart***********************/

            RenderPieChart('chart', [
                ['Passed ('+data[1]+')',     data[1]],
                ['Failed ('+data[2]+')',      data[2]],
                ['Blocked ('+data[3]+')',  data[3]],
                ['In-Progress ('+data[4]+')', data[4]],
                ['Submitted ('+data[5]+')',  data[5]],
                ['Skipped ('+data[6]+')', data[6]]
            ],'Run-ID Summary : ' + RunID);

            /*google.load("visualization", "1", {packages:["corechart"], callback:drawChart});

            function drawChart() {
                var piedata = google.visualization.arrayToDataTable([
                    ['Run Status', 'Total Case Number'],
                    ['Passed ('+data[1]+')',     data[1]],
                    ['Failed ('+data[2]+')',      data[2]],
                    ['Blocked ('+data[3]+')',  data[3]],
                    ['In-Progress ('+data[4]+')', data[4]],
                    ['Submitted ('+data[5]+')',  data[5]],
                    ['Skipped ('+data[6]+')', data[6]]
                ]);
                var options = {
                    title: 'Run-ID Summary : ' + RunID,
                    //width: 500,
                    height: 500,
                    fontSize: 13,
                    titleTextStyle:{fontSize:19, color: '#4183c4', fontName:'Helvetica Neue, Helvetica, Arial, sans-serif'},
                    legend:{ textStyle: {fontSize: 17}},
                    colors:['#65bd10','#FD0006','#FF8C00','blue','grey','#88a388']
                };
                var chart = new google.visualization.PieChart(document.getElementById('chart'));
                chart.draw(piedata, options);
            }*/
        });
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

function LoadAllTestCases(divname){

    $('#'+divname+' tr td:nth-child(2)').each(function(){
        $(this).css({
            'color':'blue',
            'cursor':'pointer',
            'textAlign':'left'
        });
        var name=$(this).text().trim();
        var TestCaseName=$($(this).closest("tr").find("td:first-child")[0]).text().trim();
        var RunID=$('#fetch_run_id').text().trim();
        $(this).html('<div id="'+TestCaseName+'name">'+name+'</div><div id="'+TestCaseName+'detail" style="display:none"></div>')
        $.get("TestCase_Detail_Table",{'RunID':RunID,'TestCaseName':TestCaseName},function(data){
            ResultTable('#'+divname+' #'+TestCaseName+'detail',data['TestCase_Detail_Col'],data['TestCase_Detail_Data'],"");
        })
        $('#'+divname+' #'+TestCaseName+'name').live('click',function(){
            var TestCaseName=$($(this).closest('tr').find('td:first-child')[0]).text().trim();
            $('#'+divname+' #'+TestCaseName+'detail tr td:first-child').each(function(){
                $(this).css({
                    'color':'blue',
                    'cursor':'pointer',
                    'textAlign':'left'
                });
                $(this).live('click',function(){
                    $('#inside_back').html("");
                    //alert(RunID+" "+TestCaseName+" "+$(this).text().trim());
                    $.get("LogFetch",{
                        run_id:RunID,
                        test_case_id:TestCaseName,
                        step_name:$(this).text().trim()
                    },function(data){
                        var stepname=data['step'];
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
                            title:stepname

                        });
                    });
                    e.stopPropagation();
                });
            });
            $('#'+divname+' #'+TestCaseName+'detail').slideToggle("slow");
        });
    });
    /////// To change status on clicking the status
    $('#'+divname+' tr td:nth-child(10)').each(function(){
        $(this).css({
            'color':'blue',
            'cursor' : 'pointer'
        });
        $(this).live('click',function(){
            var TestCaseName=$($(this).closest("tr").find("td:first-child")[0]).text().trim();
            var location=$("#fetch_run_id").text().trim();
            console.log(location);
            window.location='/Home/RunID/'+location+'/TC/'+TestCaseName+'/Execute/';
        });
    });
    $('#'+divname+' tr td:nth-child(9)').each(function(){
        $(this).css({
            'color':'blue',
            'cursor' : 'pointer'
        });
        $(this).live('click',function(){
            var TestCaseName=$($(this).closest("tr").find("td:first-child")[0]).text().trim();
            var location=$("#fetch_run_id").text().trim();
            console.log(location);
            window.location='/Home/RunID/'+location+'/TC/'+TestCaseName+'/View/';
        });
    });
    $('#'+divname+' tr td:nth-child(4)').each(function(){
        $(this).css({
            'color':'blue'
        });
    });
    $('#'+divname+' tr td:nth-child(3)').each(function(){
        $(this).css({'textAlign':'left'});
    });
    $('#'+divname+' tr td').each(function(){
        $(this).css({'textAlign':'left'});
    });
    ////////////**********************\\\\\\\\\\\\\\\
    //////////////// To change the textbox in fail reason
    $('#'+divname+' tr td:nth-child(7)').each(function(){
        var data=$(this).text().trim();
        $(this).html('<textarea rows="3" cols="30" readonly="readonly" style="border: none;text-align: left; vertical-align: middle;color: #669;display:inline-block;">'+data+'</textarea>');
    });
    /////////////////////////////////////////////////////
    /*$('#'+divname+' tr td:last-child').each(function(){
     $(this).remove();
     });*/
}
function connectLogFile(ID){
    $("#"+ID+" tr td:nth-child(8)").each(function(){
        var location=$(this).text();
        var message='<a href="file:///'+location+'">Log File</a>';
        $(this).html(message);
    })
}
function When_Clicking_On_CommonFailedTestStep(){
    $("#FailedStepsTable tr>td:nth-child(1)").css({
        'color':'blue',
        'cursor':'pointer'
    });
    $('#FailedStepsTable tr td:nth-child(1)').each(function(){
        var RunID=$("#fetch_run_id").text().trim();
        var name=$(this).text().trim();
        var stepName=name.split('(')[0].trim();
        var div_name=name.split('(')[0].trim().split(' ').join('_');
        $(this).append('<div id="'+div_name+'" style="display:none"></div>');
        $.get("FailStep_TestCases",{
            RunID : RunID,
            FailedStep : stepName
        },function(data){
            var column=data['FailStep_TC_Col'];
            var data_detail=data['FailStep_TestCases'];
            ResultTable('#'+div_name,column,data_detail,"");
            //LoadAllTestCases(div_name);
            connectLogFile(div_name);
        });
        $(this).live('click',function(e){
            $('#FailedStepsTable #'+div_name).slideToggle("slow");
            e.stopPropagation();
        });
    });
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

    var button = document.getElementById('submit_button');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification("Re-run Executed!",{body:message, icon:"/site_media/noti.ico"});
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
                var n = new Notification("Re-run Executed!",{body:message, icon:"/site_media/noti.ico"});
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


function RenderPieChart(elementId, dataList, title) {
    Highcharts.setOptions({
        colors: ['#65bd10','#FD0006','#FF8C00','blue','grey','#88a388']
    });
    new Highcharts.Chart({
        chart: {
            renderTo: elementId,
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            height: 500
        }, title: {
            text: title
        },
        tooltip: {
            /*formatter: function () {
             return '<b>' + this.point.name + '</b>: ' + this.percentage + ' %';
             }*/
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    /*formatter: function () {
                        return '<b>' + this.point.name + '</b>: ' + this.percentage + ' %';
                    }*/
                }
                /*dataLabels: {
                 enabled: false
                 }*/,
                showInLegend: true,
                size : '95%'
            }
        },
        series: [{
            type: 'pie',
            name: 'Bundle Report',
            data: dataList
        }]
    });
}

function Report(){
    $("#email_list").autocomplete({

        source : 'AutoCompleteEmailSearch',
        select : function(event, ui) {

            var value = ui.item.value
            $("#email").append('<td><img class="delete" id = "DeleteEmail" title = "EmailDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
                + '<td class="Text">'
                + value
                + ":&nbsp"
                + '</td>');

            //$("#SelectedEmail th").css('display', 'block');

            $("#email_list").val("");
            return false;

        }
    });

    $("#email_list").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });

    //Delete Seleted Email Ids
    $("#DeleteEmail").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });

    $("#send_report").click(function(){
        var RunID=$("#fetch_run_id").text().trim();

        var EmailQuery="";
        $("#email").each( function()
        {
            EmailQuery = $(this).find("td").text();
            EmailQuery = EmailQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        });
        if(EmailQuery.length==0){
            alertify.log("Email Receipient is to be selected from suggestion","",0);
            return false;
        }

        $.get("Send_Report",{runid : RunID,EmailIds:EmailQuery},function(data)
        {
            if(data[0]=="OK")
            {
                alertify.log("Email Report is sent to the recipients","",0);
            }
            else
            {
                alertify.log("Email Report is not sent. Server disconnected","",0);
            }
        });
    });
}