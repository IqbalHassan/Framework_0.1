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
                alertify.set({ delay: 300000 });
                alertify.success("Label Created!");
                $("#label_creation").slideUp('slow');
                window.location.reload(true);
            });
        }
        else{
            alertify.set({ delay: 300000 });
            alertify.error("Label Name is needed!");
        }
    });

    $("#all_labels tr td:nth-child(3)").each(function(){
        $(this).on('click',function(){
            var label = $(this).parent().find('td:first-child').text().trim();
            var label_id = $(this).parent().find('td:nth-child(2)').text().trim();
            //reset();
            var message='';
            message+='<div>';
            message+='<p style="font-size:140%">Are you sure to delete label <b>' + label + '</b>?</p>';
            message+='<br/>';
            message+='</div>';
            alertify.confirm(message, function (e) {
                if (e) {
                    $.get("DeleteLabel/",{
                        label_id:label_id
                    },function(data){
                        alertify.set({ delay: 300000 });
                        alertify.success("Label Deleted!");
                        window.location.reload(true);
                    });
                    
                } else {
                    alertify.set({ delay: 300000 });
                    alertify.error("You've clicked Cancel");
                }
            });
            return false;
       });
    });
})