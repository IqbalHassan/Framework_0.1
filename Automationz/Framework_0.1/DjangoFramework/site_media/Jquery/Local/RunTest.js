$(document).ready(function(){
	
	var Env = ""
	var URL = window.location.pathname
	indx = URL.indexOf("Run")
	if (indx != -1)
	{
		//when use will click on PC flip bar
		$(".flip[title='PC_Platform']").click(function(){ 
			
			$(".flip[title='Availeable Test Machine']").fadeIn(1000)
			$("#Place_AutoComplete_Here").fadeIn(1000)
			
			$(".flip[title='Mac_Platform']").css({'display':'none'})
			$(".text[title='Choose']").text('Welcome to PC Environment Test Lab');
			//$(".flip[title='PC_Platform']").text('Welcome to PC Environment Test Lab');
			//$(".flip[title='PC_Platform']").css({ 'cursor':'default','margin-left': '40%', 'height': '15%' , 'width': '200%'})
			$(".flip[title='PC_Platform']").css({'display':'none'})
			
			Env = "PC"
			RunTestAutocompleteSearch(Env);
			
		});
		
		
		//when user will click on Mac flip bar
		$(".flip[title='Mac_Platform']").click(function(){ 
			
			$(".flip[title='Availeable Test Machine']").fadeIn(1000)
			$("#Place_AutoComplete_Here").fadeIn(1000)
			
			$(".flip[title='PC_Platform']").css({'display':'none'})
			$(".text[title='Choose']").text('Welcome to Mac Environment Test Lab');
			//$(".flip[title='Mac_Platform']").text('Welcome to Mac Environment Test Lab');
			//$(".flip[title='Mac_Platform']").css({ 'cursor':'default','margin-left': '-100%','height': '15%' , 'width': '200%'})
			$(".flip[title='Mac_Platform']").css({'display':'none'})
			
			Env = "Mac"
			RunTestAutocompleteSearch(Env);
		});
		
		
		
			
			AddAutoCompleteSearchBox("#Place_AutoComplete_Here","Search Test Cases Data By Keywords:");
			
			AvailebableTestMachineflipButton(Env);
			
			
			
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
				
				
				$("P:contains('Test Data Type')").fadeOut(1000);
				SelecteUserProcess();
				SelectEmail();
			 });
			
			
			
			// On Clicking Run Test Button, Send Query Text to View.py > RunTest function
			$(".Buttons[title='Run Test']").click(function(){ 
			
				RunTestProcess();
				
			});
	
	  }
	
});


 var DepandencyNameList = [];

function SendingQueryAndDepandency()
{
	DepandencyNameList = []
	$("#AutoSearchResult #searchedtext").each(function() 
	{
		var UserText = $(this).find("td").text();
		UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
		Env = Get_Selected_Env_Name()
	
		$.get("Verify_Query", {Query : UserText, Env: Env}, function(data) 
		{
			if (data["DepandencyList"].length != 0 )
			{	
				var DepandencyName = "";
				//var DepandencyNameList = [];
				for (Depand in data["DepandencyList"]) 
				{
					var DepandencyName = "";
					DepandencyName = data["DepandencyList"][Depand][0]
					DepandencyNameList.push(DepandencyName)
				}
			}
			
			else
			{
				$(".Buttons[title='Select User']").fadeIn(2000)
			}
		
			
			//$("#DepandencyCheckboxes form#device_memory input").is(":checked")			
			$("input [type='radio'], #DepandencyCheckboxes").each(function()
			{
				$(this).live('click',function()
				{	
					var Text = "";
					var DNL = DepandencyNameList
					for (i in DNL)
					{	
						temp = $("#DepandencyCheckboxes form#" +DNL[i]+ " input:checked").val();
						if(temp !== undefined)
						{
							Text += temp + ":";
						}
					}
					DNL = ""
					if ( (Text.split(":").length)-1 === (DepandencyNameList.length) )
					{
						$(".Buttons[title='Select User']").fadeIn(2000)
						$("#DepandencyCheckboxes").slideUp("slow");
						$("#AutoSearchResult #DependencyText td").remove()
						var DNL = DepandencyNameList
						for (t in DNL)
						{	
							Depend = $("#DepandencyCheckboxes form#" +DNL[t]+ " input:checked").val();
							if(Depend !== undefined)
							{
								//Text += Depend + ":";
								$("#AutoSearchResult #DependencyText").css('display','block')
								$("#AutoSearchResult #DependencyText").append(
										
										'<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
										+ '<td name = "Dependencyquery" class = "Text" style = "size:10">'
										+ Depend
										+ ":&nbsp"
										+ '</td>'
										 );
								
							}
						}
						DNL = ""
						
					}
					
					
				});
				
			});
					
					
				
				
			
		});
	});		
				
				
					
				
			
		
	
	
}


function AddAutoCompleteSearchBox(WhereToPlaceId, Label)
{	
	
	$(WhereToPlaceId).append(
						
			
		"<form method = 'get' >"

				+"<table id='AutoSearchResult' style='display: block;' >"
					+ "<tbody>"
						+ "<tr>"
							//Dependency CheckBoxes
							+"<td>"
								+"<p class='flip' title='DepandencyCheckBox' style='color: black; width: 43%  ;display:None; margin-top: 10px;'>Please Select Dependency</p>"
								+"<div id = 'DepandencyCheckboxes' class = 'Text'  style= 'margin-right: 50%; display:block; color: black;'>"
								+" </div>"
						    +"</td>"
							
							
							//Test Data Type CheckBoxes
							+"<td style='position:relative;left:700px;'>"	 
								+"<p  class='flip' id = 'TestDataTypeCheckboxes' title='TestDataTypeCheckBox' style='color: black; width: 160%  ;display:none; margin-top: -94px;'>Test Data Type</p>"
								+"<div id = 'TestDataTypeCheckboxes' class = 'Text'  style= 'display:none; color: black;'>"
								+"<form  action =''>"
									+"<input   class=' ui-corner-all'  type='radio' name = 'TestDataType' value = 'Default' checked='checked' >Default <br>"
									+"<input   class=' ui-corner-all'  type='radio' name = 'TestDataType' value = 'Performance'>Performance <br>"
									+"<input   class=' ui-corner-all'  type='radio' name = 'TestDataType' value = 'Localization'>Localization <br>"
								+"</form>"
								+" </div>"
							+"</td>"
						+ "</tr>"
						
						
						+"<tr>"
							//Search Email Input Box
							+"<td>"
								+"<label  class = 'Text SearchEmail' style = 'display:none' > <b> Select Name for Email: </b></label>"
								+"<input  id = 'EmailSearchBox' class='SearchEmail ui-corner-all' style = 'display:none' type='text' title = 'Please Select Email by Keyword' />"
							+ "</td>"
						+"</tr>"
						
						+"<tr>"
						
								+"<td >"
									+"<label  style = 'display:none'   class = 'Text' id = 'TestObjective' > <b> *Test Objective: </b></label>"
								+"</td>"
							
								+"<td>"
									+"<input class = 'ui-corner-all' id = 'TestObjective' style = 'display:none; margin-left: -58%'  size = '42' maxlength = '50' type='text' title = 'Type Test Obejct' />"
								+"</td>"
						+"</tr>"		
								
							
					
					
						+ "<tr>"
							+ "<td>"
								+ "<label > <b id = 'AutoSearchTextBoxLabel' class = 'Text'>"
								+ Label
								+ " </b></label>"
								+ "<input class = 'ui-corner-all' id='searchbox' style = 'margin-left:-2%' type='text' title = 'Please Type Keyword and Click On that to add to query' name='searchboxname' />"
							+ "</td>"
						+ "</tr>"
						
						
					+ "</tbody>"
				+ "</table>"
				
				
				+"<table id = 'AutoSearchResult' >"
					+ "<tbody>"
						
						+ "<tr id = 'searchedtext'>"
							+"<p> </p>"
							+ "<th class = 'Text' style= 'text-align: left'> Test Data Set: </th>"
						+ "</tr>"
						
					+ "</tbody>"	
				+ "</table>"
						
				
				
				
				
				+"<table id = 'AutoSearchResult' >"
					+ "<tbody>"
						+ "<tr id = 'DependencyText' style = 'display:None' >"
							+ "<th class = 'Text' style= 'text-align: left'> Parameters:&nbsp;&nbsp;&nbsp; </th>"
						+ "</tr>"
						
					 + "</tbody>"	
				+ "</table>"
				
				
				+"<table id = 'AutoSearchResult' >"
					+ "<tbody>"
						+ "<tr id = 'SelectedEmail' class='SearchEmail' style='display:None'>"
					    	
							+ "<th class = 'Text' style= 'display:None ; text-align: left'>Email Name:&nbsp;&nbsp;&nbsp; </th>"
					    + "</tr>"
				    + "</tbody>"	
				+ "</table>"
	  + "</form>"
			
			
	
	);
}


function AvailebableTestMachineflipButton()
{
	$(".flip[title='Availeable Test Machine']").click(function(){
		
		Env = Get_Selected_Env_Name()
		
		
		$("#AvailableTestMachine").slideToggle("slow");
		var SearchUser = "True"
		$.get("Table_Data_UserList",{UserListRequest : SearchUser, Env: Env},function(data) {
		ResultTable('#AvailableTestMachine', data['Heading'],data['TableData'], "Available User/s");
		
		//Removing Unnecessary columns
		//$("#AvailableTestMachine .ui-widget th:nth-child(1), .ui-widget td:nth-child(1)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(2), .ui-widget td:nth-child(2)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(3), .ui-widget td:nth-child(3)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(6), .ui-widget td:nth-child(6)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(9), .ui-widget td:nth-child(9)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(12), .ui-widget td:nth-child(12)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(15), .ui-widget td:nth-child(15)").remove()
		//$("#AvailableTestMachine .ui-widget th:nth-child(16), .ui-widget td:nth-child(16)").remove()
		
		
		
		});
	}); 
	
}


function RunTestAutocompleteSearch(Env)

{
	
	$("#searchbox").autocomplete(
			{
				//Calling AutoCompleteTestSearch function with 'term'(default) parameter and Env variable
				//So AutoCompleteTestSearch function in View.py will receive two variable 'term' (this is the one when user type on search box) and Env variable.
				
				
				/*source :  'AutoCompleteTestCasesSearch' ,
					
					extraParams: {
									Env: function() {return Env},
                    
								  },*/

				source : function(request, response) {
				    									$.ajax({
				    											url:"AutoCompleteTestCasesSearch",
				    											dataType: "json",
				    											data:{ term: request.term, Env: Env },
				    											success: function( data ) {
				    																			response( data );
				    																	   }
				    									});
				  									 },

				//source : 'AutoCompleteTestCasesSearch?Env = ' +Env,
				select : function(event, ui) {

						var tc_id_name = ui.item.value.split(" - ");
						var value = "";
						if (tc_id_name != null)
							value = tc_id_name[0];

							// Checking if Search Text box is for User Search
						if ($("#AutoSearchTextBoxLabel").text().trim() === "*Select Test Machine:")

						{
								$(".Buttons[title='Select User']").css('display', 'none');
								$(".Buttons[title='Run Test']").fadeIn(2000);
								$("P:contains('Dependency')").fadeOut(1000);
								$("P:contains('Test Data Type')").fadeOut(1000);
						}

						else 
							(value != "")
						{
								$(".Buttons[title='Search']").fadeIn(2000);

								//$("#Main_Heading_And_Menu").slideUp("slow");
								$("p:contains('Menu')").fadeIn(2000);

								$("#AutoSearchResult #searchedtext").append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
														+ '<td name = "submitquery" class = "Text" style = "size:10">'
														+ value
														+ ":&nbsp"
														+ '</td>');

								if ($("#AutoSearchTextBoxLabel").text() != "Search User:") {
									PerformSearch();
								}
							}
							$("#searchbox").val("");
							return false
						}

		});

	$("#searchbox").keypress(function(event) {
		if (event.which == 13) {

			event.preventDefault();

		}

		if ($("#AutoSearchTextBoxLabel").text().trim() === "*Select Test Machine:") {
			PerformSearch();
		}
	});

}




function PerformSearch() {
	$("#AutoSearchResult #searchedtext").each(function() {
						var UserText = $(this).find("td").text();
						UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
						Env = Get_Selected_Env_Name()
						$.get("Table_Data_TestCases",{Query: UserText, Env: Env},function(data) {

											if (data['TableData'].length == 0)
											{
												$('#RunTestResultTable').children().remove();
												$('#RunTestResultTable').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
												$("#DepandencyCheckboxes").children().remove();
												//$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
											} 
											else 
											{
												ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");

												$("#RunTestResultTable").fadeIn(4000);
												$("p:contains('Show/Hide Test Cases')").fadeIn(2000);

												// ===============To Make First
												// td or each tr (i.e Test Case
												// ID) Click able
												//Making MKS link to MKS ID
												$("#RunTestResultTable tr>td:nth-child(1)").each(function(){
													
													MKS_ID = $(this).text();
													if (MKS_ID != "")
														{
															$(this).html("<a target='_blank' href ='http://mksintegrity:7001/im/issues?selection=" + MKS_ID + "' > "+ MKS_ID + " </a>");
																	
														}
												
												});		
												
											//	TestCase_TestStep_Details_Table('#RunTestResultTable tr>td:nth-child(2)');

												$(".ui-widget tr td:nth-child(2)").css({'color' : 'skyblue','cursor' : 'pointer'});
												$(".ui-widget tr td:nth-child(2)").each(function() {
													$(this).live('click',function() {
														
														var childrenCount = $(this).children().length
														if (childrenCount == 0)
														{
															$(this).children().slideDown();
														}
														else
														{
															$(this).children().slideUp();
															return;
														}
														var ClickedTC = $(this).text();
														var RunID = $(this).closest('tr').find('td:nth-child(1)').text();
														RunID = RunID.trim();
														
														var $TC = $(this).text();
														var TestSteps;
														$.get("TestCase_TestSteps_SearchPage",{ClickedTC : ClickedTC,RunID: RunID},function(data) {
															TestSteps = data['Result'];
															
															$(".ui-widget tr td:nth-child(2)").each(function() {
																if (($(this).text()) == ClickedTC) 
																{
																	
																	$(this).children().remove();
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
	
	$("#PlatformChose").remove()
	$("#searchbox").autocomplete({

		source : 'AutoCompleteUsersSearch',
	});
	var SearchUser = "True"
	$(".flip[title='DepandencyCheckBox'], #DepandencyCheckboxes").css('display','None');
	$("div#TestDataTypeCheckboxes, p#TestDataTypeCheckboxes").css('display','None');
	$(".flip[title = 'Availeable Test Machine']").css('display','None');
	
	Env = Get_Selected_Env_Name()
	$.get("Table_Data_UserList",{UserListRequest : SearchUser, Env: Env},function(data) {

		//When User Clicks on Availebable Test Machine flip image
		$(".flip[title='Availeable Test Machine']").click(function(){
			
			//$("#AvailableTestMachine").slideToggle("slow");
			ResultTable('#AvailableTestMachine', data['Heading'],data['TableData'], "Available User/s");
			
		}); //End Of Code
		
		
		
		if (data['TableData'].length == 0) 
		{
			$("#AutoSearchTextBoxLabel").html("<b>*Select Test Machine:&nbsp;&nbsp;</b>");
			$('#RunTestResultTable').children().remove();
			$('#RunTestResultTable').append('<p class = "Text"><b>Sorry There is No Availaable User To Run The Test!!!</b></p>');
		}
		
		else 
		{
			ResultTable('#RunTestResultTable', data['Heading'],data['TableData'], "Available User/s");

			$("#AutoSearchTextBoxLabel").html("<b>*Select Test Machine:&nbsp;&nbsp;  </b>");

			$(".Buttons[title='Search Test Cases']").fadeOut(1000);
			
			$(".delete").css('cursor','default');
			
			$(".SearchEmail").fadeIn(1000);
			$("P:contains('Dependency')").fadeOut(100);
			$("P:contains('Test Data Type')").fadeOut(100);
			
			$("label#TestObjective, input#TestObjective").css("display","block");
			
		 }

	});
}


function VerifyQueryProcess()

{	
	
	
	$("#DepandencyCheckboxes").children().remove();
	$("#AutoSearchResult #searchedtext").each(function() {
		var UserText = $(this).find("td").text();
		UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
		Env = Get_Selected_Env_Name()
		
		$.get("Verify_Query", {Query : UserText, Env: Env}, function(data) {
			
			if (data["DepandencyList"].length != 0 )
			{
					
				$(".flip[title='DepandencyCheckBox']").css('display','block');
				$("p#TestDataTypeCheckboxes").css('display','block');
				
					for (Depand in data["DepandencyList"]) 
					{
						var content = ""
						
						DepandencyName = data["DepandencyList"][Depand][0]
						content += "<form id = '" + DepandencyName + "'action=''>"
						content += "<p style = 'margin:0'>" +DepandencyName+ "</p>"
						lis = data["DepandencyList"][Depand]
						lis.shift();
						
						for (items in lis) 
						{
								content += "<input class = 'ui-corner-all' type='radio' name =  '" +DepandencyName+ "'value = '"  + lis[items]  + "' />" + lis[items] + "<br>"
								
						}
						
						content += "</form>"
						content += "<p> </p>"
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
		
		if ($("#AutoSearchTextBoxLabel").text().trim() != "*Select Test Machine:") //If user is on select user page, do not allow him to delete the Test Data Set
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
			
			$("#SelectedEmail th").css('display', 'block');
			
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


var EmailIds = '';
var DependencyText = '';
var TestObjective = '';
var TestDataType = '';
function RunTestProcess() {

	$("#AutoSearchResult #searchedtext").each( function()
	{
		
		//Getting Test Data Set text
		var RunTestQuery = $(this).find("td").text();
		RunTestQuery = RunTestQuery.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
		
		//Getting Selected Email ids
		$("#AutoSearchResult #SelectedEmail").each( function() 
		{
			var Email= $(this).find("td").text();
			EmailIds = Email.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
		});
		
		//Getting Selected Dependency Text
		$("#AutoSearchResult #DependencyText").each( function() 
		{
			DependencyText= $(this).find("td").text();
			DependencyText = DependencyText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
		});
		
		//Getting Test Data Type Checkbox value
		TestDataType = $("#TestDataTypeCheckboxes input:checked").val()
		
		
		//Getting Test Objective text
		TestObjective =  $("input#TestObjective").val();
		if (TestObjective === "")
		{
			MsgBox("Test Run Error","Test Objective field is empty")
			
			$("input#TestObjective").effect("highlight", {}, 30000000);
			return
		}
		
		Env = Get_Selected_Env_Name()
		$.get("Run_Test", {RunTestQuery : RunTestQuery,EmailIds:EmailIds, DependencyText:DependencyText, TestDataType:TestDataType, TestObjective:TestObjective, Env: Env}, function(data) 
		{
			
			MsgBox("Test Run Response",	"Your Test Run Request Has Been Submitted, Here is the result :"+ data['Result']);
			// alert(data['Result']);

		});
		
	});
						
		//});
}



function Get_Selected_Env_Name()

{
	
	var St = $(".text[title='Choose']").text()
	if ( St.indexOf("Mac") !== -1 )
		{ Env = "Mac"}
	else
	   { Env = "PC" }
	return Env
		
}