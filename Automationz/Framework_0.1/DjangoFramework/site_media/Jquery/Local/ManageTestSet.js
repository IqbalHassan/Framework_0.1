$(document).ready(function(){
    $("#type").click(function(event){
        event.preventDefault();
        console.log($("#type").val());
        if($("#type").val()!="0"){
            $("#button_place").html("<input type=\"submit\" name=\"submit_button\" id=\"submitButton\" value=\"Search\"/>");
        }
        else{
            $("#button_place").html("")
        }

    });
    $("#input").autocomplete({
        source: function(request,response){
            if($("#type").val()==1){
                var url="TestSet_Auto";
            }
            if($("#type").val()==2){
                var url="TestTag_Auto"
            }
            if($("#type").val()==3){
                var url="TestCase_Auto"
            }
            $.ajax({
                url:url,
                dataType:"json",
                data:{term:request.term},
                success:function(data){
                    response(data);
                }
            });
        },
        select: function(request,ui){
            var tc_id_name = ui.item.value.split(" - ");
            var value = "";
            if (tc_id_name != null)
                value = tc_id_name[0];
            $("#input").val(value);
            return false;
        }
    });
    $("#submit_button").click(function(event){

    });
});