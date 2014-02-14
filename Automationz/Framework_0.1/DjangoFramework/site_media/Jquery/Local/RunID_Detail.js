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
    When_Clicking_On_CommonFailedTestStep();
    var RunID=$("#EnvironmentDetailsTable tr td:first-child").text().trim();
    $('#run_id').text(RunID.trim());
    drawChart(RunID);
    $('#run_id').live('click',function(){
        window.location='/Home/RunID/'+RunID.trim();
    });
});
function drawChart(RunID){
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
                    title: 'Summary - ' + choice,
                    //width: 500,
                    height: 500,
                    fontSize: 13,
                    titleTextStyle:{fontSize:20},
                    legend:{ textStyle: {fontSize: 17}}
                };
                var chart = new google.visualization.PieChart(document.getElementById('RunIDChart'));
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
                    'cursor':'pointer'
                });
                $(this).live('click',function(){
                    $('#inside_back').html("");
                    //alert(RunID+" "+TestCaseName+" "+$(this).text().trim());
                    $.get("LogFetch",{
                        run_id:RunID,
                        test_case_id:TestCaseName,
                        step_name:$(this).text().trim()
                    },function(data){
                        var step_name=data['step'];
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
                            title:step_name

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
    ////////////**********************\\\\\\\\\\\\\\\
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