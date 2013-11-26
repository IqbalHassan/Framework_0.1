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
                   +"<input class=\"ui-corner-all\" id=\"input\" style=\"margin-left: -2%\" type='text' title = 'Please Type Keyword' name='inputName' />"
           );
           $("#button_id").html("<input type='submit' value='Rename' name='submit_button'/>");
       }
       else{
           $("#name_variable").html("Name:");
           $("#renamebox").html("");
           var button_value="";
           if(choice_value==0){
                $("#button_id").html("");
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
               $("#button_id").html("<input type='submit' value='"+ button_value +"' name='submit_button'/>");
           }

       }
   });
});