$(document).ready(function(){
	
	//Add AutoComplete Search from
	var DepandencyNameList = []
	
	
	AddAutoCompleteSearchBox("#Place_AutoComplete_Here","Search Test Cases Data By Keywords:");
	
	AvailebableTestMachineflipButton();
	
	
	//Calling AutoComplete Search Function
		
	RunTestAutocompleteSearch();
	
	
	//======================Calling flip Code =================
		FlipFunction();
	
	
	// Calling DeleteSearchQueryText for Deleting query text after clicking on delete button
		DeleteSearchQueryText();
	
	
	// On Clicking Auto Complete Search Button, Send Query Text to View.py > AjaxData function
	$(".Buttons[title='Search Test Cases']").click(function(){ 
		
		if ($("#AutoSearchTextBoxLabel").text() != "Search User:")
		{
			PerformSearch();
		}
		
	});
	
	
	
	// On Clicking Auto Complete Verify Query Button, Send Query Text to View.py > Verify_Query function
	$(".Buttons[title='Verify Query']").click(function(){ 
		
		VerifyQueryProcess();
	 });
	
	
	
	// On Clicking Select User Button, Send Query Text to View.py > SelectUser function
	$(".Buttons[title='Select User']").click(function(){ 
		
		
		
		SelecteUserProcess();
		
		SelectEmail();
	 });
	
	
	
	// On Clicking Run Test Button, Send Query Text to View.py > RunTest function
	$(".Buttons[title='Run Test']").click(function(){ 
	
		RunTestProcess();
		
	});
	
	
	
});



function SendingQueryAndDepandency()
{
	
	$("#AutoSearchResult #searchedtext").each(function() {
		var UserText = $(this).find("td").text();
		UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
		
		$.get("Verify_Query", {Query : UserText}, function(data) 
		{
			if (data["DepandencyList"].length != 0 )
			{	
				var DepandencyName = "";
				var DepandencyNameList = [];
				for (Depand in data["DepandencyList"]) 
				{
					var DepandencyName = "";
					DepandencyName = data["DepandencyList"][Depand][0]
					DepandencyNameList.push(DepandencyName)
				}
			}
			
			//$("#DepandencyCheckboxes form#device_memory input").is(":checked")			
			$("input [type='radio'], #DepandencyCheckboxes").each(function()
			{
				$(this).live('click',function()
				{	
					var Text = [];
					for (i in DepandencyNameList)
					{
						temp = $("#DepandencyCheckboxes form#" +DepandencyNameList[i]+ " input:checked").val();
						if(temp !== undefined)
						{
							Text += temp + ":";
							
						}
					}
					
					if ( (Text.split(":").length)-1 === (DepandencyNameList.length) )
						{
							$(".Buttons[title='Select User']").fadeIn(2000)
							$("#DepandencyCheckboxes").slideToggle("slow");
						}
					
				});
			});
		});
	});
	
}

/*
+"<table id='AutoSearchResult' style='display: block;' >"
+ "<tbody>"
	+ "<tr>"
		+ "<td>"
			+ "<p> </p>"
			+ "<label > <b id = 'AutoSearchTextBoxLabel' class = 'Text'>"
			+ Label
			+ " </b></label>"
			+ "<input id='searchbox' type='text' title = 'Please Type Keyword and Click On that to add to query' name='searchboxname' />"

			+"<img class='Buttons Dependency' title = 'DependencySign' style='display:none; margin-left: 80px;' src = '/site_media/DependencySign.png'></img>"
			+"<label class='Dependency Text' style='display:none; font-weight: bold; font-size:15px'></label>"
			
			
			+ "<label  class = 'Text SearchEmail' style = 'display:none'  > <b> Select Email: </b></label>"
			+"<input  id = 'EmailSearchBox' class='SearchEmail' style = 'display:none' type='text' title = 'Please Select Email by Keyword' />"
			
		+ "</td>"
		+"<td><p> &nbsp; </p> </td>"
	    

	+ "</tr>"
+ "</tbody>"
+ "</table>"
*/


function AddAutoCompleteSearchBox(WhereToPlaceId, Label)
{	
	
	$(WhereToPlaceId).append(
						
			
					"<form method = 'get' >"

							+"<table id='AutoSearchResult' style='display: block;' >"
								+ "<tbody>"
									+ "<tr>"
										
										+ "<td>"
											+ "<p> </p>"
											+ "<label > <b id = 'AutoSearchTextBoxLabel' class = 'Text'>"
											+ Label
											+ " </b></label>"
											+ "<input id='searchbox' type='text' title = 'Please Type Keyword and Click On that to add to query' name='searchboxname' />"
										+ "</td>"
										
										+ "<td>"
										
											+"<p class='flip' title='DepandencyCheckBox' style='color: ; width: 60% ; margin-left: 50% ;display:None; margin-top: 10px;'>Please Select Dependency</p>"
											+"<div id = 'DepandencyCheckboxes' class = 'Text'  style= 'display:none;color: ;margin-left: 50%'>"
											
											+" </div>"
											
											+"<label  class = 'Text SearchEmail' style = 'display:none'  > <b> Select Name for Email: </b></label>"
											+"<input  id = 'EmailSearchBox' class='SearchEmail' style = 'display:none' type='text' title = 'Please Select Email by Keyword' />"
											
										+ "</td>"
										
									    
		
									+ "</tr>"
								+ "</tbody>"
							+ "</table>"
							
							
							+"<table id = 'AutoSearchResult' >"
								+ "<tbody>"
									+ "<tr id = 'searchedtext'>"
										+ "<th class = 'Text' style= 'text-align: left'> Test Data Set: </th>"
										
									+ "</tr>"
									
								 + "</tbody>"	
							+ "</table>"
							
							+"<table id = 'AutoSearchResult' >"
								+ "<tbody>"
									+ "<tr id = 'SelectedEmail' class='SearchEmail' style='display:none'>"
								    	
										+ "<th class = 'Text' style= 'text-align: left'> Selected Email: </th>"
								    + "</tr>"
							    + "</tbody>"	
							+ "</table>"
				  + "</form>"
			
			
	
	);
}


function AvailebableTestMachineflipButton()
{
	$(".flip[title='Availeable Test Machine']").click(function(){
		
		$("#AvailableTestMachine").slideToggle("slow");
		var SearchUser = "True"
		$.get("Table_Data_UserList",{UserListRequest : SearchUser},function(data) {
		ResultTable('#AvailableTestMachine', data['Heading'],data['TableData'], "Available User/s");
		
		});
	}); 
	
}


function RunTestAutocompleteSearch()

{
	
	$("#searchbox").autocomplete(
			{
				source : 'AutoCompleteTestCasesSearch',
				select : function(event, ui) {

						var tc_id_name = ui.item.value.split(" - ");
						var value = "";
						if (tc_id_name != null)
							value = tc_id_name[0];

							// Checking if Search Text box is for User Search
						if ($("#AutoSearchTextBoxLabel").text() == "Select Test Machine:")

						{
								$(".Buttons[title='Select User']").css('display', 'none');
								$(".Buttons[title='Run Test']").fadeIn(2000);

						}

						else 
							(value != "")
						{
								$(".Buttons[title='Search']").fadeIn(2000);

								$("#Main_Heading_And_Menu").slideUp("slow");
								$("p:contains('Menu')").fadeIn(2000);

								$("#AutoSearchResult #searchedtext").append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
														+ '<td name = "submitquery">'
														+ value
														+ ":&nbsp"
														+ '</td>');

								if ($("#AutoSearchTextBoxLabel").text() != "Search User:") {
									PerformSearch();
								}
							}
							$("#searchbox").val("");
							return false
						},

		});

	$("#searchbox").keypress(function(event) {
		if (event.which == 13) {

			event.preventDefault();

		}

		if ($("#AutoSearchTextBoxLabel").text() != "Select Test Machine:") {
			PerformSearch();
		}
	});

}


function FlipFunction()

{
	$("p:contains('Menu')").click(function() {

		$("#Main_Heading_And_Menu").slideToggle("slow");
	});

	$("p:contains('Hide Test Cases')").click(function() {

		$("#RunTestResultTable").slideToggle("slow");
	});
	
	$("P:contains('Depandency')").click(function() {
		
		$("#DepandencyCheckboxes").slideToggle("slow");
	});
}


function PerformSearch() {
	$("#AutoSearchResult #searchedtext").each(function() {
						var UserText = $(this).find("td").text();
						UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")

						$.get("Table_Data_TestCases",{Query : UserText},function(data) {

											if (data['TableData'].length == 0)
											{
												$('#RunTestResultTable').children().remove();
												$('#RunTestResultTable').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
												$("#DepandencyCheckboxes").children().remove();
												$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
											} 
											else 
											{
												ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");

												$("#RunTestResultTable").fadeIn(4000);
												$("p:contains('Show/Hide Test Cases')").fadeIn(2000);

												// ===============To Make First
												// td or each tr (i.e Test Case
												// ID) Click able

												$(".ui-widget tr td:first-child").css({'color' : '','cursor' : 'pointer'});
												$(".ui-widget tr td:first-child").each(function() {
													$(this).live('click',function() {

													$(this).children().slideToggle("slow");
														var ClickedTC = $(this).text();
														var RunID = $("#EnvironmentDetailsTable tr td:first-child").text()
														var $TC = $(this).text();
														var TestSteps;
														$.get("TestCase_TestSteps",{ClickedTC : ClickedTC,RunID: RunID},function(data) {

															TestSteps = data['Result'];
															$(".ui-widget tr td:first-child").each(function() {
																if (($(this).text()) == ClickedTC) 
																{
																  for (eachitem in data['Result']) 
																  {
																	$($(this)).append("<p id = 'TestCase_Steps'>"+ data['Result'][eachitem]																																				+ "</p>");
																  }
																}

															  $("p#TestCase_Steps").css({'color' : 'silver','cursor' : 'text'});
															});

														});

													});
												});

												VerifyQueryProcess();
												//$(".Buttons[title='Verify Query']").fadeIn(2000);
												$(".Buttons[title='Select User']").fadeOut();
											}

										});

					});

}


function SelecteUserProcess() {

	$("#searchbox").autocomplete({

		source : 'AutoCompleteUsersSearch',
	});
	var SearchUser = "True"
	$(".flip[title='DepandencyCheckBox'], #DepandencyCheckboxes").css('display','None');	
	$.get("Table_Data_UserList",{UserListRequest : SearchUser},function(data) {

		//When User Clicks on Availebable Test Machine flip image
		$(".flip[title='Availeable Test Machine']").click(function(){
			
			$("#AvailableTestMachine").slideToggle("slow");
			ResultTable('#AvailableTestMachine', data['Heading'],data['TableData'], "Available User/s");
			
		}); //End Of Code
		
		
		
		if (data['TableData'].length == 0) 
		{
			$("#AutoSearchTextBoxLabel").text("Select Test Machine:");
			$('#RunTestResultTable').children().remove();
			$('#RunTestResultTable').append('<p><b>Sorry There is No Availaable User To Run The Test!!!</b></p>');
		}
		
		else 
		{
			ResultTable('#RunTestResultTable', data['Heading'],data['TableData'], "Available User/s");

			$("#AutoSearchTextBoxLabel").text("Select Test Machine:");

			$(".Buttons[title='Search Test Cases']").fadeOut(2000);
			
			$(".delete").css('cursor','default');
			
			$(".SearchEmail").fadeIn(2000);
			
		 }

	});
}


function VerifyQueryProcess()

{	
	
	$("#DepandencyCheckboxes").children().remove();
	$("#AutoSearchResult #searchedtext").each(function() {
		var UserText = $(this).find("td").text();
		UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
		
		$.get("Verify_Query", {Query : UserText}, function(data) {
			
			if (data["DepandencyList"].length != 0 )
			{
					
				$(".flip[title='DepandencyCheckBox']").css('display','block');
					for (Depand in data["DepandencyList"]) 
					{
						var content = ""
						
						DepandencyName = data["DepandencyList"][Depand][0]
						content += "<form id = '" + DepandencyName + "'action=''>"
						content += "<p>" +DepandencyName+ "</p>"
						lis = data["DepandencyList"][Depand]
						lis.shift();
						
						for (items in lis) 
						{
								content += "<input type='radio' name =  '" +DepandencyName+ "'value = '"  + lis[items]  + "' >" + lis[items] + "<br>"
								
						}
						
						content += "</form>"
						$("#DepandencyCheckboxes").append(content )
						
					}
					
			}
			
		});
		
	});
	
	
	SendingQueryAndDepandency();
		
			
			
			
			/*
			if (data['Result'] == 'Error') {
				$(".Dependency").fadeIn(2000);
				
				$(".Dependency").text("Don't Forget To Add Dependency: " + data['Response'])
				//MsgBox("Test Case Selection Error", data['Response']);
				
			}

			else {
				$(".Dependency").fadeOut(2000)
				$(".Buttons[title='Select User']").fadeIn(2000)
				
				
				// css("display","block");

			}
			
			*/

		
		
		

	
}


function DeleteSearchQueryText()

{

	$("#AutoSearchResult td .delete").live('click', function() {
		
		if ($("#AutoSearchTextBoxLabel").text() != "Select Test Machine:") //If user is on select user page, do not allow him to delete the Test Data Set
		{
			$(this).parent().next().remove();
			$(this).remove();
			$("#AutoSearchResult #searchedtext").each(function() {
				var UserText = $(this).find("td").text();
				if (UserText.length == 0)
				{
					//$(".Buttons[title='Search Test Cases']").fadeOut(2000);
					//$(".Buttons[title='Verify Query']").fadeOut(2000);
					$(".Buttons[title='Select User']").fadeOut(2000);
				}
			});
		
		}
		
		else 
		{
			
			$(".delete").css('cursor','default');
		}

	});
}


function SelectEmail()
{
	$("#EmailSearchBox").autocomplete({

		source : 'AutoCompleteEmailSearch',
		select : function(event, ui) {

			var value = ui.item.value
			$("#AutoSearchResult #SelectedEmail").append('<td><img class="delete" id = "DeleteEmail" title = "EmailDelete" src="/site_media/deletebutton.png" /></td>'
					+ '<td class="Text">'
					+ value
					+ ":&nbsp"
					+ '</td>');
			
			$("#EmailSearchBox").val("");
			return false
			
		}
	});
	
	$("#EmailSearchBox").keypress(function(event) {
		if (event.which == 13) {

			event.preventDefault();

		}
	});
	
	
	//Delete Seleted Email Ids
	$("#DeleteEmail").live('click', function() {
		
		$(this).parent().next().remove();
		$(this).remove();
		
	});
	

}


function RunTestProcess() {

	$("#AutoSearchResult #searchedtext").each( function() {
				var RunTestQuery = $(this).find("td").text();
				RunTestQuery = RunTestQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
				
				//Getting Selected Email ids
				$("#AutoSearchResult #SelectedEmail").each( function() {
					var Email= $(this).find("td").text();
					EmailIds = Email.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
				});
				
				$.get("Run_Test", {RunTestQuery : RunTestQuery,EmailIds:EmailIds}, function(data) {

					MsgBox("Test Run Response",
							"Your Test Run Request Has Been Submitted, Here is the result :"
									+ data['Result'])
					// alert(data['Result']);

				});

			});
}