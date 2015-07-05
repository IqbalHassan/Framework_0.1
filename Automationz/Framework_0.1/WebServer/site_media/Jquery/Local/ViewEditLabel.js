/**
 * Created by minar09 on 3/20/15.
 */
 var createpath="CreateNewLabel/";
var editpath="ViewEditLabel/";
var project_id= $.session.get('project_id');
var team_id= $.session.get('default_team_identity');
var user = $.session.get('fullname');
var new_label_text = "New label";

$(document).ready(function(){

	var URL=window.location.pathname;
    var create_index=URL.indexOf(createpath);
    var edit_index=URL.indexOf(editpath);
    var template = URL.length > (URL.lastIndexOf("/")+1) && URL.indexOf(createpath) != -1;
    
    $("#label_search_box").select2({
		placeholder: "Label Name...",
//		minimumInputLength: 3,
		width: 460,
		quietMillis: 250,
		ajax: {
			url: "LabelSearch/",
			dataType: "json",
			queitMillis: 250,
			data: function(term, page) {
				return {
					'term': term,
					'page': page,
                    'project_id': project_id,
                    'team_id': team_id
				};
			},
			results: function(data, page) {
				return {
					results: data.items,
					more: data.more
				}
			}
		},
		createSearchChoice: function(term) {
			return {id: new_label_text, text: new_label_text + ": " + term};
		},
		createSearchChoicePosition: "top",
		formatResult: formatLabels
	})
	// Listens for changes so that we can prompt the user if they want to edit or
	// copy existing test cases
	.on("change", function(e) {
//		console.log(JSON.stringify({val: e.val, added: e.added, removed: e.removed}));
		if (e.val === new_label_text) {
//			console.log("New test case is being created!");
		} else {
//			console.log("Existing test case has been selected.");
			var start = $(this).select2("data")["text"].indexOf(":") + 1;
    		var length = $(this).select2("data")["text"].length;
    		
    		var label_title = $(this).select2("data")["text"].substr(start, length - 1);
        
			var label_id = $(this).val();
			$("#title_prompt").html(
				'<p style="text-align: center">You have selected ' +
				'<span style="font-weight: bold;">' + label_id +': '+ label_title + '</span>' +
				'<br/> What do you want to do?' +
				'</p> &nbsp; &nbsp; &nbsp;' +
				'<div style="padding-left: 28%">' +
				'<a class="github" href="/Home/ViewEditLabel/'+label_id+'">Edit</a>' +
				'<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
				'</div>'
			);
          $("#title_prompt").modal();
          return false;
		}
	});
	
	// Should be used for formatting results, LATER
	function formatLabels(label_details) {
		var start = label_details.text.indexOf(":") + 1;
		var start2 = label_details.text.indexOf("#");
		var length = label_details.text.length;
		
		var label_title = label_details.text.substr(start, start2 - 1);
		var label_color = label_details.text.substr(start2, length - 1);
		
		var markup =
			'<div>' +
			'<i class="fa fa-file-text fa-fw"></i> <span>' + label_details.id + '</span>' +
			': ' +
			'<span style="font-weight: bold;">' + label_title + '</span>' +
			'  ' +
			'<a class="label" style="background-color:' + label_color + '"></a>' +
			'</div>';
		
		return markup;
	}

    if(edit_index!=-1){
        var referred_label=URL.substring((URL.lastIndexOf(editpath)+(editpath).length),(URL.length-1));
        $("#header").html(referred_label);
        
        $.get("getLabelinfo/",{
	        'label_id':referred_label.trim(),
	        'project_id':project_id,
	        'team_id':team_id
	    },function(data){
	    	//$("#label_name").val(data['details'][0][1]);
	    	$("#label_search_box").select2("data", {"id": data['details'][0][0], "text": data['details'][0][0] + ": " + data['details'][0][1]});
			$("#label_color").val(data['details'][0][2]);
			$("#created_by").text(data['details'][0][5]);
			$("#created_date").text(data['details'][0][7]);
			$("#modified_by").text(data['details'][0][6]);
			$("#modified_date").text(data['details'][0][8]);

			ResultTable(reqs_div,data['reqs_heading'],data['reqs'],'Requirements','Requirements');
			$('#reqs_div tr>td:first-child').each(function(){
		        $(this).css({
		            'color':'blue',
		            'cursor':'pointer'
		        });
		        $(this).click(function(){
		         var location='/Home/'+$.session.get('project_id')+'/EditRequirement/'+$(this).text().trim()+'/';
		         window.location=location;
		         });
	    	});	        

	    	ResultTable(tasks_div,data['tasks_heading'],data['tasks'],'Tasks','Tasks');
	    	$('#tasks_div tr>td:first-child').each(function(){
		        $(this).css({
		            'color':'blue',
		            'cursor':'pointer'
		        });
		        $(this).click(function(){
		            var location='/Home/'+$.session.get('project_id')+'/EditTask/'+$(this).text().trim()+'/';
		            window.location=location;
		        });
		    });

		    ResultTable(bugs_div,data['bugs_heading'],data['bugs'],'Bugs','Bugs');
		    $('#bugs_div tr>td:first-child').each(function(){
		        $(this).css({
		            'color':'blue',
		            'cursor':'pointer'
		        });
		        $(this).click(function(){
		         var location='/Home/EditBug/'+$(this).text().trim()+'/';
		         window.location=location;
		         });
		    });
	    });


	    $("#edit_button").click(function(){
	        var name = $("#label_name").val();
	        var color = $("#label_color").val();

	        if(name!= ""){
	            $.get("EditLabel/",{
	            	id:referred_label.trim(),
	                name:name.trim(),
	                color:color.trim(),
	                project:project_id,
	                team:team_id,
	                user:user
	            },function(data){
	            	alertify.set({ delay: 300000 });
	                alertify.success("Label Updated!");
	                window.location.reload(true);
	            });
	        }
	        else{
	        	alertify.set({ delay: 300000 });
	            alertify.error("Label Name is needed!");
	        }
	    });
    }

});