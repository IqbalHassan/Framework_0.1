$(document).ready(function(){
	var Env = "PC"
	var URL = window.location.pathname
	indx = URL.indexOf("Run")

			AddAutoCompleteSearchBox("#Place_AutoComplete_Here","Search Test Cases Data By Keywords:");
			
			AvailebableTestMachineflipButton("PC");
			RunTestAutocompleteSearch("PC");
			
			
			// Calling DeleteSearchQueryText for Deleting query text after clicking on delete button
				DeleteSearchQueryText();
			
			
			// On Clicking Auto Complete Search Button, Send Query Text to View.py > AjaxData function
			$(".Buttons[title='Search Test Cases']").click(function(){ 
				
				if ($("#AutoSearchTextBoxLabel").text() != "Search User:")
				{
					PerformSearch();
				}
				
			});
	
});


 var DepandencyNameList = [];

function AddAutoCompleteSearchBox(WhereToPlaceId, Label)
{	
	
	$(WhereToPlaceId).append(


        "<form method = 'get' >"

            +"<table id='AutoSearchResult' style='display: block;' >"
                + "<tbody>"

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
		$("#AvailableTestMachine .ui-widget th:nth-child(1), .ui-widget td:nth-child(1)").remove()
		$("#AvailableTestMachine .ui-widget th:nth-child(2), .ui-widget td:nth-child(2)").remove()
		$("#AvailableTestMachine .ui-widget th:nth-child(3), .ui-widget td:nth-child(3)").remove()
		$("#AvailableTestMachine .ui-widget th:nth-child(6), .ui-widget td:nth-child(6)").remove()
		$("#AvailableTestMachine .ui-widget th:nth-child(9), .ui-widget td:nth-child(9)").remove()
		$("#AvailableTestMachine .ui-widget th:nth-child(12), .ui-widget td:nth-child(12)").remove()
		$("#AvailableTestMachine .ui-widget th:nth-child(15), .ui-widget td:nth-child(15)").remove()
		$("#AvailableTestMachine .ui-widget th:nth-child(16), .ui-widget td:nth-child(16)").remove()
		
		
		
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

						if(value != "")
						{

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
							return false;
						},

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

												$("#RunTestResultTable").fadeIn(1000);
												$("p:contains('Show/Hide Test Cases')").fadeIn(0);	
												implementDropDown("#RunTestResultTable");
												// add edit btn
												var indx = 0;
												$('#RunTestResultTable tr>td:nth-child(3)').each(function(){
													var ID = $("#RunTestResultTable tr>td:nth-child(1):eq("+indx+")").text().trim();
													
													$(this).after('<img class="templateBtn buttonCustom" id="'+ID+'" src="/site_media/template.png" height="50"/>');
													$(this).after('<img class="editBtn buttonCustom" id="'+ID+'" src="/site_media/edit_case.png" height="50"/>');
												
													indx++;
												});

												$(".editBtn").click(function (){
													window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
												});
												$(".templateBtn").click(function (){
													window.location = '/Home/ManageTestCases/Create/'+ $(this).attr("id");
												});
												VerifyQueryProcess();
												//$(".Buttons[title='Verify Query']").fadeIn(2000);
												$(".Buttons[title='Select User']").fadeOut();
											}

										});

					});

}
function implementDropDown(wheretoplace){
    $(wheretoplace+" tr td:nth-child(2)").css({'color' : '#000066','cursor' : 'pointer'});
    $(wheretoplace+" tr td:nth-child(2)").each(function() {
        $(this).live('click',function() {

            var childrenCount = $(this).children().length
            if (childrenCount == 0)
            {
                $(this).children().slideDown();
            }
            else
            {
                $(this).children().slideUp();
                //childrenCount=0;
                $(this).children().remove();
                return;
            }
            var ClickedTC = $(this).text();
            var RunID = $(this).closest('tr').find('td:nth-child(1)').text();
            RunID = RunID.trim();

            var $TC = $(this).text();
            var TestSteps;
            $.get("TestStepWithTypeInTable",{ClickedTC : ClickedTC,RunID: RunID},function(data) {
                TestSteps = data['Result'];

                $(".ui-widget tr td:nth-child(2)").each(function() {
                    //if (($(this).text()) == ClickedTC)
                    if($(this).closest('tr').find('td:nth-child(1)').text()==RunID)
                    {

                        $(this).children().remove();
                        for (eachitem in data['Result'])
                        {

                            $($(this)).append("<p id = 'TestCase_Steps'>"+ data['Result'][eachitem]																																				+ "</p>");
                        }

                    }

                    $("p#TestCase_Steps").css({'color' : '#9999FF','cursor' : 'text'});
                });

            });
            //$(this).children().slideToggle();

        });
    });
}

