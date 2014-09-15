/**
 * Bismillahir Rahmanir Rahim, ALLAHU AKBAR
 * Author: Sazid
 */

$(document).ready(function() {
	
	window.section_has_no_tc = true;
	
	// code for jstree --------------------

	var config_object = {
			"core": {
				"themes" : { "variant" : "large" },
				
				"data" : {
					"url" : function(node) {
						return "/Home/ManageTestCases";
					},
					
					"data" : function(node) {
						return {
                            "id" : node.id,
                            "project_id": $.session.get('project_id'),
                            "team_id": $.session.get('default_team_identity')
                        };
					}
				},
				
				"check_callback": true
			},
			
			"types" : {
				"#" : {
					"valid_children" : [ "parent_section" ]
				},
				
				"parent_section" : {
					"icon" : "fa fa-folder fa-lg fa-fw",
					"valid_children" : [ "section" ]
				},
				
				"section" : {
					"icon" : "fa fa-folder fa-fw fa-lg",
					"valid_children" : [ "section" ]
				}
			},
			
			"contextmenu" : {
				"items" : function(node) {
					return {
						"Create" : {
							"separator_before": false,
							"separator_after": false,
							"label": "Create Section",
							"icon": "fa fa-plus",
							"action": function(obj) {
								try {
									var x = node.text.split('<span style="display:none;">');
									var y = x[1].split("</span>");
									createNode(y[0] + ".");
								} catch (TypeError) {
									createNode(node.text + ".");
								}
							}
						},
						"Rename" : {
							"separator_before": false,
							"separator_after": false,
							"label": "Rename Section",
							"icon": "fa fa-edit",
							"action": function(obj) {
								renameNode(node, node.id);
							}
						},
						"Delete" : {
							"separator_before": true,
							"separator_after": false,
							"icon": "fa fa-trash-o",
							"label": "Delete Section",
							"action": function(obj) {
								deleteNode(node);
							}
						}
					}
				}
			},
			
			"checkbox" : {
				"keep_selected_style": false
			},
			
			"plugins" : [ "search", "checkbox", "types", "wholerow", "contextmenu", "sort" ]
	};
	
	$("#tree").jstree(config_object)
	.on("changed.jstree", function(e, data) {
		var selected_sections = JSON.stringify(data.selected);
		$(this).jstree(true).open_node(data.selected);
		
		$.get('/Home/ManageTestCases/getData/', { 'selected_section_ids': selected_sections }, function(data, status) {
			if (status === 'success') {
				var query_string = data;
				loadTable(query_string);
			} else {
				alertify.error("Could not eastablish connection to the server.");
			}
		});
	});
	
	var to = false;
	$("#searchbox").keyup(function() {
		if (to) { clearTimeout(to); }
		
		to = setTimeout(function() {
			var v = $("#searchbox").val();
			$("#tree").jstree(true).search(v);
		}, 150);
	});
	
	
	function initiateRefresh(tree) {
		$(tree).jstree(true).refresh();
	}
	
	function createNode(text) {
		var node_text = '';
		var text = text || "";
		
		alertify.prompt("Name of the new section:<br><span style='font-size: 10px;'>" + text.split('.').join(' > ') + "</span>", function(e, str) {
			if (e) {
				node_text = text + str;
				node_text = node_text.split(' ').join('_');

				$.get("/Home/ManageTestCases/setData/createSection/", { 'section_text': node_text }, function(data, status) {
					if (status === 'success' && data === "1") {
						alertify.success("Section '" + str + "' created successfully.");
						initiateRefresh("#tree");
					} else {
						alertify.error("Could not eastablish connection to the server :(");
					}
				});
			} else {
				alertify.error("No text was provided", 3000);
			}
		});
	}
	
	function renameNode(node, node_id) {
		var x, y, section_path;
		
		try {
			x = node.text.split('<span style="display:none;">');
			new_text = x[0];
			
			y = x[1].split("</span>");
			section_path = y[0].split(' ').join('_');
		} catch (TypeError) {
			text = node.text;
		}
		
		alertify.prompt("New name of the section:", function(e, str) {
			if (e) {		
				$.get("/Home/ManageTestCases/setData/renameSection/", { 'section_id': node.id, 'section_path': section_path, 'new_text': str }, function(data, status) {
					if (status === 'success' && data === "1") {
						alertify.success("Section '" + node.text + "' renamed to '" + str + "' successfully.");
						initiateRefresh("#tree");
					} else {
						alertify.error("Could not eastablish connection to the server :(");
					}
				});
			} else {
				alertify.error("No text was provided", 3000);
			}
		}, new_text);
	}
	
	function deleteNode(node) {
		if (window.section_has_no_tc && node.children.length === 0) {
			$.get("/Home/ManageTestCases/setData/deleteSection/", { 'section_id': node.id }, function(data, status) {
				if (status === 'success') {
					alertify.success("Section with ID '" + data + "' deleted successfully");
					initiateRefresh("#tree");
					$("#tree").jstree(true).delete_node(node);
				} else {
					alertify.error("Could not eastablish connection to the server.");
				}
			});
		} else {
			alertify.error("Could not delete node as it has child section(s)/test cases.");
		}
	}
	
	
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
        var other_string=query_string;
		$.get("TableDataTestCasesOtherPages", {'Query': other_string,
            'test_status_request': true,
            "project_id": $.session.get('project_id'),
            "team_id": $.session.get('default_team_identity')
        }, function(data) {

	        if (data['TableData'].length == 0)
	        {
	        	window.section_has_no_tc = true;
	            $('#RunTestResultTable').children().remove();
	            $('#RunTestResultTable').append("<p class = 'Text' style=\"text-align: center;\">No Test Cases to view :(<br>It's either because you have not selected any section(s) or there are no test case(s) for the selected section(s).</p>");
	            $("#DepandencyCheckboxes").children().remove();
	        }
	        else
	        {
	        	window.section_has_no_tc = false;
				console.log(data['TableData'])
	            ResultTable('#RunTestResultTable',data['Heading'],data['TableData'],"Test Cases", "Number of test cases for the selected section(s)");
	            $("#RunTestResultTable").fadeIn(1000);
	            $("p:contains('Show/Hide Test Cases')").fadeIn(0);
	            implementDropDown("#RunTestResultTable");
	            // add edit btn
	            var indx = 0;
	            $('#RunTestResultTable tr>td:nth-child(7)').each(function(){
	                var ID = $("#RunTestResultTable tr>td:nth-child(1):eq("+indx+")").text().trim();

	                $(this).after('<span class="hint--left hint--bounce hint--rounded" data-hint="Copy Test Case"><img class="templateBtn buttonPic" id="'+ID+'" src="/site_media/copy.png" height="25"/></span>');
	                $(this).after('<span class="hint--left hint--bounce hint--rounded" data-hint="Edit Test Case"><img class="editBtn buttonPic" id="'+ID+'" src="/site_media/edit.png" height="25"/></span>');

	                indx++;
	            });

	            $(".editBtn").click(function (){
	                window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
	            });
	            $(".templateBtn").click(function (){
	                window.location = '/Home/ManageTestCases/CreateNew/'+ $(this).attr("id");
	            });
	        }
	    });
	}
	
	$("#create_section_btn").click(function(e) {
		e.preventDefault();
		
		createNode();
	});
});
