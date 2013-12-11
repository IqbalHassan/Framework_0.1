$(document).ready(function(){
   $("#operation").click(function(event){
       var choice_value=$("#operation").val();
       event.preventDefault();
       console.log(choice_value);
       if(choice_value == 2){
           $("#name_variable").html("Old Name:");
           $("#renamebox").html(
               "<label><b>New Name:</b></label>"
                   +"&nbsp;&nbsp;&nbsp;"
                   +"<input class=\"ui-corner-all\" id=\"input2\" style=\"margin-left: -2%\" type='text' title = 'Please Type Keyword' name='inputName2' />"
           );
           //$("#button_id").html("<input type='submit' value='Rename' name='submit_button'/>");
           $("#error").hide();
          // console.log("choice_value:"+choice_value);
           $("#select_button").val("Rename");
           var value=$("#select_button").val();
         //  console.log(value);
           $("#button_id").show();
           $("#input2").autocomplete({
               source: function(request,response){
                   if($("#type").val()=="set"){
                       data_type="set";
                   }
                   if($("#type").val()=="tag"){
                       data_type="tag"
                   }
                   $.ajax({
                       url:"TestSet_Auto",
                       dataType:"json",
                       data:{term:request.term,data_type:data_type},
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
                   $("#input2").val(value);
                   return false;
               }
           });
       }
       else{
           $("#name_variable").html("Name:");
           $("#renamebox").html("");
           var button_value="";
           if(choice_value==0){
               button_value=0;
               if(button_value==0){
                   $("#select_button").val(button_value);
                   $("#button_id").hide();
                   $("#error").show();
               }

           }
           else{
               if(choice_value==1)
               {
                   button_value="Create";
               }
               if(choice_value==3){
                   button_value="Edit";
               }
               if(choice_value==4){
                   button_value="Delete";
               }
               console.log("choice_value:"+choice_value);
               $("#error").hide();
               $("#select_button").val(button_value);
               console.log($("#select_button").val());
               $("#button_id").show();
              // $("#button_id").html("<input type='submit' value='"+ button_value +"' name='submit_button'/>");
           }
       }
   });
   $("#input").autocomplete({
       source: function(request,response){
           if($("#type").val()=="set"){
               data_type="set";
           }
           if($("#type").val()=="tag"){
               data_type="tag"
           }
           $.ajax({
               url:"TestSet_Auto",
               dataType:"json",
               data:{term:request.term,data_type:data_type},
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
   /* $("#input2").autocomplete({
        source: function(request,response){
            $.ajax({
                url:"TestSetTag_Auto",
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
            $("#input2").val(value);
            return false;
        }
    });*/
});