
$(document).ready(function(){

    //Sections
    $.ajax({
        url:'GetSections/',
        dataType : "json",
        data : {
            section : ''
        },
        success: function( json ) {
            if(json.length > 1)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                if(i == 0)return;
                $(".section[data-level='']").append($('<option>').text(value).attr('value', value));
            });
        }
    });

    $(".section").click(function(event)
    {
        var choice = $(".section").val();
        if(choice != 0)
        {
            $.get("TestTypeStatus_Report",{choice : choice},function(data)
            {
                ResultTable(TestTypeStatusTable,data['Heading'],data['TableData'],"Test Type Status Report");

                //Getting Test Case Name
                var TestCaseName = $("#TestTypeStatusTable tr:nth-child(2)>td:nth-child(2)").text()

                //Removing Test Case Name column
                $(".ui-widget th:nth-child(2), .ui-widget td:nth-child(2)").remove()


                $("p.flip[title =  'Test Cases Analysis']").text("Run History of (" + TestCaseName + ":" +Selected_TC_Analysis + ")" )
                $("p.flip[title =  'Test Cases Analysis']").fadeIn(1000);
                AnalysisTableActions()

                //Making Run ID blue color and clickable
                $(".ui-widget tr td:first-child").css({'color':'black', 'cursor' : 'pointer'});


                //When user click on Run Id
                $("#TestTypeStatusTable .ui-widget tr td:first-child").each(function(){
                    $(this).live('click',function(){


                        $("#TestTypeStatusTable").slideToggle("slow");
                        ClickedRunId = $(this).text();
                        var $TC = $(this).text();
                        var TestSteps;

                        //Following function exist in SearchResult.js file
                        RunIdTestCases(ClickedRunId)



                    });
                });



            });
        }
        else
        {
        }

    });
});

