/**
 * Created by minar09 on 3/27/14.
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

});