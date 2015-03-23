/**
 * Created by minar09 on 3/20/15.
 */
var editpath="ViewEditLabel/";
var project_id= $.session.get('project_id');
var team_id= $.session.get('default_team_identity');
var user = $.session.get('fullname');

$(document).ready(function(){

	var URL=window.location.pathname;
    var edit_index=URL.indexOf(editpath);
    var template = URL.length > (URL.lastIndexOf("/")+1) && URL.indexOf(createpath) != -1;
    
    if(edit_index!=-1){
        var referred_label=URL.substring((URL.lastIndexOf(editpath)+(editpath).length),(URL.length-1));
        $("#header").html(referred_label);
        
        $.get("getLabelinfo/",{
	        'label_id':referred_label.trim(),
	        'project_id':project_id,
	        'team_id':team_id
	    },function(data){
	    	$("#label_name").val(data['details'][0][1]);
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
	                alertify.success("Label Updated!");
	                window.location.reload(true);
	            });
	        }
	        else{
	            alertify.error("Label Name is needed!", 5000);
	        }
	    });
    }

});