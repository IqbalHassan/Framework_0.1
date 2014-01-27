
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


                $("p.flip[title =  'Test Type Status']").text("Test type status report of (" +choice + ")" )
                $("p.flip[title =  'Test Type Status']").fadeIn(1000);
                AnalysisTableActions();


                $("#TestTypeStatusTable").css({'text-align':'center', 'cursor' : 'pointer'});



                $("#TestTypeStatusTable .ui-widget tr td:first-child").each(function(){
                    $(this).live('click',function(){


                        $("#TestTypeStatusTable").slideToggle("slow");
                       // ClickedRunId = $(this).text();
                        //var $TC = $(this).text();
                        //var TestSteps;

                        //Following function exist in SearchResult.js file
                        //RunIdTestCases(ClickedRunId)



                    });
                    $(this).css({
                        'color':'blue',
                        'cursor':'pointer',
                        //'font-weight' : 'bold'
                    });
                });
                $("#TestTypeStatusTable .ui-widget tr:nth-child(5n+1)").css({
                    'color':'black',
                    'cursor':'pointer',
                    'font-weight' : 'bold'
                });
            });
        }

    });
});


function AnalysisTableActions()
{

    $("p.flip[title =  'Test Type Status']").click(function() {

        $("#TestTypeStatusTable").slideToggle("slow");
    });

}

