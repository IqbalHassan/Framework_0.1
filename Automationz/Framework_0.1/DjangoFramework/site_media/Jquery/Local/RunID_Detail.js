/**
 * Created by lent400 on 1/13/14.
 */
$(document).ready(function(){
    RESPONSIVEUI.responsiveTabs();
    LoadAllTestCases("AllTestCasesTable");
    connectLogFile("AllTestCasesTable");
    LoadAllTestCases("PassTestCasesTable");
    connectLogFile("PassTestCasesTable");
    LoadAllTestCases("FailTestCasesTable");
    connectLogFile("FailTestCasesTable");
    LoadAllTestCases("SubmittedTestCasesTable");
    connectLogFile("SubmittedTestCasesTable");
    //buttonPreparation();
    When_Clicking_On_CommonFailedTestStep()
    var RunID=$("#EnvironmentDetailsTable tr td:first-child").text().trim();
    $('#run_id').text(RunID.trim());
    //drawChart(RunID);
    $('#run_id').live('click',function(){
        window.location='/Home/RunID/'+RunID.trim();
    });
    drawGraph(RunID);
    ReRunTab();
});
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
            console.log(data);
            var column=data['column'];
            var resultdata=data['Result'];
            var message="";
            message+='<table class="one-column-emphasis">';
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
            console.log(message);
            $('#rerun '+'#'+test_case_id+'detail').html(message);
        });
        $('#rerun '+'#'+test_case_id).live('click',function(){
            $('#rerun '+'#'+test_case_id+'detail').fadeToggle(500);
        });
    });
}
function ReRunTab(){
    $('.filter-item').click(function(){
        $('.filter-item').removeClass('selected');
        $(this).addClass('selected');
        $.get('ReRun',{
            status:$(this).attr('data-id').trim(),
            RunID:$('#EnvironmentDetailsTable tr>td:first-child').text().trim()
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
                message+='<table class="one-column-emphasis"><tr><th>Select</th>';
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
            alert('Test Cases are not selected');
            return false;
        }
        //console.log(tc_list);
        var machine=$('input[name="machine"]').val();
        var tester=$('input[name="tester"]').val();
        var client=$('input[name="client"]').val();
        var email=$('input[name="email"]').val();
        var os=$('input[name="os"]').val();
        var objective=$('#test_objective').val();
        os=os.split("-")[0].trim();
        os=os.split(" ")[0].trim();
        var environment="";
        if(os=='Windows'){
            environment="PC";
        }
        else{
            environment="Mac";
        }
        //console.log(os);
        objective=objective.trim();
        if(objective==""){
            alert("TestObjective is empty");
            return false;
        }
        var queryText="";
        for(var i=0;i<tc_list.length;i++){
            queryText+=tc_list[i].trim();
            queryText+=": ";
        }
        queryText+=((machine.trim())+':');
        //console.log(queryText);
        var testerText="";
        tester=tester.split(",");
        for(var i=0;i<tester.length;i++){
            testerText+=tester[i];
            testerText+=": ";
        }
        //console.log(testerText);
        var emailText="";
        email=email.split(",");
        for(var i=0;i<email.length;i++){
            emailText+=email[i];
            emailText+=": ";
        }
        //console.log(emailText);
        var dependencyText="";
        dependencyText+=(client+": ");
        //console.log(dependencyText);
        $.get("Run_Test",{
            RunTestQuery:queryText,
            EmailIds:emailText,
            TesterIds:testerText,
            DependencyText:dependencyText,
            TestObjective:objective,
            Env:environment,
            ReRun:"rerun",
            RunID:$('#EnvironmentDetailsTable tr>td:first-child').text().trim()
        },function(data){
            if(data['Result']){
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
            google.load("visualization", "1", {packages:["corechart"], callback:drawChart});

            function drawChart() {
                var piedata = google.visualization.arrayToDataTable([
                    ['Run Status', 'Total Case Number'],
                    ['Passed',     data[1]],
                    ['Failed',      data[2]],
                    ['Blocked',  data[3]],
                    ['In-Progress', data[4]],
                    ['Submitted',  data[5]],
                    ['Skipped', data[6]]
                ]);
                var options = {
                    title: 'Run-ID Summary : ' + RunID,
                    width: 500,
                    height: 500,
                    fontSize: 13,
                    titleTextStyle:{fontSize:16},
                    legend:{ textStyle: {fontSize: 17}},
                    colors:['#65bd10','#FD0006','#FF8C00','blue','grey','#88a388']
                };
                var chart = new google.visualization.PieChart(document.getElementById('chart'));
                chart.draw(piedata, options);
            }
        });
}
function LoadAllTestCases(divname){

    $('#'+divname+' tr td:nth-child(2)').each(function(){
        $(this).css({
            'color':'blue',
            'cursor':'pointer',
            'textAlign':'left'
        });
        var name=$(this).text().trim();
        var TestCaseName=$(this).closest("tr").find("td:nth-child(8)").text().trim();
        var RunID=$('#EnvironmentDetailsTable tr td:first-child').text().trim();
        $(this).html('<div id="'+TestCaseName+'name">'+name+'</div><div id="'+TestCaseName+'detail" style="display:none"></div>')
        $.get("TestCase_Detail_Table",{'RunID':RunID,'TestCaseName':TestCaseName},function(data){
            ResultTable('#'+divname+' #'+TestCaseName+'detail',data['TestCase_Detail_Col'],data['TestCase_Detail_Data'],"");
        })
        $('#'+divname+' #'+TestCaseName+'name').live('click',function(){
            var TestCaseName=$(this).closest("tr").find("td:nth-child(8)").text().trim();
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
    $('#'+divname+' tr td:nth-child(4)').each(function(){
        $(this).css({
            'color':'blue',
            'cursor' : 'pointer'
        });
        $(this).live('click',function(){
            var TestCaseName=$(this).closest("tr").find("td:nth-child(8)").text().trim();
            var location=$("#EnvironmentDetailsTable tr td:first-child").text().trim();
            console.log(location);
            window.location='/Home/RunID/'+location+'/TC/'+TestCaseName+'/';
        });
    });
    $('#'+divname+' tr td:nth-child(3)').each(function(){
        $(this).css({'textAlign':'center'});
    });
    ////////////**********************\\\\\\\\\\\\\\\
    //////////////// To change the textbox in fail reason
    $('#'+divname+' tr td:nth-child(6)').each(function(){
        var data=$(this).text().trim();
        console.log(data);
        $(this).html('<textarea rows="3" cols="30" readonly="readonly" style="border: none">'+data+'</textarea>');
    });
    /////////////////////////////////////////////////////
}
function connectLogFile(ID){
    $("#"+ID+" tr td:nth-child(7)").each(function(){
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
        var RunID=$("#EnvironmentDetailsTable tr td:first-child").text().trim();
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