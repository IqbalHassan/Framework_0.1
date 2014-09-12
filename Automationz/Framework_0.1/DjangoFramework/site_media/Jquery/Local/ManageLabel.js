/**
 * Created by J on 9/11/14.
 */
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
                color:color.trim()
            },function(data){
                alertify.success("Label Created!");
                $("#label_creation").slideUp('slow');
            });
        }
        else{
            alertify.error("Label Name is needed!", 5000);
        }
    });
})