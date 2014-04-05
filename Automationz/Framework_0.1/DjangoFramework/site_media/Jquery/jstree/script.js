// Bismillahir Rahmanir Rahim, ALLAHU AKBAR
// Author: Sazid

$(function() {

	$("button").click(function() {
		$.get("http://127.0.0.1:8000/Home/ManageTestCases/view_and_organize_tc/", function(data, status) {
			alert("Data: " + data + "\nStatus: " + status);
		});
	});

	var treeConfig = {
		
		'core' : { /*
			'data' : {
				'url' : function (node) {
				  return node.id === '#' ? 
					'http://127.0.0.1:8000/Home/ManageTestCases/view_and_organize_tc/' : 
					'http://127.0.0.1:8000/Home/ManageTestCases/view_and_organize_tc/';
				},
				'data' : function (node) {
				  return { 'id' : node.id };
				}
			} */
		}
	};
	
	// Create an instance of jstree with the provided container
	$("#jstree_container").jstree(treeConfig);

	
});
