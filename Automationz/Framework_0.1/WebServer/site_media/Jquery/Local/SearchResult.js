$(document).ready(
		function() {
			if (navigator.appName == "Microsoft Internet Explorer") {
				MsgBox("Browser", "Sorry! Internet Explorer is not supported")
			}

			// var URL = window.location.pathname
			// indx = URL.indexOf("Search")

			var Type = window.location.pathname.substring(window.location.pathname.lastIndexOf("/") + 3,
					window.location.pathname.length);
            //console.log(window.location.pathname.lastIndexOf("ID/") + 1);
            //console.log(window.location.pathname.length);
            //console.log("path:"+window.location.pathname);
            //console.log("Sub Path:"+Type.trim());
            /*var confirmation=window.location.pathname.substring(window.location.pathname.lastIndexOf("/") + 1,
                window.location.pathname.length);
            console.log(confirmation);*/
            console.log(Type);
            console.log(window.location.pathname.indexOf("RunID"));
			if (Type != "") {
				RunIdTestCases(Type)
				if (document.getElementById('LoadingText') != null)
					document.getElementById('LoadingText').style.display = 'None';
			} else {
                //console.log("index of runId:"+window.location.pathname.indexOf("RunID"));
				if (window.location.pathname.indexOf("RunID") != -1) {
					if (document.getElementById('LoadingText') != null)
						document.getElementById('LoadingText').innerHTML = "You must provide a RunID in the URL!";
				} else {
					var ResultRequest = "Search";
                    //console.log('ResultRequest:'+ResultRequest);
					Search_Result_Table(ResultRequest)
				}

		}
        }
            );

function Search_Result_Table(ResultRequest)

{
    //console.log("In search_result_table function:"+ResultRequest);
	$.get("Table_Data_TestResult", {
		ResultRequest : ResultRequest
	}, function(data) {
		if (data['TableData'].length == 0) {
			$('#Search_Result_Table').children().remove();
			$('#Search_Result_Table').append('<p><b>Sorry There is No Test Cases For Selected Query!!!</b></p>');
		} else {

			// $("#Search_Result_Table").append("<p class='flip' '
			// style='display: block'>Show All</p>")
			ResultTable('#Search_Result_Table', data['Heading'], data['TableData'], "Test Results Shown");
			$('#LoadingText').css({
				"display" : "none"
			});
			$("<p class='flip' title = 'Show All' style='display: block'>Show All</p>").insertBefore(
					"#Search_Result_Table")
		}

		// If user click on "Show All" button
		$("p.flip[title =  'Show All']").click(
				function() {

					ResultRequest = "Show All"
					$('#Search_Result_Table').children().remove();
					$("p.flip[title =  'Show All']").remove()
					$('#LoadingText').css({
						"display" : "block"
					});

					$.get("Table_Data_TestResult", {
						ResultRequest : ResultRequest
					}, function(data) {
						if (data['TableData'].length == 0) {
							$('#Search_Result_Table').children().remove();
							$('#Search_Result_Table').append(
									'<p><b>Sorry There is No Test Cases For Selected Query!!!</b></p>');
						} else {

							ResultTable('#Search_Result_Table', data['Heading'], data['TableData'],
									"Test Results Shown");
							$('#LoadingText').css({
								"display" : "none"
							});

						}

						Make_RunID_Clickable()
					});
				});

		Make_RunID_Clickable()

	});

}

function Make_RunID_Clickable()

{

	$(".ui-widget tr td:first-child").css({
		'color' : 'blue',
		'cursor' : 'pointer'
	});
	$(".ui-widget tr>td:nth-child(12)").each(function() {

		if ($(this).text() === "null") {
			$(this).text("SV&V");
		}
	});

	$(".ui-widget tr td:first-child").click(function() {

		$("p.flip[title =  'Show All']").remove()
        //console.log("children:"+$(this).children().text());
		$(this).children().slideToggle("slow");
		ClickedRunId = $(this).text();
        //console.log("clicked runId:"+ClickedRunId);
		var $TC = $(this).text();
        //console.log("$TC:"+$TC);
		var TestSteps;

		$(".ui-widget tr td:first-child").each(function() {
			$(this).unbind('click');
		});
        var location='/Home/RunID/'+ClickedRunId+'/';
        console.log(location);
        window.location=location;
		//RunIdTestCases(ClickedRunId); // Look in JQuery.js for this function
	});

}

function WhenClickingOnCommonFailedTestStep() {
	$("#FailedStepsTable tr>td:nth-child(1)").css({
		'color' : 'blue',
		'cursor' : 'pointer'
	});

	$("#FailedStepsTable tr td:first-child")
			.each(
					function() {
						$(this)
								.live(
										'click',
										function() {
											var RunID = $("#EnvironmentDetailsTable tr td:first-child").text()
											var FailedStepWithCount = $(this).text()
											var FailedStep = FailedStepWithCount.split("(")[0]
											var This = $(this)

											$
													.get(
															"FailStep_TestCases",
															{
																RunID : RunID,
																FailedStep : FailedStep
															},
															function(data) {
																var TableData = data['FailStep_TestCases']
																var TableCol = data['FailStep_TC_Col']

																$("#FailedStepsTable tr>td:nth-child(1)")
																		.each(
																				function() {

																					if ($(This).text() == FailedStepWithCount) {

																						var ID = FailedStep.replace(
																								/ /g, '').replace("-",
																								'');
																						$(This).append(
																								"<div style='display: none; margin-left:10px ' id='"
																										+ ID
																										+ "'> </div>");

																						ResultTable('#' + ID, TableCol,
																								TableData, "");

																						// Making
																						// Log
																						// file
																						// link
																						// (
																						// 2nd
																						// Last
																						// column
																						// of
																						// failed
																						// test
																						// cases
																						// table)
																						$(
																								'#'
																										+ ID
																										+ ' tr>td:nth-child(6)')
																								.each(
																										function() {

																											logPath = $(
																													this)
																													.text();
																											$(this)
																													.html(
																															"<a href ='file:///"
																																	+ logPath
																																	+ "'>Log File</a>");

																										});

																						// Making
																						// MKS
																						// link
																						// to
																						// MKS
																						// ID
																						$(
																								'#'
																										+ ID
																										+ ' tr>td:nth-child(1)')
																								.each(
																										function() {

																											MKS_ID = $(
																													this)
																													.text();
																											if (MKS_ID != "") {
																												$(this)
																														.html(
																																"<a target='_blank' href ='http://mksintegrity:7001/im/issues?selection="
																																		+ MKS_ID
																																		+ "' > "
																																		+ MKS_ID
																																		+ " </a>");

																											}

																										});

																						$(
																								'#'
																										+ ID
																										+ ' tr>td:nth-child(6)')
																								.css(
																										{
																											'color' : 'blue',
																											'cursor' : 'pointer'
																										});
																						$("#" + ID).slideToggle("slow");

																						// When
																						// User
																						// Click
																						// on
																						// fail
																						// test
																						// case
																						// (
																						// first
																						// column
																						// of
																						// table
																						// under
																						// Fail
																						// Step
																						// Name)
																						$(
																								'#'
																										+ ID
																										+ ' tr>td:nth-child(2)')
																								.each(
																										function() {
																											var ID = $(
																													this)
																													.text()
																													.replace(
																															/ /g,
																															'0');
																											$(this)
																													.attr(
																															'id',
																															ID);
																											$(this)
																													.css(
																															{
																																'display' : 'block'
																															});

																										});

																						$(
																								'#'
																										+ ID
																										+ ' tr>td:nth-child(2)')
																								.each(
																										function() {

																											$(this)
																													.live(
																															'click',
																															function(
																																	e) {

																																var TestCaseName = $(
																																		this)
																																		.text()
																																var RunID = $(
																																		"#EnvironmentDetailsTable tr td:first-child")
																																		.text()
																																var ClickedItemId = $(
																																		this)
																																		.attr(
																																				'id');
																																$(
																																		this)
																																		.children()
																																		.slideToggle(
																																				"slow");

																																$
																																		.get(
																																				"TestCase_Detail_Table",
																																				{
																																					RunID : RunID,
																																					TestCaseName : TestCaseName
																																				},
																																				function(
																																						data) {

																																					if (data['TestCase_Detail_Data'].length != 0) {
																																						ResultTable(
																																								'#'
																																										+ ClickedItemId,
																																								data['TestCase_Detail_Col'],
																																								data['TestCase_Detail_Data'],
																																								"");
																																						$(
																																								'#'
																																										+ ClickedItemId
																																										+ ' table')
																																								.css(
																																										{
																																											'margin-left' : '20px'
																																										});
																																						$(
																																								'#'
																																										+ ClickedItemId
																																										+ ' tr>td:nth-child(2)')
																																								.css(
																																										{
																																											'color' : 'blue',
																																											'cursor' : 'pointer'
																																										});

																																						// Show
																																						// Test
																																						// Step
																																						// Details
																																						// table
																																						// when
																																						// user
																																						// click
																																						// on
																																						// Test
																																						// Step
																																						// Name

																																						TestCaseDetailTable(
																																								ClickedItemId,
																																								TestCaseName);

																																					}
																																				});

																																e
																																		.stopPropagation();

																															});
																										});

																					}

																				});

															});

										});

					});

}
//count=0;
function TestCase_TestStep_Details_Table(sMainTableColumn) {
    console.log(sMainTableColumn);
	$(sMainTableColumn).css({
		'color' : 'blue',
		'cursor' : 'pointer'
	});
	$(sMainTableColumn).each(function() {
        //count=count+1;
        //console.log("Cycle:"+count);
        //console.log("Text:"+$(this).text());
		var ID = $(this).text().replace(/ /g, '').replace(/,/g, '');
        //console.log("ID:"+ID);
		ID = ID.replace("(", "").replace(")", "").replace("&", "");
		if (sMainTableColumn.search("PassTestCasesTable") == 1) {
			ID = "Pass" + ID
            //console.log(ID);
		}
		if (sMainTableColumn.search("FailTestCasesTable") == 1) {
			ID = "Fail" + ID
		}
		$(this).append("<div style='display: none;' id='" + ID + "'> </div>");
	});

	$(sMainTableColumn).each(
			function() {

				$(this).live(
						'click',
						function() {
                            //console.log("Before:"+$(this).text());
							var TestCaseName = $(this).text().split("Test Step Name")[0];
                            //console.log("After:"+TestCaseName);
							var TestCaseId = $(this).closest('tr').find('td:nth-child(7)').text();
							var RunID = $("#EnvironmentDetailsTable tr td:first-child").text();
							$(this).children().slideToggle("slow");

							$.get("TestCase_Detail_Table/", {
								RunID : RunID,
								TestCaseName : TestCaseId
							}, function(data) {

								// Show Step Name table when user click on Test
								// case name
								$(sMainTableColumn)
										.each(
												function() {

													if ($(this).text().replace("(", "").replace(")", "").replace("&",
															"") == TestCaseName.replace("(", "").replace(")", "")
															.replace("&", "")) {
														// var ID = TestCaseId;
														var ID = $(this).text().replace(/ /g, '').replace(/,/g, "");

														ID = ID.replace("(", "").replace(")", "").replace("&", "");

														if (sMainTableColumn.search("PassTestCasesTable") == 1) {
															ID = "Pass" + ID
														}
														if (sMainTableColumn.search("FailTestCasesTable") == 1) {
															ID = "Fail" + ID
														}

														ResultTable('#' + ID, data['TestCase_Detail_Col'],
																data['TestCase_Detail_Data'], "");
														$('#' + ID + ' table').css({
															'margin-left' : '20px'
														});
														$('#' + ID + ' tr td:first-child').css({
															'color' : 'blue',
															'cursor' : 'pointer'
														});
														// Show Test Step
														// Details table when
														// user click on Test
														// Step Name
														TestCaseDetailTable(ID, TestCaseName);
													}

												});

							});

						});

			});
}

function TestCaseDetailTable(TableID, TestCaseName) {

	$("#" + TableID + " tr td:first-child").each(function() {

		$(this).live('click', function(i) {
			$("#" + TableID).append("<div id = 'TestStep_Details' title='" + $(this).text() + "'>" +
                "<div id='' title='Execution Log'>" +
                    "<div id='TestStep_ExecutionLog_Header' style='margin-bottom: 10px;'>" +
                    "</div>" +
                    "<div id='TestStep_ExecutionLog'>" +
                    "</div>" +
                "</div>" +
                "<hr>" +
                "<div id='' title='Step Data and Info'>" +
                    "<div id='TestStep_InfoData_Header' style='margin-bottom: 10px;'>" +
                    "</div>" +
                    "<div id='TestStep_InfoData'>" +
                    "</div>"+
                "</div>" +
                "<hr>" +
                "<div id=''>" +
                    "<div id='Data_Header' style='margin-bottom: 10px;'>"+
                    "</div>" +
                    "<div id='Data' align='center'>" +
                    "</div>" +
                "</div>"+
			"</div>");
			var RunID = $("#EnvironmentDetailsTable tr td:first-child").text();
			var TestStepName = $(this).text();
			var TestStepSeqID = ($(this).parent().parent().children().index($(this).parent()));

			$.get("TestStep_Detail_Table/", {
				RunID : RunID,
				TestCaseName : TestCaseName,
				TestStepName : TestStepName,
				TestStepSeqID : TestStepSeqID
			}, function(data) {

				// alert(data['TestCaseName']);
				var TestStep_Table = data['TestStep_Details']
				var TestStep_Col = data['TestStep_Col']
                ResultTable("#TestStep_ExecutionLog_Header",["Execution Log"],"","");
				ResultTable('#TestStep_ExecutionLog', data['TestStep_Col'], TestStep_Table, "");
				ResultTable('#TestStep_InfoData_Header',["Description"], "", "");
				ResultTable('#TestStep_InfoData',data['TestStep_Description_Col'], data['TestStep_Description'], "");
				ResultTable('#Data_Header', ["Data"], "", "");
                if(data['data_required']=="no"){
                    $("#Data").html("");
                    $("#Data").html("<b>Data is not required for this step</b>")
                }
                if(data['data_required']=="yes"){
                    console.log(data['data_val_comp']);
                    $("#Data").html("");
                    ResultTable('#Data',data['data_col'],data['data_val'], "");
                    /*console.log(data['data_val_comp']);
                    var currentrow=$("#Data tr:nth-child(2)");
                    console.log(currentrow.text());
                    for(var i=0;i<data['data_set_count'];i++){
                        //var temp=currentrow.find("td:nth-child(2)");
                        ResultTable('#Data tr:nth-child('+(i+2)+')>td:nth-child(2)',['Field','value'],data['data_val_comp'][i],"");
                        //currentrow+=currentrow.next("tr");
                        //console.log(currentrow.text());
                    }
                    //ResultTable('#Data tr>td:nth-child(2)',['Field','value'],data['data_val_comp'][0],"");*/
                    for(var i=0;i<data['data_val'].length;i++){
                        var col= "row"+(i+2)+"col"+(i+2);
                        $('#Data tr:nth-child('+(i+2)+')>td:nth-child(2)').attr({'id':col});
                    }
                    var dataset=data['data_val_comp'];
                    for(var i=0;i<dataset.length;i++){
                        var col= "#row"+(i+2)+"col"+(i+2);
                        console.log(col);
                        console.log(dataset[i]);
                        ResultTable(col,["Field","Value"],dataset[i],"");
                    }
                }

				$("#TestStep_Details").dialog({
					buttons : {
						"OK" : function() {
							$(this).dialog("close");
						}
					},

					show : {
						effect : 'drop',
						direction : "up"
					},

					modal : true,
					width : 600,
					height : 780,

				});

			});
			i.stopPropagation();

		});
	});

}