$(document).ready(function(){

	
	//For Tachyon Build
	$("p.flip[title =  'Tachyon']").click(function(){ 
		
		DailyBranchResult("Tachyon");
		
		
	});
	
	$("p.flip[title =  'Daily Tachyon Build Result']").click(function(){ 
		
		$("#Daily_Tachyon_Build_Result_Table").slideToggle("slow");
	});
	
	
	//For SCM Build
	$("p.flip[title =  'SCM']").click(function(){ 
		
		DailyBranchResult("SCM");
		
	});
		
	$("p.flip[title =  'Daily SCM Build Result']").click(function(){ 
		
		$("#Daily_SCM_Build_Result_Table").slideToggle("slow");
	});
		
});




function DailyBranchResult(BranchName)

{
	
	$("#"+BranchName).slideToggle("slow");
	var Branch = BranchName;
	//if (BranchName =="Tachyon") {Branch = 'tachyon'}
	
	
	$.get("Table_Data_DailyBuild",{Branch:Branch},function(data,status,XHR) { 
		if (data['TableData'].length == 0) 
		{
			
			
			$('#Daily_'+BranchName+'_Build_Result_Table').children().remove();
			$('#Daily_'+BranchName+'_Build_Result_Table').append('<p><b>Sorry There is No Data For '+BranchName+' Daily Build Results!!!</b></p>');
			$('#Daily_'+BranchName+'_Build_Result_Table').fadeIn(400);
		}
		else
		 { 
			$("p.flip[title =  'Daily "+BranchName+" Build Result']").fadeIn(400);
			ResultTable('#Daily_'+BranchName+'_Build_Result_Table',data['Heading'],data['TableData'],"");
			//alert(XHR.getResponseHeader("Location"));
			
			
			var CurrentStep = [ data['CurrentStatus'] , data['DurationTime'] ]
			var SinceLastRun = ["Since Last Successful Run On Bundle: " + data['SinceLastRunBundle'] ,data['SinceLastRun'] ]
			var SinceLastBuild = ["Since Last Build Found: " + data['SinceLastBuildBundle'] ,data['SinceLastBuild'] ]
			var TableData = [CurrentStep,SinceLastRun, SinceLastBuild]
			var Col = ['Current Status','Duration']
			ResultTable("#Current_"+BranchName+"_Status",Col,TableData,'');
			//$("#Current_Status").append("<p>Current Status: "  + Status + "  Duration: " + Duration + "</P>")
		 }
		
	});

}