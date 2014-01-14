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
    $(".expand_button").live('click',function(){
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
                '<div id="'+data['TestCase_Name']+'detail" style="display:block"></div>');
            ResultTable("#"+data['TestCase_Name']+"detail",data['TestCase_Detail_Col'],data['TestCase_Detail_Data'],"");
            //console.log(div_name+'is going down');
            //$(this).css({'display':'none'});
            $("#"+div_name+" #"+data['TestCase_Name']+"detail").slideDown("slow");
        });
    });
    $(".collapse_button").live('click',function(){
        var TestCaseName=$(this).attr("id");
        TestCaseName=TestCaseName.split(":")[1].trim();
        var div_name=$(this).attr("class").split(" ")[1].trim();
        //console.log("#"+TestCaseName+"detail");
        //console.log(div_name+' is going up');
        $("#"+div_name+" #"+TestCaseName+"detail").slideUp("slow");
    });
    When_Clicking_On_CommonFailedTestStep();
});
function buttonPreparation(){
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
    $(".flip[title='Failed Steps']").click(function(){
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
        $(this).append('<div align="right" style="padding-right: 3px;"><img class="expand_button '+divname+'" id="expand:'+name+ '" src="/site_media/add_step.png" style="margin-left:50px;background-color: transparent; width:10px; height:10px;text-align: right"/>'
        +'<img class="collapse_button '+divname+'" id="collapse:'+name+ '" src="/site_media/minus.png" style="margin-left:10px;background-color: transparent; width:10px; height:10px;text-align: right"/></div>');
        $(this).live('click',function(){
            var ClickedRunId=$("#EnvironmentDetailsTable tr td:first-child").text().trim();
            var location='/Home/RunID/'+ClickedRunId+'/'+name+'/';
            window.location=location;
        });
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

 }
