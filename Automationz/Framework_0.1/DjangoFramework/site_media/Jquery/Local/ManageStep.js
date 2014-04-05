/**
 * Created by minar09 on 4/5/14.
 */
$(document).ready(function(){


    var feature_list=[];
    var driver_list=[];
    $.ajax({
        url:'GetFeature/',
        dataType : "json",
        data : {
            feature : ''
        },
        success: function( data ) {
            /*if(json.length > 1)
             for(var i = 1; i < json.length; i++)
             json[i] = json[i][0].replace(/_/g,' ')
             $.each(json, function(i, value) {
             //if(i == 0)return;
             $(".step-feat[data-level='']").append($('<option>').text(value).attr('value', value));
             });*/
            //console.log(data);
            for(var i=0;i<data.length;i++){
                //$('#step_feature').append('<option value="'+data[i][0]+'">'+data[i][0]+'</opiton>');
                feature_list.push(data[i][0]);
            }
        }
    });
    $.ajax({
        url:'GetDriver/',
        dataType : "json",
        data : {
            driver : ''
        },
        success: function( data ) {
            /* if(json.length > 1)
             for(var i = 1; i < json.length; i++)
             json[i] = json[i][0].replace(/_/g,' ')
             $.each(json, function(i, value) {
             //if(i == 0)return;
             $(".step-driv[data-level='']").append($('<option>').text(value).attr('value', value));
             });*/
            //console.log(data);
            for(var i=0;i<data.length;i++){
                //$('#step_driver').append('<option value="'+data[i][0]+'">'+data[i][0]+'</opiton>');
                driver_list.push(data[i][0]);
            }
        }
    });
    $("#create_edit").click(function(event){
        //event.preventDefault();
        //console.log("clicked");

        $('#search').hide();
        //$('#error').hide();
        $('#create_edit').hide();
        $("#feature_driver").hide();
        //$("#choice").append("<p style='font-size:1.5em;'><b>Action</b>: Delete</p>");
        populate_info_div(feature_list,driver_list);
        populate_footer_div();
    });
    $("#search").click(function(){
        $("#choice_div").hide();
        $("#create_edit_div").hide();
        $("#feature_driver").hide();
        $("#search_choice").append("<p style='font-size:1.5em;'><b>Action</b>: Search Test Step</p>");
        populate_search_div();
    });
    $("#feature_driver").click(function(){
        //$('#error').hide();
        $('#search').hide();
        $("#choice_div").hide();
        $("#create_edit_div").hide();
        $("#feature_driver_choice").append("<p style='font-size:1.5em;'><b>Action</b>: Feature/Driver Options</p>");
        populate_feature_driver_info_div();
    });

});


function populate_feature_driver_info_div(){
    $("#feature_driver_info_div").append('' +
        '<div align="center">' +
        '<table style="border: 2px #666; font-family: Open Sans, Arial, Helvetica, sans-serif; padding: 2px; margin: 10px;" width="80%">' +
        '<tr>' +
        '<td align="center">' +
        '<div id="left">'+
        '<label><b>Type:</b></label>' +
        "&nbsp;&nbsp;&nbsp;" +
        '<select id="type" class="select-drop" name="type">' +
        '<option selected value="">Select from list</option>' +
        '<option value="feature">Feature</option>' +
        '<option value="driver">Driver</option>' +
        '</select>' +
        '</div>' +
        '</td>' +
        '<td align="center">' +
        '<div id="right">' +
        '<label><b>Operation:</b></label>' +
        "&nbsp;&nbsp;&nbsp;" +
        '<select id="operation" class="select-drop" name="operation">' +
        '<option value="0"selected="selected">Select from list</option>' +
        '<option value="1">Create</option>' +
        '<option value="2">Rename</option>' +
        '<option value="3">Delete</option>' +
        '</select>' +
        '</div>' +
        '</td>' +
        '<td align="center">' +
        '<div id="center">' +
        '<label><b id="name_variable">Name:</b></label>' +
        "&nbsp;&nbsp;&nbsp;" +
        "<input class=\"ui-corner-all textbox\" id=\"input\" style=\"margin: 5px; width:auto;\" type='text' title = 'Please Type Keyword' name='inputName' />" +
        '</div>' +
        '</td>' +
        '<td align="center">' +
        '<div id="renamebox">' +

        '</div>' +
        '</td>' +
        '<td align="center">' +
        '<div id="error">' +
        '<p><b>No Operation is selected</b></p>' +
        '</div>' +
        '</td>' +
        '<td align="center">' +
        '<br/>' +
        '<div id="button_id" style="display: none">' +
        '<input type=\'submit\' id=\"select_button\" class=\"button minibutton primary\" name=\'submit_button\'/>' +
        '</div>' +
        '<div id="button_del" style="display: none">' +
        '<input type=\'button\' id=\"del_button\" class=\"button minibutton primary\" name=\'del_button\'/>' +
        '</div>' +
        '</td>' +
        '</tr>' +
        '</table>' +
        '</div>'

    );
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
            //$("#error").hide();
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
                    window.location = '/Home/ManageTestCases/FeatureDriverDelete';
                }
            }
        });
    });
}

function populate_info_div(feature_list,driver_list){
    $('#info_div').append('' +
        '<div align="center">' +
        '<label><b>Test Step Name:</b></label><br>' +
        '<br/>' +
        '<input type="text" placeholder="Enter the test step name" id="step_name" class="textbox" name="step_name"/>' +
        '</div>'
       /* '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
        '<label><b>Test Step Description:</b></label><br>' +
        '<textarea rows="5" cols="35" id="step_desc" name="step_desc" class="textbox" style="height:35px"  placeholder="Describe the test step(within 180 letters)"></textarea>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
        '<label><b>Feature:</b></label><br>' +
        '<select type="text" id="step_feature" name="step_feature" class="combo-box step-feat" data-level="">' +
        '<option value="">Select from list</option>' +
        '</select>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
        '<label><b>Driver:</b></label><br>' +
        '<select type="text" id="step_driver" name="step_driver" class="combo-box step-driv" data-level="">' +
        '<option value="">Select from list</option>' +
        '</select>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
        '<br/>' +
        '<label><b>Test Step Type:</b></label><br>' +
        '<select id="step_type" class="select-drop" name="step_type">' +
        '<option value="0" selected="selected">Select from list:</option>' +
        '<option value="1">Automated</option> ' +
        '<option value="2">Manual</option>' +
        '<option value="3">Performance</option> ' +
        '</select>' +
        '</div>' +
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
        '<br/>' +
        '<label><b>Data Requirement:</b></label><br>' +
        '<select id="step_data" class="select-drop" name="step_data">' +
        '<option value="0" selected="selected">Select from list:</option>' +
        '<option value="1">Data</option>' +
        '<option value="2">No Data</option> ' +
        '<option value="3">Edit Data</option> ' +
        '</select>' +
        '</div><br>'+
        '<div style="float: left;margin-right: 15px;margin-left: 5px">' +
        '<br/>' +
        '<label><b>Step Enable</b></label><br>' +
        '<select id="step_enable" class="select-drop" name="step_enable">' +
        '<option value="0" selected="selected">Select from list:</option>' +
        '<option value="1">True</option>' +
        '<option value="2">False</option> ' +
        '</select>' +
        '</div><br>'*/
    );
    for(var i=0;i<feature_list.length;i++){
        $('#step_feature').append('<option value="'+feature_list[i]+'">'+feature_list[i]+'</opiton>');
    }
    for(var i=0;i<driver_list.length;i++){
        $('#step_driver').append('<option value="'+driver_list[i]+'">'+driver_list[i]+'</opiton>');
    }
    $("#step_name").autocomplete({
        source: function(request,response){
            $.ajax({
                url:"TestStep_Auto",
                dataType:"json",
                data:{term:request.term},
                success:function(data){
                    response(data);
                }
            });
        },
        select: function(request,ui){
            var value=ui.item[0];
            if(value!=""){
                $("#step_name").val(value);
                $.ajax({
                    url:"Populate_info_div",
                    dataType:"json",
                    data:{term:value},
                    success:function(data){
                        //info_div(data[0]);
                        var row=data[0];
                        $("#step_desc").val(row[2]);
                        $("#step_driver").val(row[3]);
                        if(row[7]==null){
                            $("#step_enable").val(2);
                        }
                        if(row[7]==false){
                            $("#step_enable").val(2);
                        }
                        if(row[7]==true){
                            $("#step_enable").val(1);
                        }
                        if(row[5]==null && (row[8]== false||row[8]==null)){
                            $("#step_data").val(2);
                        }
                        if(row[5]==false && (row[8]== false||row[8]==null)){
                            $("#step_data").val(2);
                        }
                        if(row[5]==true && (row[8]== false||row[8]==null)){
                            $("#step_data").val(1);
                        }
                        if(row[5]==true && row[8]==true){
                            $("#step_data").val(3);
                        }
                        if(row[4]=="manual"){
                            $("#step_type").val(2);
                        }
                        if(row[4]=="automated"){
                            $("#step_type").val(1);
                        }
                        if(row[4]=="performance"){
                            $("#step_type").val(3);
                        }
                        $("#step_feature").val(row[6]);
                    }
                });
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
            .appendTo( ul );
    };
    /*$("#step_feature").autocomplete({
     source: function(request,response){
     $.ajax({
     url:"TestFeature_Auto",
     dataType:"json",
     data:{term:request.term},
     success:function(data){
     response(data);
     }
     });
     },
     select: function(request,ui){
     var value = ui.item[0];
     if(value!=""){
     $("#step_feature").val(value);
     return false;
     }
     }
     }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
     return $( "<li></li>" )
     .data( "ui-autocomplete-item", item )
     .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
     .appendTo( ul );
     };
     $("#step_driver").autocomplete({
     source: function(request,response){
     $.ajax({
     url:"TestDriver_Auto",
     dataType:"json",
     data:{term:request.term},
     success:function(data){
     response(data);
     }
     });
     },
     select: function(request,ui){
     var value = ui.item[0];
     if(value!=""){
     $("#step_driver").val(value);
     return false;
     }
     }
     }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
     return $( "<li></li>" )
     .data( "ui-autocomplete-item", item )
     .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
     .appendTo( ul );
     };*/
    //$(".select-drop").selectBoxIt();
    //$('.combo-box').combobox();
}
function populate_footer_div(){
    $('#footer_div').append('' +
        '<div>' +
        '<input type="button" id="delete_button" class="button minibutton danger" value="Delete"/>' +
        '<input type="button" id="get_cases" class="button minibutton primary" value="Get Test Cases"/>' +
        //'<input type="submit" id="submit_button" class="button minibutton blue" name="submit_button" value="Submit">' +
        '</div>'
    );
    $("#get_cases").click(function(){
        var UserText=$("#step_name").val();
        console.log(UserText);
        Env = "PC"
        $.get("TestCase_Results",{Query: UserText, Env: Env},function(data) {

            if (data['TableData'].length == 0)
            {
                $('#search_result').children().remove();
                $('#search_result').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                //$("#DepandencyCheckboxes").children().remove();
                //$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
            }
            else
            {
                ResultTable('#search_result',data['Heading'],data['TableData'],"Test Cases");

                $("#search_result").fadeIn(1000);
                $("p:contains('Show/Hide Test Cases')").fadeIn(0);
                implementDropDown("#search_result");
                // add edit btn
                var indx = 0;
                $('#search_result tr>td:nth-child(3)').each(function(){
                    var ID = $("#search_result tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<img class="templateBtn buttonPic" id="'+ID+'" src="/site_media/copy.png" height="25" style="cursor:pointer;"/>');
                    $(this).after('<img class="editBtn buttonPic" id="'+ID+'" src="/site_media/edit.png" height="25" style="cursor:pointer;"/>');

                    indx++;
                });

                $(".editBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
                });
                $(".templateBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Create/'+ $(this).attr("id");
                });
                //VerifyQueryProcess();
                //$(".Buttons[title='Verify Query']").fadeIn(2000);
                //$(".Buttons[title='Select User']").fadeOut();
            }

        });

    });
    $("#delete_button").click(function(){
        var name=$("#step_name").val();
        console.log(name);
        $.ajax({
            url:"TestStep_Delete",
            dataType:"json",
            data:{term:name},
            success:function(data){
                var count=data[0];
                console.log(count);
                if(count>0){
                    $("#delete_error").html("<p><b>This test step can't be deleted. There are "+count+" test cases using this test step '"+name+"'</b></p>");
                }
                if(count==0){
                    window.location = '/Home/ManageTestCases/TestStepDelete';
                }
            }
        });
    });
}
function populate_search_div(){
    $('#search_div').append('' +
        '<div>' +
        '<label><b>Search for the Test Steps:</b></label>' +
        '<input type="text" id="search_query" class="textbox" name="search_query" placeholder="Enter the keywords"/>' +
        '</div>' +
        '<div>' +
        '<table id = "AutoSearchResult" >'
        +   '<tbody>'
        + '<tr id = "searchedtext">'
        +'<p> </p>'
        + '<th class = "Text" style= "text-align: left"> Test Data Set: </th>'
        + '</tr>'
        +   '</tbody>' +
        '</table>' +
        '</div>'
    );
    AutoComplete();
}
function AutoComplete(){
    $("#search_query").autocomplete({
        source : function(request, response) {
            $.ajax({
                url:"TestStepAutoComplete",
                dataType: "json",
                data:{ term: request.term },
                success: function( data ) {
                    response( data );
                }
            });
        },
        select : function(event, ui) {

            var tc_id_name = ui.item.value.split(" - ");
            var value = "";
            if (tc_id_name != null)
                value = tc_id_name[0];
            if(value!=""){
                $("#AutoSearchResult #searchedtext").append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
                    +'<td name = "submitquery" class = "Text" style = "size:10">'
                    + value
                    + ":&nbsp"
                    +'</td>');
                //console.log(value);
                PerformSearch();
                $("#search_query").val("");
                return false;
            }

        }
    });
    $("#search_query").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }

    });
}
function PerformSearch(){
    $("#AutoSearchResult #searchedtext").each(function(){
        var UserText=$(this).find("td").text();
        console.log(UserText);
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        console.log("Changed:"+UserText);
        $.get("TestStep_TestCases",{Query:UserText},function(data){
            if (data['TableData'].length == 0)
            {
                $('#search_result').children().remove();
                $('#search_result').append("<p class = 'Text'><b>Sorry There is No Test Cases For Selected Query!!!</b></p>");
                //$("#DepandencyCheckboxes").children().remove();
                //$('#DepandencyCheckboxes').append("<p class = 'Text'><b>No Depandency Found</b></p>");
            }
            else
            {
                ResultTable('#search_result',data['Heading'],data['TableData'],"Test Cases");

                $("#search_result").fadeIn(1000);
                $("p:contains('Show/Hide Test Cases')").fadeIn(0);
                //new modification
                implementDropDown("#search_result");
                // add edit btn
                var indx = 0;
                $('#search_result tr>td:nth-child(3)').each(function(){

                    var ID = $("#search_result tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<img class="templateBtn buttonPic" id="'+ID+'" src="/site_media/copy.png" height="25" style="cursor:pointer;"/>');
                    $(this).after('<img class="editBtn buttonPic" id="'+ID+'" src="/site_media/edit.png" height="25" style="cursor:pointer;"/>');

                    indx++;
                });

                $(".editBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
                });
                $(".templateBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Create/'+ $(this).attr("id");
                });
                //VerifyQueryProcess();
                //$(".Buttons[title='Verify Query']").fadeIn(2000);
                //$(".Buttons[title='Select User']").fadeOut();
            }

        });
        $(".delete").click(function(){
            $(this).parent().next().remove();
            $(this).remove();
        });
    });
}
function implementDropDown(wheretoplace){
    $(wheretoplace+" tr td:nth-child(2)").css({'color' : '#000066','cursor' : 'pointer'});
    $(wheretoplace+" tr td:nth-child(2)").each(function() {
        $(this).live('click',function() {

            var childrenCount = $(this).children().length
            if (childrenCount == 0)
            {
                $(this).children().slideDown();
            }
            else
            {
                $(this).children().slideUp();
                //childrenCount=0;
                $(this).children().remove();
                return;
            }
            var ClickedTC = $(this).text();
            var RunID = $(this).closest('tr').find('td:nth-child(1)').text();
            RunID = RunID.trim();

            var $TC = $(this).text();
            var TestSteps;
            $.get("TestStepWithTypeInTable",{ClickedTC : ClickedTC,RunID: RunID},function(data) {
                TestSteps = data['Result'];

                $(".ui-widget tr td:nth-child(2)").each(function() {
                    //if (($(this).text()) == ClickedTC)
                    if($(this).closest('tr').find('td:nth-child(1)').text()==RunID)
                    {

                        $(this).children().remove();
                        for (eachitem in data['Result'])
                        {

                            $($(this)).append("<p id = 'TestCase_Steps'>"+ data['Result'][eachitem]																																				+ "</p>");
                        }

                    }

                    $("p#TestCase_Steps").css({'color' : '#9999FF','cursor' : 'text'});
                });

            });
            //$(this).children().slideToggle();

        });
    });
}