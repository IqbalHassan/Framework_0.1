
// Bismillahir Rahmanir Rahim, ALLAHU AKBAR
// Author: Sazid

$(document).ready(function() {
	
	var config_object = {
			"core" : {
				"themes" : { "variant" : "large" },

				"data" : {
					"url" : function(node) {
						if (node.id === "#") {
							return "/Home/ManageTestCases";
						} else {
							return "/Home/ManageTestCases/getData";
						}
						
					},
					"data" : function(node) {
						return { 'id' : node.id }
					}
				}
				
				// "check_callback" : true
			},
			
			"types" : {
				"#" : {
					"valid_children" : ["parent"]
				},
				
				"parent" : {
					"icon" : "glyphicon glyphicon-list",
					"valid_children" : ["children"]
				},
				
				"children" : {
					"icon" : "glyphicon glyphicon-tag",
					"valid_children" : []
				}
			},
			
			"plugins" : [ "checkbox", "search", "types", "wholerow", "contextmenu", "sort", "state" ]
	};
	
	$("#tree_container").jstree(config_object);
	
	var to = false;
	$("#searchbox").keyup(function() {
		if (to) { clearTimeout(to); }
		
		/* Here we're using a timeout so that the search is done after
		   a specified amount of time rather than on every key stroke
		   NOTE: Raise the value if the browser slows down during search
		 */
		to = setTimeout(function() {
			var v = $("#searchbox").val();
			
			$("#tree_container").jstree(true).search(v);
		}, 250);
	});

});
