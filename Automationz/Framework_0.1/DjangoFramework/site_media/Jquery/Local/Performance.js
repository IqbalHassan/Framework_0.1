$(document).ready(function() {

	var URL = window.location.pathname
	indx = URL.indexOf("Performance")
	if (indx != -1) {

		Performance()

	}

});

function Performance() {
	var PerformanceResultRequesting = ""
	$.get("PerformanceResult", {
		PerformanceResultRequest : PerformanceResultRequesting
	}, function(data) {

		if (data['Environments'].length == 0) {
			$('#Performance').append(
					'<p class = "Text" ><b>Sorry There is no performance result data available!!!</b></p>');
		} else {
			// Removing Loading text when data is loaded
			$('#LoadingText').remove();

			for (Cat in data['Categories']) {
				// Replacing comma and space from environment
				// array
				var curr_category = data['Categories'][Cat]

				$('div#FlipBar').append(

						"<p  id = '" + curr_category + "'class='flip' style = 'display:block;width:50%'>"
								+ curr_category + "</p>")

				var all_cat_envs = new Array();

				for (Env in data['Environments']) {
					if (data['Environments'][Env][3] != curr_category)
						continue;

					// Replacing comma and space from environment
					// array
					var EnvString = '';
					for ( var i = 0; i < data['Environments'][Env].length - 1; i++) {
						Envstr = data['Environments'][Env][i].replace(/,/g, "_").replace(/ /g, "").replace(/-/g, "");
						EnvString += Envstr
					}

					var ID = $.trim(EnvString);
					$('div#FlipBar').append(

							"<p  id = '" + ID + "_Environment_Flip_Bar_"+curr_category
									+ "'class='flip lower' style = 'display:none;width:30%'>"
									+ data['Environments'][Env][0] + "," + data['Environments'][Env][1] + ","
									+ data['Environments'][Env][2] + "</p>"

									/* DURATION */
									+ "<p  id = '" + ID + "_Duration_Table_Flip"
									+ "'class='flip xlower' style = 'width:10%'>" + "Duration Table" + "</p>"
									+ "<div id='" + ID + "_Duration_Table" + "'style='display: none'>" + "</div>"
									
									/* GRAPH Duration */
									+ "<p  id = '" + ID + "_Duration_Table_Flip_Graph_Flip" + "'class='flip xlower' style = 'width:10%'>"
									+ "Duration Graph Report" + "</p>"

									+ "<div id='" + ID + "_Graph_Table" + "'style='display: none'>" + "</div>"
									
									/* MEMORY */
									+ "<p  id = '" + ID + "_Memory_Table_Flip"
									+ "'class='flip xlower' style = 'width:10%'>" + "Memory Table" + "</p>"
									+ "<div id='" + ID + "_Memory_Table" + "'style='display: none'>" + "</div>"
									
									/* GRAPH Memory */
									+ "<p  id = '" + ID + "_Memory_Table_Flip_Graph_Flip" + "'class='flip xlower' style = 'width:10%'>"
									+ "Memory Graph Report" + "</p>"

									+ "<div id='" + ID + "_Graph_Table" + "'style='display: none'>" + "</div>"
									
									/* CPU */
									+ "<p  id = '" + ID + "_CPU_Table_Flip"
									+ "'class='flip xlower' style = 'width:10%'>" + "CPU Table" + "</p>"
									+ "<div id='" + ID + "_CPU_Table" + "'style='display: none'>" + "</div>"
									
									/* GRAPH Cpu */
									+ "<p  id = '" + ID + "_CPU_Table_Flip_Graph_Flip" + "'class='flip xlower' style = 'width:10%'>"
									+ "CPU Graph Report" + "</p>"

									+ "<div id='" + ID + "_Graph_Table" + "'style='display: none'>" + "</div>"

					)
					$('#' + ID + "_Duration_Table_Flip").data('category', curr_category);
					$('#' + ID + "_Memory_Table_Flip").data('category', curr_category);
					$('#' + ID + "_CPU_Table_Flip").data('category', curr_category);
					$('#' + ID + "_Duration_Table_Flip_Graph_Flip").data('category', curr_category);
					$('#' + ID + "_Memory_Table_Flip_Graph_Flip").data('category', curr_category);
					$('#' + ID + "_CPU_Table_Flip_Graph_Flip").data('category', curr_category);
					all_cat_envs[Env] = ID + "_Environment_Flip_Bar_"+curr_category;
				}

				$('#' + curr_category).data('Environments', all_cat_envs);
			}
		}
		Click_Category_Flip_Bar(data['Categories']);

	});

}
function Click_Category_Flip_Bar(cat_list) {
	for (cat in cat_list) {
		$("p#" + cat_list[cat] + ".flip").each(function() {
			$(this).live('click', function() {

				var ID = $(this).text();
				var all_cat_envs = $('#' + ID).data('Environments');

				for (env in all_cat_envs) {
					$("#" + all_cat_envs[env]).slideToggle("slow");

					Click_Environment_Flip_Bar(all_cat_envs[env]);
				}
			});

		});
	}
}

function Click_Environment_Flip_Bar(env_name) {

	$("p#" + env_name + ".flip").each(function() {
		$(this).live('click', function() {

			var PerformanceResultRequest = $(this).text();
			// Replacing comma and space from environment array
			var ID = PerformanceResultRequest.replace(/,/g, "").replace(/ /g, "").replace(/-/g, "");

			// Getting Duration/MemoryTable ids
			var DurationTable = "#" + ID + "_Duration_Table"
			var MemoryTable = "#" + ID + "_Memory_Table"
			var CPUTable = "#" + ID + "_CPU_Table"
			var DurationGraphTable = "#" + ID + "_Duration_Table_Graph_Table"
			var MemoryGraphTable = "#" + ID + "_Memory_Table_Graph_Table"
			var CPUGraphTable = "#" + ID + "_CPU_Table_Graph_Table"

			// Getting Duration/MemoryTableFlip bar ids
			var DurationTableFlip = "#" + ID + "_Duration_Table_Flip"
			var MemoryTableFlip = "#" + ID + "_Memory_Table_Flip"
			var CPUTableFlip = "#" + ID + "_CPU_Table_Flip"
			var DurationGraphFlip = "#" + ID + "_Duration_Table_Flip_Graph_Flip"
			var MemoryGraphFlip = "#" + ID + "_Memory_Table_Flip_Graph_Flip"
			var CPUGraphFlip = "#" + ID + "_CPU_Table_Flip_Graph_Flip"

			$(DurationTableFlip).slideToggle("slow");
			$(MemoryTableFlip).slideToggle("slow");
			$(CPUTableFlip).slideToggle("slow");
			$(DurationGraphFlip).slideToggle("slow");
			$(MemoryGraphFlip).slideToggle("slow");
			$(CPUGraphFlip).slideToggle("slow");
			
			// Calling Functions When use click on any of three
			// flip bars (Duration, Memory, Graph)
			Click_DurationTable_Flip_Bar(DurationTableFlip, DurationTable, PerformanceResultRequest)
			Click_MemoryTable_Flip_Bar(MemoryTableFlip, MemoryTable, PerformanceResultRequest)
			Click_CPUTable_Flip_Bar(CPUTableFlip, CPUTable, PerformanceResultRequest)
			
			Click_DurationGraphTable_Flip_Bar(DurationGraphFlip, DurationGraphTable, PerformanceResultRequest)
			Click_MemoryGraphTable_Flip_Bar(MemoryGraphFlip, MemoryGraphTable, PerformanceResultRequest)
			Click_CPUGraphTable_Flip_Bar(CPUGraphFlip, CPUGraphTable, PerformanceResultRequest)
		});

	});

}

function Click_DurationTable_Flip_Bar(DurationTableFlip, DurationTable, PerformanceResultRequest) {

	$(DurationTableFlip).each(function() {
		$(this).live('click', function() {
			$.get("PerformanceResult", {
				PerformanceResultRequest : PerformanceResultRequest,
				'category':$(DurationTableFlip).data('category')
			}, function(data) {

				ResultTable(DurationTable, data['Heading'], data['DurationTable'], "Performance Duration Test Result");

				$(".ui-widget tr td:not(:first-child)").css({
					'color' : 'skyblue',
					'cursor' : 'pointer',
					'text-decoration' : 'underline',
					'text-align' : 'center',
					'line-height' : '200%'
				});
				$(".ui-widget tr>td:nth-child(2)").css({
					'color' : '#D9D9D9',
					'cursor' : 'text',
					'text-decoration' : 'none',
					'text-align' : 'left'
				});

				$(DurationTable).slideToggle("slow");

				ClickBundlesDuration(DurationTable, PerformanceResultRequest);
			});

		});

	});

}

function Click_MemoryTable_Flip_Bar(MemoryTableFlip, MemoryTable, PerformanceResultRequest) {

	$(MemoryTableFlip).each(function() {
		$(this).live('click', function() {

			$.get("PerformanceResult", {
				PerformanceResultRequest : PerformanceResultRequest,
				'category':$(MemoryTableFlip).data('category')
			}, function(data) {
				ResultTable(MemoryTable, data['Heading'], data['MemoryTable'], "Performance Memory Test Result");

				$(".ui-widget tr td:not(:first-child)").css({
					'color' : 'skyblue',
					'cursor' : 'pointer'
				});
				$(".ui-widget tr>td:nth-child(2)").css({
					'color' : '#D9D9D9',
					'cursor' : 'text'
				});

				$(MemoryTable).slideToggle("slow");

				ClickBundlesMemory(MemoryTable, PerformanceResultRequest);
			});

		});

	});

}

function Click_CPUTable_Flip_Bar(CPUTableFlip, CPUTable, PerformanceResultRequest) {

	$(CPUTableFlip).each(function() {
		$(this).live('click', function() {

			$.get("PerformanceResult", {
				PerformanceResultRequest : PerformanceResultRequest,
				'category':$(CPUTableFlip).data('category')
			}, function(data) {
				ResultTable(CPUTable, data['Heading'], data['CPUTable'], "Performance CPU Test Result");

				$(".ui-widget tr td:not(:first-child)").css({
					'color' : 'skyblue',
					'cursor' : 'pointer'
				});
				$(".ui-widget tr>td:nth-child(2)").css({
					'color' : '#D9D9D9',
					'cursor' : 'text'
				});

				$(CPUTable).slideToggle("slow");

				ClickBundlesCPU(CPUTable, PerformanceResultRequest);
			});

		});

	});

}

function Click_DurationGraphTable_Flip_Bar(DurationGraphFlip, DurationGraphTable, PerformanceResultRequest) {
	$(DurationGraphFlip).each(
			function() {
				$(this).live(
						'click',
						function(i) {

							$(this).text("Loading...");

							$(this).css({
								"cursor" : "progress"
							});
							
							$.get("PerformanceResult", {
								PerformanceResultRequest : PerformanceResultRequest,
								GraphRequest : "Graph",
								'category':$(DurationGraphFlip).data('category'),
								'type':"Duration"
							}, function(data) {

								// var NWin =
								// window.open(('/Home/PerformanceGraph_Window/'),
								// '',
								// 'height=800,width=800');

								$(DurationGraphTable).children().remove();

								var content = '';

								if (data['GraphPathList'] != '') {
									content += "<p class = 'Text' style=' color:skyblue; font-size:12px'><b>"
											+ data['GraphPathList'].length + " Graphs Found" + "</b></p>"
								}

								content += "<table width='100%'  border='0'>";

								items = []
								for ( var i = 0; i < data['GraphPathList'].length; i = i + 3) {

									content += '<tr>';

									content += "<td> " + "<img src= ' " + data['GraphPathList'][i]
											+ "' width='400' height='317' > " + "</td>";

									content += "<td> " + "<img src= ' " + data['GraphPathList'][i + 1]
											+ "' width='400' height='317' > " + "</td>";

									content += "<td> " + "<img src= ' " + data['GraphPathList'][i + 2]
											+ "' width='400' height='317' > " + "</td>";

									content += '<tr>';

								}

								content += '</table>';
								$(GraphTable).append(content);

								$("img[src=' undefined']").remove();

								$(DurationGraphFlip).text("Graph Report")
								$(DurationGraphFlip).css({
									"cursor" : "pointer"
								});
								$(DurationGraphFlip).css({
									"cursor" : "hand"
								});

								$(GraphTable).dialog({
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
									width : 1250,
									height : 1000,

								});

								// ResultTable(GraphTable,data['Heading'],data['GraphPathList'],"Performance
								// Graph Test
								// Result");
								// $(GraphTable).slideToggle("slow");

							});

							// i.stopPropagation();

						});

			});

}

function ClickBundlesDuration(Environment, PerformanceResultRequest){

	$(Environment + " tr>td:not(:nth-child(1))").each(
			function() {

				$(this).live(
						'click',
						function() {

							if ($(this).text().indexOf("-") < 0) {
								// Finding Bundle Name of
								// clicked cell
								var col = ($(this).parent().children().index($(this)));
								var BundleNumber = $(this).closest("table").find("th").eq(col).text();

								// Finding Test Case Number of
								// clicked cell
								var TestCaseName = $(this).closest('tr').find('td:nth-child(2)').text();
								var TestCaseNumber = $(this).closest('tr').find('td:nth-child(1)').text();

								$(Environment).append(
										"<div id = 'DurationTestCase_Details' title='" + TestCaseName + "("
												+ BundleNumber + ")" + "'>" +

												"</div>");

								// Calling function to get the
								// detail of bundle duration
								// test cases
								$.get("Performance_ClickedBundle_Details_D", {
									PerformanceResultRequest : PerformanceResultRequest,
									BundleNumber : BundleNumber,
									TestCaseNumber : TestCaseNumber
								}, function(data) {

									ResultTable("#DurationTestCase_Details", data['Heading'],
											data['Performance_TestCase_Duration_Table'],
											"Performance Duration Test Result");

									$("#DurationTestCase_Details tr>td:nth-child(6)").each(function() {

										logPath = $(this).text();
										if (logPath != "") {
											$(this).html("<a href ='file:///" + logPath + "'>Log File</a>");
										}

									});

									$("#DurationTestCase_Details").dialog({
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
										height : 600,

									});

								});
							}

						});
			});

}
function ClickBundlesMemory(Environment, PerformanceResultRequest){

	$(Environment + " tr>td:not(:nth-child(1))").each(
			function() {

				$(this).live(
						'click',
						function() {

							if ($(this).text().indexOf("-") < 0) {
								// Finding Bundle Name of
								// clicked cell
								var col = ($(this).parent().children().index($(this)));
								var BundleNumber = $(this).closest("table").find("th").eq(col).text();

								// Finding Test Case Number of
								// clicked cell
								var TestCaseName = $(this).closest('tr').find('td:nth-child(2)').text();
								var TestCaseNumber = $(this).closest('tr').find('td:nth-child(1)').text();

								$(Environment).append(
										"<div id = 'DurationTestCase_Details' title='" + TestCaseName + "("
												+ BundleNumber + ")" + "'>" +

												"</div>");

								// Calling function to get the
								// detail of bundle duration
								// test cases
								$.get("Performance_ClickedBundle_Details_M", {
									PerformanceResultRequest : PerformanceResultRequest,
									BundleNumber : BundleNumber,
									TestCaseNumber : TestCaseNumber
								}, function(data) {

									ResultTable("#DurationTestCase_Details", data['Heading'],
											data['Performance_TestCase_Duration_Table'],
											"Performance Duration Test Result");

									$("#DurationTestCase_Details tr>td:nth-child(6)").each(function() {

										logPath = $(this).text();
										if (logPath != "") {
											$(this).html("<a href ='file:///" + logPath + "'>Log File</a>");
										}

									});

									$("#DurationTestCase_Details").dialog({
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
										width : 900,
										height : 600,

									});

								});
							}

						});
			});

}
function ClickBundlesCPU(Environment, PerformanceResultRequest){

	$(Environment + " tr>td:not(:nth-child(1))").each(
			function() {

				$(this).live(
						'click',
						function() {

							if ($(this).text().indexOf("-") < 0) {
								// Finding Bundle Name of
								// clicked cell
								var col = ($(this).parent().children().index($(this)));
								var BundleNumber = $(this).closest("table").find("th").eq(col).text();

								// Finding Test Case Number of
								// clicked cell
								var TestCaseName = $(this).closest('tr').find('td:nth-child(2)').text();
								var TestCaseNumber = $(this).closest('tr').find('td:nth-child(1)').text();

								$(Environment).append(
										"<div id = 'DurationTestCase_Details' title='" + TestCaseName + "("
												+ BundleNumber + ")" + "'>" +

												"</div>");

								// Calling function to get the
								// detail of bundle duration
								// test cases
								$.get("Performance_ClickedBundle_Details_C", {
									PerformanceResultRequest : PerformanceResultRequest,
									BundleNumber : BundleNumber,
									TestCaseNumber : TestCaseNumber
								}, function(data) {

									ResultTable("#DurationTestCase_Details", data['Heading'],
											data['Performance_TestCase_Duration_Table'],
											"Performance Duration Test Result");

									$("#DurationTestCase_Details tr>td:nth-child(7)").each(function() {

										logPath = $(this).text();
										if (logPath != "") {
											$(this).html("<a href ='file:///" + logPath + "'>Log File</a>");
										}

									});

									$("#DurationTestCase_Details").dialog({
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
										height : 600,

									});

								});
							}

						});
			});

}
