/**
 * Bismillahir Rahmanir Rahim, ALLAHU AKBAR
 * Author: Sazid
 */

var test_case_per_page=5;
var test_case_page_current=1;

var do_on_load = function do_on_load () {
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
							"label": "Create Folder",
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
							"label": "Rename Folder",
							"icon": "fa fa-edit",
							"action": function(obj) {
								renameNode(node, node.id);
							}
						},
						"Delete" : {
							"separator_before": false,
							"separator_after": false,
							"icon": "fa fa-trash-o",
							"label": "Delete Folder",
							"action": function(obj) {
								deleteNode(node);
							}
						},
						"CreateTestCase" : {
							"separator_before": true,
							"separator_after": false,
							"label": "Create Test Case",
							"icon": "fa fa-plus-square",
							"action": function(obj) {
								window.location.href="/Home/ManageTestCases/CreateNewTestCase/";
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
		var data_selected=data.selected.toString();
		$.get('/Home/ManageTestCases/getData/', { 'selected_section_ids': selected_sections }, function(data, status) {
			if (status === 'success') {
				var query_string = data_selected;
				loadTable(query_string,test_case_per_page,test_case_page_current);
                $("#pageitem").show();
                test_case_per_page = $("#perpageitem").val();
                $('#perpageitem').on('change',function(){
                    if($(this).val()!=''){
                        test_case_per_page=$(this).val();
                        test_case_page_current=1;
                        $('#pagination_tab').pagination('destroy');
                        window.location.hash = "#1";
                        loadTable(query_string,test_case_per_page,test_case_page_current);
                    }
                });
			} else {
				alertify.set({ delay: 300000 });
				alertify.error("Could not eastablish connection to the server.");
				$("#pageitem").hide();
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
		
		alertify.prompt("Name of the new folder:<br><span style='font-size: 10px;'>" + text.split('.').join(' > ') + "</span>", function(e, str) {
			if (e) {
				node_text = text + str;
				node_text = node_text.split(' ').join('_');

				$.get("/Home/ManageTestCases/setData/createSection/", 
					{
					"section_text": node_text,
                    "project_id": $.session.get('project_id'),
                    "team_id": $.session.get('default_team_identity')
                    },
					function(data, status) {
						if (status === 'success' && data === "1") {
							alertify.set({ delay: 300000 });
							alertify.success("Folder '" + str + "' created successfully.");
							initiateRefresh("#tree");
						} else {
							alertify.set({ delay: 300000 });
							alertify.error("Section '" + str + "' can not be created.");
						}
					}
				);
			} else {
				alertify.set({ delay: 300000 });
				alertify.error("No text was provided");
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
		alertify.prompt("New name of the folder:", function(e, str) {
			if (e) {		
				$.get("/Home/ManageTestCases/setData/renameSection/", { 'project_id': $.session.get('project_id'),'team_id': $.session.get('default_team_identity') ,'section_id': node.id, 'section_path': section_path, 'new_text': str }, function(data, status) {
					if (status === 'success' && data === "1") {
						alertify.success("Folder '" + node.text + "' renamed to '" + str + "' successfully.");
						initiateRefresh("#tree");
					} else {
						alertify.error("Same Folder name exists");
					}
				});
			} else {
				alertify.set({ delay: 300000 });
				alertify.error("No text was provided");
			}
		}, new_text);
	}
	
	function deleteNode(node) {
		if (window.section_has_no_tc && node.children.length === 0) {
			$.get("/Home/ManageTestCases/setData/deleteSection/", { 'section_id': node.id }, function(data, status) {
				if (status === 'success') {
					alertify.set({ delay: 300000 });
					alertify.success("Folder with ID '" + data + "' deleted successfully");
					initiateRefresh("#tree");
					$("#tree").jstree(true).delete_node(node);
				} else {
					alertify.set({ delay: 300000 });
					alertify.error("Could not eastablish connection to the server.");
				}
			});
		} else {
			alertify.set({ delay: 300000 });
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
	
	function loadTable(query_string,test_case_per_page,test_case_page_current) {
        var other_string=query_string;
		$.get("ViewAndOrganizeTestCases", {'Query': other_string,
            'test_status_request': true,
            "project_id": $.session.get('project_id'),
            "team_id": $.session.get('default_team_identity'),
            'test_case_per_page':test_case_per_page,
            'test_case_page_current':test_case_page_current
        }, function(data) {

	        if (data['TableData'].length == 0)
	        {
	        	window.section_has_no_tc = true;
	            $('#RunTestResultTable').children().remove();
	            $('#RunTestResultTable').append("<p class = 'Text' style=\"text-align: center;\">No Test Cases to view :(<br>It's either because you have not selected any folder(s) or there are no test case(s) for the selected folder(s).</p>");
	            $("#DepandencyCheckboxes").children().remove();
	            $('#pagination_div').pagination('destroy');
	            //$('#pageitem').hide();
	        }
	        else
	        {
	        	window.section_has_no_tc = false;
				console.log(data['TableData'])
	            form_table('RunTestResultTable',data['Heading'],data['TableData'],data['Count'],'Test Cases');
	            //$('#pageitem').show();
	            $('#pagination_div').pagination({
                    items:data['Count'],
                    itemsOnPage:test_case_per_page,
                    cssStyle: 'dark-theme',
                    currentPage:test_case_page_current,
                    displayedPages:2,
                    edges:2,
                    hrefTextPrefix:'#',
                    onPageClick:function(PageNumber){
                        loadTable(query_string,test_case_per_page,PageNumber);
                    }
                });
	            $("#RunTestResultTable").fadeIn(1000);
	            $("p:contains('Show/Hide Test Cases')").fadeIn(0);
	            implementDropDown("#RunTestResultTable");
	            // add edit btn
	            var indx = 0;
	            $('#RunTestResultTable tr>td:nth-child(7)').each(function(){
	                var ID = $("#RunTestResultTable tr>td:nth-child(1):eq("+indx+")").text().trim();
	                $(this).after('<span style="cursor: pointer; margin-left: 8px;" class="hint--left hint--bounce hint--rounded" data-hint="Copy Test Case"><i class="fa fa-copy fa-2x templateBtn" id="'+ID+'"></i></span>');
	                $(this).after('<span style="cursor: pointer; margin-left: 8px;" class="hint--left hint--bounce hint--rounded" data-hint="Edit Test Case"><i class="fa fa-pencil fa-2x editBtn" id="'+ID+'"></i></span>');
	                
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
};
function form_table(divname,column,data,total_data,type_case){
	var tooltip=type_case||':)';
	var message='';
	message+= "<p class='Text hint--right hint--bounce hint--rounded' data-hint='" + tooltip + "' style='color:#0000ff; font-size:14px; padding-left: 12px;'>" + total_data + " " + type_case+"</p>";
	message+='<table class="two-column-emphasis">';
	message+='<tr>';
	for(var i=0;i<column.length;i++){
		message+='<th>'+column[i]+'</th>';
	}
	message+='</tr>';
	for(var i=0;i<data.length;i++){
		message+='<tr>';
		for(var j=0;j<data[i].length;j++){
			switch(data[i][j]){
				case 'Dev':
					message+='<td style="background-color: ' + colors['dev'] + '; color: #fff;">' + data[i][j] + '</td>';
					continue;
				case 'Ready':
					message+='<td style="background-color: ' + colors['ready'] + '; color: #fff;">' + data[i][j] + '</td>';
					continue;
				default :
					message+='<td>'+data[i][j]+'</td>';
					continue;
			}
		}
		message+='</tr>';
	}
	message+='</table>';
	$('#'+divname).html(message);
}
function loadWithScript() {
	$.getScript("/site_media/Jquery/jstree/jstree.min.js")
	.done(function (script, textStatus) {
		do_on_load();
	})
	.fail(function (jqxhr, settings, exception) {
		window.location.reload();
	});
}

$(document).ready(loadWithScript);
$(window).bind('pjax:complete', loadWithScript);
