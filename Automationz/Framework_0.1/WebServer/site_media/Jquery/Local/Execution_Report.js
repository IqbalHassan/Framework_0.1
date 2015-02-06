$(document).ready(function(){

	
	//For PC
	/*$("p.flip[title =  'GeneratePCReport']").click(function(){
		
		GenerateReport("SCM");
	});*/
	
	/*$("p.flip[title =  'Daily Tachyon Build Result']").click(function(){ 
		
		$("#Daily_Tachyon_Build_Result_Table").slideToggle("slow");
	});
	
	
	//For SCM Build
	$("p.flip[title =  'SCM']").click(function(){ 
		
		DailyBranchResult("SCM");
		
	});
		
	$("p.flip[title =  'Daily SCM Build Result']").click(function(){ 
		
		$("#Daily_SCM_Build_Result_Table").slideToggle("slow");
	});*/
		
});

function GenerateReport(BranchName)

{	
	$("#"+BranchName).slideToggle("slow");
	var Branch = BranchName;
	
	$.get("Execution_Report_Table", function(data) { 
		
		if (data['Result'].length == 0) 
		{
			
			$('#Daily_'+BranchName+'_Build_Result_Table').children().remove();
			$('#Daily_'+BranchName+'_Build_Result_Table').append('<p><b>Sorry There is No Data For '+BranchName+' Daily Build Results!!!</b></p>');
			$('#Daily_'+BranchName+'_Build_Result_Table').fadeIn(400);
		}
		else
		 { 
			ResultTable('#Daily_'+BranchName+'_Build_Result_Table',data['Headings'],data['Result'],"");
			//$(".ui-widget table").css({'width':'100%'});
			$(".ui-widget tr td:not(:first-child)").css({'color':'#D9D9D9', 'cursor' : 'text','text-decoration':'none','text-align':'center'});
			
			
			$("#Daily_SCM_Build_Result_Table").width(1000);
			$("#Daily_SCM_Build_Result_Table").slideToggle("slow");
		 }
		
		
		
	});

}