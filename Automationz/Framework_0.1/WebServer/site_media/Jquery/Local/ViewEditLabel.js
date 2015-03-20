/**
 * Created by minar09 on 3/20/15.
 */
var editpath="ViewEditLabel/";
var project_id= $.session.get('project_id');
var team_id= $.session.get('default_team_identity');

$(document).ready(function(){

	var URL=window.location.pathname;
    var edit_index=URL.indexOf(editpath);
    var template = URL.length > (URL.lastIndexOf("/")+1) && URL.indexOf(createpath) != -1;
    
    if(edit_index!=-1){
        var referred_label=URL.substring((URL.lastIndexOf(editpath)+(editpath).length),(URL.length-1));
        $("#header").html($.session.get('project_id')+' / View & Edit Label / '+referred_label);
        
        $.get("getLabelinfo/",{
	        'label_id':referred_label.trim()
	    },function(data){
	    	$("#label_name").val(data['details'][0][1]);
			$("#label_color").val(data['details'][0][2]);	        
	    });


	    $("#edit_button").click(function(){
	        var name = $("#label_name").val();
	        var color = $("#label_color").val();

	        if(name!= ""){
	            $.get("EditLabel/",{
	            	id:referred_label.trim(),
	                name:name.trim(),
	                color:color.trim()
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