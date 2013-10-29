$(document).ready(function(){
	
	
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
			var Selected_TC_Analysis = ui.item.value
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
				$("#TestAnalysisTable .ui-widget tr td:first-child").each(function(){
					$(this).live('click',function(){
						
						
							$("#TestAnalysisTable").slideToggle("slow");
							ClickedRunId = $(this).text();
							var $TC = $(this).text();
							var TestSteps;
							
							//Following function exist in SearchResult.js file
							RunIdTestCases(ClickedRunId)
			


					});
				});
				
				
				
			});
			
			
			$("#searchbox").val("");
			return false
		}
	});

}
	


function AnalysisTableActions()

{
	
	
	$("p.flip[title =  'Test Cases Analysis']").click(function() {
		
		$("#TestAnalysisTable").slideToggle("slow");
	});

}
