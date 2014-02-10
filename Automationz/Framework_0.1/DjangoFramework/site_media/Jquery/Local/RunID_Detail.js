/**
 * Created by lent400 on 1/13/14.
 */
$(document).ready(function(){
    LoadAllTestCases("AllTestCasesTable");
    connectLogFile("AllTestCasesTable");
    LoadAllTestCases("PassTestCasesTable");
    connectLogFile("PassTestCasesTable");
    LoadAllTestCases("FailTestCasesTable");
    connectLogFile("FailTestCasesTable");
    buttonPreparation();
    When_Clicking_On_CommonFailedTestStep();
});
function buttonPreparation(){
    $(".flip[title='All Test Cases']").click(function(){
        $("#AllTestCasesTable").slideToggle("slow");
    });
    $(".flip[title='Passed Test Cases']").click(function(){
        $("#PassTestCasesTable").slideToggle("slow");
    });
    $(".flip[title='Failed Test Cases']").click(function(){
        $("p.flip[title =  'Rerun']").slideToggle('slow');
        $("p.flip[title =  'Rerun']").each(function(){
            $(this).css("display","inline-block")
        });
        $("#FailTestCasesTable").slideToggle("slow");
    });
    $(".flip[title='Failed Steps']").click(function(e){
        e.stopPropagation();
        $("#FailedStepsTable").slideToggle("slow");

    });
}
function LoadAllTestCases(divname){

    $('#'+divname+' tr td:nth-child(2)').each(function(){
        $(this).css({
            'color':'blue',
            'cursor':'pointer',
            'textAlign':'left'
        });
        var TestCaseName=$(this).closest("tr").find("td:nth-child(8)").text().trim();
        var RunID=$('#EnvironmentDetailsTable tr td:first-child').text().trim();
        $(this).append('<div id="'+TestCaseName+'detail" style="display:none"></div>')
        $.get("TestCase_Detail_Table",{'RunID':RunID,'TestCaseName':TestCaseName},function(data){
            ResultTable('#'+divname+' #'+TestCaseName+'detail',data['TestCase_Detail_Col'],data['TestCase_Detail_Data'],"");
        })
        $(this).live('click',function(){
            var TestCaseName=$(this).closest("tr").find("td:nth-child(8)").text().trim();
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
    $('#FailedStepsTable tr>td:nth-child(1)').each(function(){
        var RunID=$("#EnvironmentDetailsTable tr td:first-child").text().trim();
        var name=$(this).text().trim();
        var stepName=name.split('(')[0].trim();
        console.log(stepName);
        $(this).append('<div id="'+stepName.split(' ').join('_')+'"></div>');
        $.get("FailStep_TestCases",{
            RunID : RunID,
            FailedStep : stepName
        },function(data){
            var column=data['FailStep_TC_Col'];
            var data_detail=data['FailStep_TestCases'];
            ResultTable('#'+stepName.split(' ').join('_'),column,data_detail,"");

            var div_name=stepName.split(' ').join('_');
            //LoadAllTestCases(div_name);
            connectLogFile(div_name);
        });
        $(this).live('click',function(e){
            $('#'+stepName.split(' ').join('_')).slideToggle("slow");
            e.stopPropagation();
        });
    });
 }