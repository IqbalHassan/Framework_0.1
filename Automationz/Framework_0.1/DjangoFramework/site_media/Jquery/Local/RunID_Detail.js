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
    $(".expand_button").live('click',function(e){
        var TestCaseName=$(this).attr("id");
        var div_name=$(this).attr("class").split(" ")[1].trim();
        console.log(div_name);
        TestCaseName=TestCaseName.split(":")[1].trim();
        //console.log(TestCaseName);
        var current=$(this);
        var RunID=$("#EnvironmentDetailsTable tr td:first-child").text().trim();
        $.get("TestCase_Detail_Table",{RunID : RunID,TestCaseName : TestCaseName},function(data){
            /*console.log(data['TestCase_Name']);
            console.log(data['TestCase_Detail_Data']);
            console.log(data['TestCase_Detail_Col']);*/
            //console.log(current.attr("id"));
            current.closest("td").append('' +
                '<div id="'+TestCaseName+'detail" style="display:block"></div>');
            ResultTable("#"+TestCaseName+"detail",data['TestCase_Detail_Col'],data['TestCase_Detail_Data'],"");
            //console.log(div_name+'is going down');
            //$(this).css({'display':'none'});
            $("#"+div_name+" #"+TestCaseName+"detail").slideDown("slow");
        });
        e.stopPropagation();
    });
    $(".collapse_button").live('click',function(e){
        var TestCaseName=$(this).attr("id");
        TestCaseName=TestCaseName.split(":")[1].trim();
        var div_name=$(this).attr("class").split(" ")[1].trim();
        //console.log("#"+TestCaseName+"detail");
        //console.log(div_name+' is going up');
        $("#"+div_name+" #"+TestCaseName+"detail").slideUp("slow");
        e.stopPropagation();
    });
    $(".edit_button").live('click',function(){
        var TestCaseName=$(this).attr("id");
        TestCaseName=TestCaseName.split(":")[1].trim();
        var location=$("#EnvironmentDetailsTable tr td:first-child").text().trim();
        console.log(location);
        window.location='/Home/RunID/'+location+'/TC/'+TestCaseName+'/';
    });
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
    $('#'+divname+' tr td:nth-child(2)').css({
        'color':'blue',
        'cursor':'pointer'
    });
    $('#'+divname+' tr td:nth-child(2)').each(function(){
        var name=$(this).closest("tr").find("td:nth-child(7)").text().trim();
        console.log(name);
        $(this).append('' +
            '<div align="right" style="padding-right: 3px;">' +
            '<img class="edit_button '+divname+'" id="edit:'+name+ '" src="/site_media/edit_case.png" style="margin-left:50px;background-color: transparent; width:10px; height:10px;text-align: right"/>' +
            '<img class="expand_button '+divname+'" id="expand:'+name+ '" src="/site_media/add_step.png" style="margin-left:30px;background-color: transparent; width:10px; height:10px;text-align: right"/>'
        +'<img class="collapse_button '+divname+'" id="collapse:'+name+ '" src="/site_media/minus.png" style="margin-left:10px;background-color: transparent; width:10px; height:10px;text-align: right"/></div>');
    });
}
function connectLogFile(ID){
    $("#"+ID+" tr td:nth-child(6)").each(function(){
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