/**
 * Bismillahir Rahmanir Rahim, ALLAHU AKBAR
 * Author: Sazid
 */

$(document).ready(function() {

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
				}
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
			
			"plugins" : [ "search", "checkbox", "types" ]
	};
	
	$("#tree").jstree(config_object);
	
});
