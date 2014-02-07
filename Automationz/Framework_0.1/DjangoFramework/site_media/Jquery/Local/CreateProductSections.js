/**
 * Created by minar09 on 2/7/14.
 */

$(document).ready(function(){

    $(".main").autocomplete({
        source: function(request,response){
            $.ajax({
                url:"GetSections",
                dataType:"json",
                data:{
                    section : ''
                },
                success:function(data){
                    response(data);
                }
            });
        },
        /*select: function(request,ui){
         var tc_id_name = ui.item.value.split(" - ");
         var value = "";
         if (tc_id_name != null)
         value = tc_id_name[0];
         $("#input").val(value);
         return false;
         }*/
        select: function(request,ui){
            var value = ui.item[0];
            if(value!=""){
                $(".main").val(value);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "</a>" )
            .appendTo( ul );
    };

    $(".sub1").autocomplete({
        //var sect = $(".main").val();
        source: function(request,response){
            $.ajax({
                url:"GetSubSections",
                dataType:"json",
                data:{
                    section : ''
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select: function(request,ui){
            var value = ui.item[0];
            if(value!=""){
                $(".sub1").val(value);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "</a>" )
            .appendTo( ul );
    };
});
