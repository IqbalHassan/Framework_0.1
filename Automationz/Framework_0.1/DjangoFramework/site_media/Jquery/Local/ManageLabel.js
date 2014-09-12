/**
 * Created by J on 9/11/14.
 */
$(document).ready(function(){
    $("#new_label").click(function(){
        $("#label_creation").show();
        if($("#label_creation").visible()){
            //$(this).slideUp('slow');
            $(this).hide();
        }
        else{
            //$(this).slideDown('slow');
            $(this).show();
        }
    });
})