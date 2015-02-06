/**
 * Created by minar09 on 3/25/14.
 */
$(document).ready(function(){

    $(".select-drop").selectBoxIt();
    $("#operation").live('change',function(event){
        var choice_value=$("#operation").val();
        event.preventDefault();
        console.log(choice_value);
        console.log("choice_value:"+choice_value);
        if(choice_value == 2){
            $("#name_variable").html("Old Name:");
            $("#renamebox").html(
                "<label><b>New Name:</b></label>"
                    +"&nbsp;&nbsp;&nbsp;"
                    +"<input class=\"ui-corner-all textbox\" id=\"input2\" style=\"margin: 5px; width:auto;\" type='text' title = 'Please Type Keyword' name='inputName2' />"
            );
            //$("#button_id").html("<input type='submit' value='Rename' name='submit_button'/>");
            $("#error").hide();
            $("#button_del").hide();
            // console.log("choice_value:"+choice_value);
            $("#select_button").val("Rename");
            var value=$("#select_button").val();
            //  console.log(value);
            $("#button_id").show();
            $("#input2").autocomplete({
                source: function(request,response){
                    if($("#type").val()=="feature"){
                        data_type="feature";
                    }
                    if($("#type").val()=="driver"){
                        data_type="driver"
                    }
                    $.ajax({
                        url:"TestFeatureDriver_Auto",
                        dataType:"json",
                        data:{term:request.term,data_type:data_type},
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
                 $("#input2").val(value);
                 return false;
                 }*/
                select: function(request,ui){
                    var value = ui.item[0];
                    if(value!=""){
                        $("#input2").val(value);
                        return false;
                    }
                }
            }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
                return $( "<li></li>" )
                    .data( "ui-autocomplete-item", item )
                    .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
                    .appendTo( ul );
            };
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
                    $("#button_del").hide();
                    $("#error").show();
                }

            }
            else{
                if(choice_value==1)
                {
                    button_value="Create";
                    $("#error").hide();
                    $("#button_del").hide();
                    $("#select_button").val(button_value);
                    $("#button_id").show();
                }
                if(choice_value==3){
                    button_value="Delete";
                    $("#error").hide();
                    $("#button_id").hide();
                    $("#del_button").val(button_value);
                    $("#button_del").show();
                }
                //console.log("choice_value:"+choice_value);
                //$("#error").hide();
                //$("#select_button").val(button_value);
                // console.log($("#select_button").val());
                //$("#button_id").show();
                // $("#button_id").html("<input type='submit' value='"+ button_value +"' name='submit_button'/>");
            }
        }
    });
    $("#input").autocomplete({
        source: function(request,response){
            if($("#type").val()=="feature"){
                data_type="feature";
            }
            if($("#type").val()=="driver"){
                data_type="driver";
            }
            $.ajax({
                url:"TestFeatureDriver_Auto",
                dataType:"json",
                data:{term:request.term,data_type:data_type},
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
                $("#input").val(value);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
            .appendTo( ul );
    };

    $("#del_button").click(function(){
        var type = $("#type").val();
        var inputName=$("#input").val();
        console.log(inputName);
        $.ajax({
            url:"FeatureDriver_Delete",
            dataType:"json",
            data:{term:type,inputName:inputName},
            //data:{term:inputName},
            success:function(data){
                var count=data[0];
                console.log(count);
                if(count>0){
                    $("#delete_error").html("<p><b>This feature/driver can't be deleted. There are "+count+" test steps using this feature/driver '"+inputName+"'</b></p>");

                    var UserText=$("#input").val();
                    console.log(UserText);
                    Env = "PC"
                    $.get("TestSteps_Results",{Query: UserText, Env: Env},function(data) {

                        if (data['TableData'].length == 0)
                        {
                            $('#search_result').children().remove();
                            $('#search_result').append("<p class = 'Text'><b>Sorry There is No Test Steps For Selected Query!!!</b></p>");
                            //$("#DepandencyCheckboxes").children().remove();
                            //$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
                        }
                        else
                        {
                            ResultTable('#search_result',data['Heading'],data['TableData'],"Test Steps");

                            $("#search_result").fadeIn(1000);
                            $("p:contains('Show/Hide Test Steps')").fadeIn(0);
                            implementDropDown("#search_result");
                            // add edit btn
                            var indx = 0;
                            $('#search_result tr>td:nth-child(1)').each(function(){
                                var ID = $("#search_result tr>td:nth-child(1):eq("+indx+")").text().trim();

                                $(this).after('<img class="templateBtn buttonPic" id="'+ID+'" src="/site_media/copy.png" height="25" style="cursor:pointer;"/>');
                                $(this).after('<img class="editBtn buttonPic" id="'+ID+'" src="/site_media/edit.png" height="25" style="cursor:pointer;"/>');

                                indx++;
                            });

                            $(".editBtn").click(function (){
                                window.location = '/Home/ManageTestCases/TestStep/';//+ $(this).attr("id");
                            });
                            $(".templateBtn").click(function (){
                                window.location = '/Home/ManageTestCases/TestStep/';//+ $(this).attr("id");
                            });
                            //VerifyQueryProcess();
                            //$(".Buttons[title='Verify Query']").fadeIn(2000);
                            //$(".Buttons[title='Select User']").fadeOut();

                        }

                    });
                }
                if(count==0){
                    window.location = '/Home/FeaDri/FeatureDriverDelete';
                }
            }
        });
    });

    /*$("#select_button").click(function(){

        var type = $("#type").val();
        var operation = $("#operation").val();
        var inputName=$("#input").val();
        var inputName2=$("#input2").val();
        console.log(inputName);

        $.ajax({
            url:'FeatureDriverOperation',
            dataType:"json",
            data:{type:type,operation:operation,inputName:inputName,inputName2:inputName2},
            success:function(data){
            if(data['confirm_message']==""){
                var color='red';
            }
            else{
                var color='green';
            }
            if(data['confirm_message']==""){
                $('#error_message').html('<b style="color:red;">'+data['error_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                $('#error_message').slideDown('slow');
                setTimeout(function(){window.location='/Home/FeaDri/';},4000);
            }
            else{
                $('#error_message').html('<b style="color:green;">'+data['confirm_message']+'<br>Page will be refreshed in 3 seconds to change effect</b>');
                $('#error_message').slideDown('slow');
                setTimeout(function(){window.location='/Home/FeaDri/';},4000);
            }
            }
        });
    });*/


});