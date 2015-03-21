/**
 * Created by J on 9/11/14.
 */

var project_id= $.session.get('project_id');
var team_id= $.session.get('default_team_identity');
var user = $.session.get('fullname');

$(document).ready(function(){
    $("#new_label").click(function(){
        //$("#label_creation").show();
        if($("#label_creation").is(":visible")){
            $("#label_creation").slideUp('slow');
            //$("#label_creation").hide();
        }
        else{
            $("#label_creation").slideDown('slow');
            //$("#label_creation").show();
        }
    });
    $("#cancel_label").click(function(){
        $("#label_creation").slideUp('slow');
    });
    $("#color_picker").spectrum({
        color: "#f00",
        preferredFormat: "hex",
        showInput: true
    });

    $("#create_label").click(function(){
        var name = $("#label_name").val();
        var color = $(".sp-input").val();

        if(name!= ""){
            $.get("CreateLabel/",{
                name:name.trim(),
                color:color.trim(),
                project:project_id,
                team:team_id,
                user:$.session.get('fullname')
            },function(data){
                alertify.success("Label Created!");
                $("#label_creation").slideUp('slow');
                window.location.reload(true);
            });
        }
        else{
            alertify.error("Label Name is needed!", 5000);
        }
    });
})