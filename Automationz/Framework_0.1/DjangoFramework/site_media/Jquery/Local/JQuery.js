
function MsgBox(Title, MessageText) {
	
	return $("<div class='dialog' title='" + Title + "'><p>" + MessageText + "</p></div>")
    .dialog({
        resizable: false,
        height:440,
        width:500,
        modal: true,
        buttons: {
            "OK": function() {
                $( this ).dialog( "close" );
            },
            /*Cancel: function() {
                $( this ).dialog( "close" );
            }*/
        }
    });

	
	/*$(".dialog").append(
			"<div id = 'MsgBox' title=' " + Title + "'>" + "<p>" + MessageText
					+ " </p>" + "</div>");

	$("#MsgBox").dialog({
		buttons : {
					"OK" : function() {
										$(this).dialog("close");
									  }
				  },

		show : {
				effect : 'drop',
				direction : "up"
			   },
		modal: true
	});*/
}



function ResultTable(HtmlElementID, Heading, tabledata, ResultName) {
	
	$(HtmlElementID).children().remove();
	
	var content = '';
	var mDiffRows = '';
	var mAddress = '';

	if (ResultName != '') {
		content += "<p class = 'Text' style=' color:black; font-size:12px'><b>" + tabledata.length + " " + ResultName
				+ "</b></p>"

	}
	
	
	content += "<table class = 'ui-widget' style='font-size:small; border-collapse:collapse;'  width='100%'>";

	content += '<tr>';
	head = []
	for (head in Heading) {

		content += "<th class='ui-widget-header' >" + Heading[head] + '</th>';
	}
	content += '</tr>'

	items = []
	for (items in tabledata) {

		content += '<tr>';

		table_item = tabledata[items]
		
		for (data in table_item) {
			var mStr = table_item[data];
			if ((String(mStr).indexOf("[") !== -1) == false)
			{
				content += "<td class = 'ui-widget-content'>" + table_item[data]
				+ '</font></td>';
			}
		else
			{
				var mCont = "<table class = 'ui-widget' style='font-size:small; border-collapse:collapse;'>";
//				if ((String(mStr).indexOf(":") !== -1) == true)
//					{
//						mStr = mStr.split(":")[1];
//					}
				
				if ((String(mStr).indexOf(")") !== -1) == false)
					{
						mDiffRows = "Yes";
					}
				if ((String(mStr).indexOf("Details") !== -1) == true || (String(mStr).indexOf("Home Address") !== -1) == true || (String(mStr).indexOf("Other Address") !== -1) == true)
					{
						mAddress = "Yes";
					}
				
				mStr = mStr.replace(/[(]/g,"").replace("[","").replace(/'/g,"");
				
				var mFirstTuple = mStr.split(")");
				var mCol = mFirstTuple[0].split(",").length;
				if (mCol >= 4)
					{
						mAddress = "No";
					}
				mData = mStr.split(",");
				mItems = []
				for (each in mData)
					{
						mItems.push(mData[each]);
					}
				
				
				//This portion of code is for when there are no curly braces
				if (mDiffRows == "Yes")
					{
						mDiffRows = "No";
						for (e in mItems)
						{	
							mItems[e] = mItems[e].replace(/]/g,"");
							mCont += "<td class = 'ui-widget-content' width='50%'>" + mItems[e]
									+ '</td><tr>';
							
						}
					}
				
				//This is for entire data that has addresses in it
				else if(mAddress == "Yes")
					{
						
						mAddress = "No";
						mAddData = mStr.split("])");
						
						mNewData = String(mAddData[0]).split(", [");
						
				//This is for first part of data which just contain Address field
						mAddfreeData = mNewData[0].split(",");
						for (each in mAddfreeData)
							{
								mAddfreeData[each] = mAddfreeData[each].replace(/[)]/g,"").replace(/]/g,"").replace(/'/g,"").replace("[","");
								mCont += "<td class = 'ui-widget-content' width='50%'>" + mAddfreeData[each]
								+ '</td>';
								
								if (each%mCol != 0)
								{
									mCont += "<tr>";
									
								}
								
							}
						
						//This is for the address portion of data after address field
                        //Change here
						if (mNewData.length >= 2)
							{
								mNewData[1] = mNewData[1].split('),')
								var mInsideTable = "<table class = 'ui-widget' style='font-size:small; border-collapse:collapse;'>";
								for (eachinsiderow in mNewData[1])
									{
										mInsideTable += "<tr>";
										insidecoldata = mNewData[1][eachinsiderow].split(',')
										for (eachinsidecol in insidecoldata){
											mInsideTable += "<td class = 'ui-widget-content' width='50%'>" + insidecoldata[eachinsidecol] + "</td>"
										}
										mInsideTable += "</tr>";
									}
								mInsideTable += "</table>";
								//mNewData[1] = mNewData[1].replace(/[)]/g,"").replace(/]/g,"").replace("[","");
								mCont += "<td class = 'ui-widget-content' width='50%'>" + mInsideTable //mNewData[1]
									+ '</td><tr>';
										
								for(var i = 1;i<mAddData.length;i++)
									{
										mRestData = mAddData[i].split(",");
										for(var e = 1;e<mRestData.length;e++)
											{
												mRestData[e] = mRestData[e].replace(/[)]/g,"").replace(/]/g,"").replace(/'/g,"").replace("[","");
												mCont += "<td class = 'ui-widget-content' width='50%'>" + mRestData[e]
												+ '</td>';
												
												if (e%mCol == 0)
												{
													mCont += "<tr>";
													
												}
											}
										
									}
							}
					}
				else
					{
					
					//This part of code is for Address Edits condition
					if ((String(mStr).indexOf("Details") !== -1) == true || (String(mStr).indexOf("Home Address") !== -1) == true || (String(mStr).indexOf("Other Address") !== -1) == true)
					{
						var i = 0;
						
						mEditAddress = String(mStr).split(", [");
						mFieldPart = String(mEditAddress[0]).split(",");
						for (each in mFieldPart)
							{
								mFieldPart[each] = mFieldPart[each].replace(/[)]/g,"").replace(/]/g,"").replace(/'/g,"").replace("[","");
								mCont += "<td class = 'ui-widget-content' width='50%'>" + mFieldPart[each]
										+ '</td>';
								
							}
						mTaskAddress = String(mEditAddress[1]).split("],");
						for (e in mTaskAddress)
							{
								mTaskAddress[e] = mTaskAddress[e].replace(/[)]/g,"").replace(/]/g,"").replace(/'/g,"").replace("[","");
								mCont += "<td class = 'ui-widget-content' width='50%'>" + mTaskAddress[e]
										+ '</td>';
								i = i+1
							}
						
						if (i >= mCol)
							{	
								i = 0;
								mCont += "<tr>";
								
							}
						
					}
					
					//This part of code is for all other condition
					else
						{
							var i = 0;
							for (e in mItems)
								{
									mItems[e] = mItems[e].replace(/[)]/g,"").replace(/]/g,"").replace(/'/g,"").replace("[","");
									mCont += "<td class = 'ui-widget-content' width='50%'>" + mItems[e]
											+ '</td>';
									i = i+1
									if (i >= mCol)
										{	
											i = 0;
											mCont += "<tr>";
											/*mCont += "<td>" + " "
											+ '</td>';
											mCont += "<td>" + " "
											+ '</td>';*/
										}
									
								}
						}
						
					}
				mCont += '</table>';
				content += "<td class = 'ui-widget-content'>" + mCont
				+ '</font></td>';
			}
			
			
		}
	}

	content += '</table>';
	
	$(HtmlElementID).append(content);

}



function RunIdTestCases(ClickedRunId)

{
	
	$.get("RunId_TestCases/",{ClickedRunId:ClickedRunId},function(data){
		
		
		All_Test_Cases = data['AllTestCases']
		Columns = data['Column']
		
		Env_Columns = data['Env_Details_Col']
		Env_Data = data['Env_Details_Data']
		
		Pass_Test_Cases = data['Pass']
		Fail_Test_Cases = data['Fail']
		Fail_Steps = data['failsteps']
		Fail_Step_Col = data['failsteps_Col']
		
		$('#Search_Result_Table').children().remove();
		
		
         //window.location.assign(this.url)
		
		//All Test Cases Table
		All_Test_Cases_Data(All_Test_Cases, Columns)
		TestCase_TestStep_Details_Table('#AllTestCasesTable tr>td:nth-child(2)');
		
		//Test Case Environment Details Table
		Envronment_Data()
		
		//Pass Test Cases Table
		Pass_Test_Cases_Data(Pass_Test_Cases, Columns)
		TestCase_TestStep_Details_Table('#PassTestCasesTable tr>td:nth-child(2)');
		
		//Fail Test Cases Table
		Fail_Test_Cases_Data(Fail_Test_Cases, Columns)
		TestCase_TestStep_Details_Table('#FailTestCasesTable tr>td:nth-child(2)');
		
		Re_Run_Fail_Test_Cases()
		
		//Common Failed Test Steps Table
		Common_Fail_Test_Steps()
		

		//When Clicking on Failed Test Step
		WhenClickingOnCommonFailedTestStep();
		

	});
}

function All_Test_Cases_Data(All_Test_Cases, Columns)

{
	console.log(All_Test_Cases);
	$("p.flip[title =  'All Test Cases']").text("All Test Cases (" + All_Test_Cases.length + ")" )
	$("p.flip[title =  'All Test Cases']").fadeIn(4000);
	
	if (All_Test_Cases.length > 0)
		{
            console.log(Columns);
			ResultTable("#AllTestCasesTable", Columns ,All_Test_Cases,"");

			$("p.flip[title =  'All Test Cases']").bind('click',function(){
				
				$("#AllTestCasesTable").slideToggle("slow");
			});
	    }
	
	// Making Log file link ( Last column of All test cases table)
	$("#AllTestCasesTable tr>td:nth-child(6)").each(function(){
		
		logPath = $(this).text();
		if (logPath != "")
			{
				$(this).html("<a href ='file:///"+logPath+"'>Log File</a>");
				//return;
			}
	
	});
	
	
	//Making MKS link to MKS ID
	$("#AllTestCasesTable tr>td:nth-child(1)").each(function(){
		
		MKS_ID = $(this).text();
		if (MKS_ID != "")
			{
				$(this).html("<a target='_blank' href ='http://mksintegrity:7001/im/issues?selection=" + MKS_ID + "' > "+ MKS_ID + "</a>");
				
			}
	
	});
		return true
}

function Envronment_Data()

{
	
	$("p.flip[title =  'Environment Details']").fadeIn(4000);
	$("#EnvironmentDetailsTable").fadeIn("slow");
	ResultTable("#EnvironmentDetailsTable", Env_Columns, Env_Data,"");
	$("p.flip[title =  'Environment Details']").click(function(){ 
		
		$("#EnvironmentDetailsTable").slideToggle("slow");
	});
	
	$(window).scrollTop();
}

function Pass_Test_Cases_Data(Pass_Test_Cases, Columns)
{
	
	$("p.flip[title =  'Passed Test Cases']").text("Passed Test Cases (" + Pass_Test_Cases.length + ")" )
	$("p.flip[title =  'Passed Test Cases']").fadeIn(4000);
	
	if (Pass_Test_Cases.length > 0)
	{
		ResultTable("#PassTestCasesTable", Columns, Pass_Test_Cases,"");
		$("p.flip[title =  'Passed Test Cases']").click(function(){ 
			
			$("#PassTestCasesTable").slideToggle("slow");
		});
	
	}
	
	// Making Log file link ( Last column of All test cases table)
	$("#PassTestCasesTable tr>td:nth-child(6)").each(function(){
		
		logPath = $(this).text();
		if (logPath != "")
			{
				$(this).html("<a href ='file:///"+logPath+"'>Log File</a>");
			}
	
	});
	
	
	
	//Making MKS link to MKS ID
	$("#PassTestCasesTable tr>td:nth-child(1)").each(function(){
		
		MKS_ID = $(this).text();
		if (MKS_ID != "")
			{
				$(this).html("<a target='_blank' href ='http://mksintegrity:7001/im/issues?selection=" + MKS_ID + "' > "+ MKS_ID + " </a>");
						
			}
	
	});
}

function Fail_Test_Cases_Data(Fail_Test_Cases, Columns)
{
	$("p.flip[title =  'Failed Test Cases']").text("Failed Test Cases (" + Fail_Test_Cases.length + ")" )
	$("p.flip[title =  'Failed Test Cases']").fadeIn(4000);
	
	if (Fail_Test_Cases.length > 0)
	{
		ResultTable("#FailTestCasesTable", Columns, Fail_Test_Cases,"");
		$("p.flip[title =  'Failed Test Cases']").click(function(){ 
			
			$("p.flip[title =  'Rerun']").slideToggle('slow');
			$("p.flip[title =  'Rerun']").each(function(){
				$(this).css("display","inline-block")
			});
			$("#FailTestCasesTable").slideToggle("slow");
		});
	
	}
	
		// Making Log file link ( Last column of failed test cases table)
		$("#FailTestCasesTable tr>td:nth-child(6)").each(function(){
			
			logPath = $(this).text();
			$(this).html("<a href ='file:///"+logPath+"'>Log File</a>");
			
		
		});
		
		
		//Making MKS link to MKS ID
		$("#FailTestCasesTable tr>td:nth-child(1)").each(function(){
			
			MKS_ID = $(this).text();
			if (MKS_ID != "")
				{
					$(this).html("<a target='_blank' href ='http://mksintegrity:7001/im/issues?selection=" + MKS_ID + "' > "+ MKS_ID + " </a>");
							
				}
		
		});

}

function Re_Run_Fail_Test_Cases()

{
	$("p.flip[title = 'Rerun']").click(function(){ 
		
		var RunID = $("#EnvironmentDetailsTable tr td:first-child").text()
		var TesterID = $("#EnvironmentDetailsTable tr td:nth-child(2)").text()
		$.get("ReRun_Fail_TestCases",{RunID:RunID,TesterID:TesterID,ReRunType:$(this).attr('data-id')},function(data){ 
			
			if (data['Response'] == 'False')
				{
					MsgBox("Test Run Error","Sorry! User '" + TesterID + "' is In-Progress or Submitted. Please check the user and re-run again")
					
				} //if
			
			else if (data['Response'] == 'True')
			{
				MsgBox("Test Run Response",	"Failed test cases have been successfully submitted and Run Id is '"+data['RunID']+ "'");
				
			} //else
				
	    }); //Get
	
     }); //Click	

}

function Common_Fail_Test_Steps()
{
	
	$("p.flip[title =  'Failed Steps']").text("Common Failed Steps (" + Fail_Steps.length + ")" )
	$("p.flip[title =  'Failed Steps']").fadeIn(4000);
	if (Fail_Steps.length  > 0)
		
	{
		ResultTable("#FailedStepsTable", Fail_Step_Col, Fail_Steps,"");
		$("p.flip[title =  'Failed Steps']").click(function(){ 
			
			$("#FailedStepsTable").slideToggle("slow");
		});
	
	}
}





function FlipFunction()

{
	$("p:contains('Menu')").click(function() {

		$("#Main_Heading_And_Menu").slideToggle("slow");
	});

	$("p:contains('Hide Test Cases')").click(function() {

		$("#RunTestResultTable").slideToggle("slow");
	});
	
	$("P:contains('Dependency')").click(function() {
		
		$("#DepandencyCheckboxes").slideToggle("slow");
	});
	
	$("P:contains('Test Data Type')").click(function() {
		
		$("div#TestDataTypeCheckboxes").slideToggle("slow");
	});
	
	
	
	
}




