$(document).ready(function(){
   $("#operation").live('change',function(event){
       var choice_value=$("#operation").val();
       var data_type;
       event.preventDefault();
       console.log(choice_value);
       if(choice_value == 2){
           $("#name_variable").html("Old Name:");
           $("#renamebox").css({'display':'inline-block'});
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
           }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
               return $( "<li></li>" )
                   .data( "ui-autocomplete-item", item )
                   .append( "<a>" + item[0] + "<strong> - " + item[1] + "</strong></a>" )
                   .appendTo( ul );
           };
       }
       else{
           $("#name_variable").html("Name:");
           $("#renamebox").css({'display':'none'});
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
           var tc_id_name = ui.item[0].split(" - ");
           var value = "";
           if (tc_id_name != null)
               value = tc_id_name[0];
           $("#input").val(value);
           return false;
       }
   }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
       return $( "<li></li>" )
           .data( "ui-autocomplete-item", item )
           .append( "<a>" + item[0] + "<strong> - " + item[1] + "</strong></a>" )
           .appendTo( ul );
   };
});