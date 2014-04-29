/*$(document).ready(function(){
	
	
	var URL = window.location.pathname
	indx = URL.indexOf("Analysis")
	if (indx != -1)
	{
		Analysis();
		
	}
	
	
	
	
});


		

function Analysis()
{
	
	$("#searchbox").autocomplete({

		source : 'TestCaseSearch',
		select : function(event, ui) 
		{
			var Selected_TC_Analysis = ui.item[0].split("-").join("-").trim();
            console.log(Selected_TC_Analysis);
			$.get("Selected_TestCaseID_Analaysis",{Selected_TC_Analysis : Selected_TC_Analysis},function(data) 
			{
				ResultTable(TestAnalysisTable,data['Heading'],data['TestCase_Analysis_Result'],"Test Analysis Result");
				
				//Getting Test Case Name
				var TestCaseName = $("#TestAnalysisTable tr:nth-child(2)>td:nth-child(2)").text()
				
				//Removing Test Case Name column
				$(".ui-widget th:nth-child(2), .ui-widget td:nth-child(2)").remove()
				
				// Making Log file link ( Last column of All test cases table)
				$("#TestAnalysisTable tr>td:nth-child(4)").each(function(){
					
					logPath = $(this).text();
					if (logPath != "")
						{
							$(this).html("<a href ='file:///"+logPath+"'>Log File</a>");
						}
				
				});
				
				$("p.flip[title =  'Test Cases Analysis']").text("Run History of (" + TestCaseName + ":" +Selected_TC_Analysis + ")" )
				$("p.flip[title =  'Test Cases Analysis']").fadeIn(1000);
				AnalysisTableActions()
				
				//Making Run ID blue color and clickable
				$(".ui-widget tr td:first-child").css({'color':'black', 'cursor' : 'pointer'});
				
				
				//When user click on Run Id
				$("#TestAnalysisTable tr td:first-child").each(function(){
                    $(this).css({
                       'color':'blue',
                        'cursor':'pointer',
                        'textAlign':'left'
                    });
					$(this).live('click',function(){
						
						
							$("#TestAnalysisTable").slideToggle("slow");
							ClickedRunId = $(this).text();
                            console.log(ClickedRunId);
							var $TC = $(this).text();
							var TestSteps;
							
							//Following function exist in SearchResult.js file
							//RunIdTestCases(ClickedRunId)
                            var location='/Home/RunID/'+ClickedRunId.trim()+'/';
                            window.location=location;
			


					});
				});
				
				
				
			});
			
			
			$("#searchbox").val("");
			return false
		}
	}).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + " - "+item[1]+"<strong> - " + item[2] + "</strong></a>" )
            .appendTo( ul );
    };;

}
	


function AnalysisTableActions()

{
	
	
	$("p.flip[title =  'Test Cases Analysis']").click(function() {
		
		$("#TestAnalysisTable").slideToggle("slow");
	});

}
*/
$(document).ready(function(){
    AutoCompleteSearchForAnalysis();
});

function AutoCompleteSearchForAnalysis(){
    $('#searchbox').autocomplete({
        source:function(request,response){
            $.ajax({
                url:"TestCaseSearch",
                dataType:"json",
                data:{
                    term:request.term
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select:function(event,ui){
            var tc_id=ui.item[0].trim();
            var tc_name=ui.item[1].trim();
            if(tc_id!=""){
                $(this).val(tc_id+' - '+tc_name);
                PopulateResultDiv(tc_id);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + " - "+item[1]+"<strong> - " + item[2] + "</strong></a>" )
            .appendTo( ul );
    };
}

function PopulateResultDiv(tc_id){
    $.get("Selected_TestCaseID_Analaysis",{Selected_TC_Analysis : tc_id},function(data){
        ResultTable(Resultdiv,data['Heading'],data['TestCase_Analysis_Result'],"Test Analysis Result");
        makeRunClickable();
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

    $('#Resultdiv tr>td:last-child').each(function(){
        $(this).css({
            'color':'blue',
            'cursor':'pointer'
        });
        var log=$(this).text().trim();
        if(log != "null"){
            $(this).html('<a target="_blank" href="' +
                log +
                '">log file</a>')
        }
    });
}