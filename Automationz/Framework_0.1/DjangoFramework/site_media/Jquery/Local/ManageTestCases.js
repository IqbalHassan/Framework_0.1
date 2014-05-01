/**
 * Bismillahir Rahmanir Rahim, ALLAHU AKBAR
 * Author: Sazid
 */

$(document).ready(function() {
	
	// code for jstree --------------------

	var config_object = {
			"core": {
				"themes" : { "variant" : "large" },
				
				"data" : {
					"url" : function(node) {
						return "/Home/ManageTestCases";
					},
					
					"data" : function(node) {
						return { "id" : node.id };
					}
				},
				
				"check_callback": true
			},
			
			"types" : {
				"#" : {
					"valid_children" : [ "section" ]
				},
				
				"section" : {
					"icon" : "glyphicon glyphicon-list",
					"valid_children" : [ "section", "test_case" ]
				},
				
				"test_case" : {
					"valid_children" : []
				}
			},
			
			"plugins" : [ "search", "checkbox", "types", "wholerow" ]
	};
	
	$("#tree").jstree(config_object);
	
	$("#tree").on("changed.jstree", function(e, data) {
		var selected_sections = JSON.stringify(data.selected);
//		console.log(selected_sections);
		$(this).jstree(true).open_node(data.selected);
		
		$.get('/Home/ManageTestCases/getData/', { 'selected_section_ids': selected_sections }, function(data, status) {
			if (status === 'success') {
//				console.log(data);
				var query_string = data;
				loadTable(query_string);
			} else {
				alertify.error("Could not eastablish connection to the server.");
			}
		});
	});	
	
	
	function implementDropDown(wheretoplace){
	    $(wheretoplace+" tr td:nth-child(2)").css({'color' : 'blue','cursor' : 'pointer'});
	    $(wheretoplace+" tr td:nth-child(2)").each(function() {
	        var ID=$(this).closest('tr').find('td:nth-child(1)').text().trim();
	        var name=$(this).text().trim();
	        $(this).html('<div id="'+ID+'name">'+name+'</div><div id="'+ID+'detail" style="display:none;"></div>');
	        $.get("TestStepWithTypeInTable",{RunID: ID},function(data) {
	            var data_list=data['Result'];
	            var column=data['column'];
	            ResultTable('#'+ID+'detail',column,data_list,"");
	            $('#'+ID+'detail tr').each(function(){
	                $(this).css({'textAlign':'left'});
	            });
	        });
	        $(this).live('click',function(){
	            $('#'+ID+'detail').slideToggle("slow");
	        });
	    });
	}
	
	function loadTable(query_string) {
		$.get("TableDataTestCasesOtherPages", {'Query': query_string, 'test_status_request': true}, function(data) {

	        if (data['TableData'].length == 0)
	        {
	            $('#RunTestResultTable').children().remove();
	            $('#RunTestResultTable').append("<p class = 'Text' style=\"text-align: center;\">No Test Cases to view :(<br>It's either because you have not selected any section(s) or there are no test case(s) for the selected section(s).</p>");
	            $("#DepandencyCheckboxes").children().remove();
	        }
	        else
	        {
	            ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases");
	            
	            console.log(data['Heading']);
	            console.log(data['TableData']);

	            $("#RunTestResultTable").fadeIn(1000);
	            $("p:contains('Show/Hide Test Cases')").fadeIn(0);
	            implementDropDown("#RunTestResultTable");
	            // add edit btn
	            var indx = 0;
	            $('#RunTestResultTable tr>td:nth-child(5)').each(function(){
	                var ID = $("#RunTestResultTable tr>td:nth-child(1):eq("+indx+")").text().trim();

	                $(this).after('<img class="templateBtn buttonPic" id="'+ID+'" src="/site_media/copy.png" height="25"/>');
	                $(this).after('<img class="editBtn buttonPic" id="'+ID+'" src="/site_media/edit.png" height="25"/>');

	                indx++;
	            });

	            $(".editBtn").click(function (){
	                window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
	            });
	            $(".templateBtn").click(function (){
	                window.location = '/Home/ManageTestCases/CreateNew/'+ $(this).attr("id");
	            });
	            //VerifyQueryProcess();
	            //$(".Buttons[title='Verify Query']").fadeIn(2000);
	            $(".Buttons[title='Select User']").fadeOut();
	        }
	    });
	}
	
	
	// Handle button events
	$("#select_all_and_open_btn").click(function(e) {
		$("#tree").jstree(true).select_all();
		$("#tree").jstree(true).open_all();
	});
});
