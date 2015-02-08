/**
 * Created by minar09 on 3/27/14.
 */


var lowest_feature = 0;
var isAtLowestFeature = false;
var user = $.session.get('fullname');

$(document).ready(function(){

    $('input[name="step_user"]').val(user);
    $('input[name="step_project"]').val($.session.get('project_id'));
    $('input[name="step_team"]').val($.session.get('default_team_identity'));

    description_fill();
    verification_radio();
    Continue_radio();
    TimePicker();


    $.ajax({
        url:'GetFeatures/',
        dataType : "json",
        data : {
            feature : '',
            project_id: $.session.get('project_id'),
            team_id: $.session.get('default_team_identity')
        },
        success: function( json ) {
            if(json.length > 0)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                if(i == 0)return;
                $(".feature[data-level='']").append($('<option>').text(value).attr('value', value));
            });
            $(".feature[data-level='']").attr('id',1);
        }
    });
    $(".feature[data-level='']").change(function(){
        isAtLowestFeature = false;
        recursivelyAddFeature(this);
        $("#feature-flag").removeClass("filled");
        $("#feature-flag").addClass("unfilled");
        $('input[name="step_feature"]').val("");
    });

    /*$.ajax({
        url:'GetFeature/',
        dataType : "json",
        data : {
            feature : ''
        },
        success: function( json ) {
            if(json.length > 1)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                //if(i == 0)return;
                if(value=="Common"){
                    $(".step-feat[data-level='']").append($('<option selected="selected">').text(value).attr('value', value));
                }
                else{
                    $(".step-feat[data-level='']").append($('<option>').text(value).attr('value', value));
                }
            });
        }
    });*/
    $.ajax({
        url:'GetDriver/',
        dataType : "json",
        data : {
            driver : ''
        },
        success: function( json ) {
            if(json.length > 1)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                //if(i == 0)return;
                if(value=="Manual"){
                    $(".step-driv[data-level='']").append($('<option selected="selected">').text(value).attr('value', value));
                }
                else{
                    $(".step-driv[data-level='']").append($('<option>').text(value).attr('value', value));
                }
            });
        }
    });
    /*var feature_list=[];
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
          /*  for(var i=0;i<data.length;i++){
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
         /*   for(var i=0;i<data.length;i++){
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
    }*/

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
                console.log(value);
                $("#step_name").val(value);
                $.ajax({
                    url:"Populate_info_div",
                    dataType:"json",
                    data:{term:value},
                    success:function(data){
                        console.log(data[0])
                        //info_div(data[0]);
                        ready_feature();

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
                        //$("#step_feature").val(row[6]);
                        
                        $.get("get_feature_path",{'term':value ,'id':row[6]},function(data)
                        {
                            var features = data;
                        var featureArray = features.split('.');
                        var dataId ="";
                        var handlerString = "";
                        for(var index in featureArray){
                            if(featureArray[index] == "")
                                continue;
                            $.ajax({
                                url:'GetFeatures/',
                                dataType : "json",
                                data : {
                                    feature : dataId.replace(/^\.+|\.+$/g, "").replace(/ /g,'_'),
                                    project_id: $.session.get('project_id'),
                                    team_id: $.session.get('default_team_identity')
                                },
                                success: function( json ) {
                                    if(json.length != 1){
                                        var realItemIndex = parseInt(json[0][0])
                                        var handlerString = ""
                                        for(var i = 0; i < realItemIndex; i++)
                                            handlerString+=featureArray[i]+'.'

                                        if(realItemIndex == 0){
                                            $(".feature[data-level='']").find('option').each(function(){$(this).remove();});
                                            $(".feature[data-level='']").append("<option>Choose...</option>");

                                            for(var i = 0; i < json.length; i++)
                                                json[i] = json[i][0].replace(/_/g,' ')
                                            $.each(json, function(i, value) {
                                                if(i == 0)return;
                                                $(".feature[data-level='']").append($('<option>').text(value).attr('value', value));
                                            });
                                            $(".feature[data-level='']").val(featureArray[realItemIndex].replace(/_/g,' '))
                                        }else{
                                            var tag = jQuery('<select/>',{
                                                'class':'feature',
                                                'data-level':handlerString,
                                                'id':realItemIndex+1,
                                                change: function(){
                                                    isAtLowestFeature = false;
                                                    recursivelyAddFeature(this);
                                                    $("#feature-flag").removeClass("filled");
                                                    $("#feature-flag").addClass("unfilled");
                                                }
                                            })
                                            if($('#featuregroup select[id='+realItemIndex+']').length != 0)
                                                $('#featuregroup select[id='+realItemIndex+']').after(tag)
                                            else
                                                $('#featuregroup select[id=1]').after(tag);

                                            $(".feature[data-level='"+handlerString+"']").append("<option>Choose...</option>");

                                            var once = true;
                                            for(var i = 0; i < json.length; i++)
                                                json[i] = json[i][0].replace(/_/g,' ')
                                            $.each(json, function(i, value) {
                                                if(i == 0)return;
                                                if(once){
                                                    lowest_feature+=1
                                                    once = false
                                                }
                                                $(".feature[data-level='"+handlerString+"']").append($('<option>').text(value).attr('value', value));
                                            });
                                            $(".feature[data-level='"+handlerString+"']").val(featureArray[realItemIndex].replace(/_/g,' '))
                                        }
                                        isAtLowestFeature = true;
                                        $("#feature-flag").removeClass("unfilled");
                                        $("#feature-flag").addClass("filled");
                                        var newFeaturePath = $("#featuregroup select.feature:last-child").attr("data-level").replace(/ /g,'_') + $("#featuregroup select.feature:last-child option:selected").val().replace(/ /g,'_');
                                        $('input[name="step_feature"]').val(newFeaturePath);


                                        /*var newFeaturePath = $("#featuregroup select.feature:last-child").attr("data-level").replace(/ /g,'_') + $("#featuregroup select.feature:last-child option:selected").val().replace(/ /g,'_');

                                        $.get("Check_Feature_Path",{Feature_Path : newFeaturePath},function(data)
                                            {
                                                if (data.length > 1) {
                                                    $("#feature-flag").removeClass("filled");
                                                    $("#feature-flag").addClass("unfilled");
                                                    isAtLowestFeature = false;
                                                };
                    
                                            });*/
                                    }
                                }
                            });

                            dataId += featureArray[index] + '.'
                        }
                    });



                        $("#case_desc").val(row[9]);
                        $("#step_expect").val(row[10]);
                        if(row[11]==true){
                            $("#true_radio").trigger('click');
                        }
                        else if(row[11]==false){
                            $("#false_radio").trigger('click');
                        }
                        if(row[12]==true){
                            $("#yes_radio").trigger('click');
                        }
                        else if(row[12]==false){
                            $("#no_radio").trigger('click');
                        }
                        $("#step_time").val(row[13]);
                        $(".timepicker").timepicker('setTime', convertToString(row[13]));

                        
                        $("#automata").val(row[14]);

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
                alertify.log("Sorry There is No Test Cases For Selected Query!","",0);
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


function ready_feature(){
    $("#featuregroup").empty();

    $('#featuregroup').html('' +
        '<select type="text" class="feature step-feat" data-level="">' +
         '<option>Choose...</option>' +
          '</select>'
        );

    $.ajax({
        url:'GetFeatures/',
        dataType : "json",
        data : {
            feature : '',
            project_id: $.session.get('project_id'),
            team_id: $.session.get('default_team_identity')
        },
        success: function( json ) {
            if(json.length > 0)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                if(i == 0)return;
                $(".feature[data-level='']").append($('<option>').text(value).attr('value', value));
            });
            $(".feature[data-level='']").attr('id',1);
        }
    });
    $(".feature[data-level='']").change(function(){
        isAtLowestFeature = false;
        recursivelyAddFeature(this);
        $("#feature-flag").removeClass("filled");
        $("#feature-flag").addClass("unfilled");
        $('input[name="step_feature"]').val("");
    });

}
    /*$("#delete_button").click(function(){
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
    });*/

});
function description_fill(){
    $("#step_name").keyup(function(){
        var desc = $(this).val();
        /*if(("#step_desc").val()==""){
            $("#step_desc").val(desc);
        }
        if(("#case_desc").val()==""){
            $("#case_desc").val(desc);
        }
        if(("#step_expect").val()==""){
            $("#step_expect").val(desc);
        }*/
        $("#step_desc").val(desc);
        $("#case_desc").val(desc);
        $("#step_expect").val(desc);
    });
};
function verification_radio(){
    $("#true_radio").live('click',function(){
        $(this).addClass("selected");
        $("#false_radio").removeClass("selected");
        var value = $("#true_radio").attr('value');
        $("#verify_radio").attr('value',value);
    });
    $("#false_radio").live('click',function(){
        $(this).addClass("selected");
        $("#true_radio").removeClass("selected");
        var value = $("#false_radio").attr('value');
        $("#verify_radio").attr('value',value);
    });

   if($("#true_radio").hasClass("selected"))
    {
        var value = $("#true_radio").attr('value');
        $("#verify_radio").attr('value',value);
    }
    else if($("#false_radio").hasClass("selected"))
    {
       var value = $("#false_radio").attr('value');
       $("#verify_radio").attr('value',value);
    }
}
function Continue_radio(){
    $("#yes_radio").live('click',function(){
        $(this).addClass("selected");
        $("#no_radio").removeClass("selected");
        var value = $("#yes_radio").attr('value');
        $("#continue_radio").attr('value',value);
    });
    $("#no_radio").live('click',function(){
        $(this).addClass("selected");
        $("#yes_radio").removeClass("selected");
        var value = $("#no_radio").attr('value');
        $("#continue_radio").attr('value',value);
    });

    if($("#yes_radio").hasClass("selected"))
    {
        var value = $("#yes_radio").attr('value');
        $("#continue_radio").attr('value',value);
    }
    else if($("#no_radio").hasClass("selected"))
    {
        var value = $("#no_radio").attr('value');
        $("#continue_radio").attr('value',value);
    }
}
function TimePicker(){
    $('.timepicker').timepicker({
        minuteStep: 1,
        template: 'dropdown',
        appendWidgetTo: 'body',
        showSeconds: true,
        showMeridian: false,
        defaultTime: '00:00:60 AM',
        secondStep: 1
    });

    var time = $(".timepicker").val();
    var second = convertToSeconds(time);
    $("#step_time").val(second);

    $(".timepicker").change(function(){
        var time = $(".timepicker").val();
        var second = convertToSeconds(time);
        $("#step_time").val(second);
    });
}
function convertToSeconds(stringTime){
    var hour=stringTime.split(":")[0].trim();
    var minuate=stringTime.split(":")[1].trim();
    var seconds=stringTime.split(":")[2].trim();
    var total=(hour*3600)+(minuate*60)+(seconds*1);
    return total;
}
function convertToString(intTime){
    var hour=Math.floor(intTime/3600);
    intTime=intTime%3600;
    var minuate=Math.floor(intTime/60);
    intTime=intTime%60;
    if(hour<10){
        hour="0"+hour;
    }
    if(minuate<10){
        minuate="0"+minuate;
    }
    if(intTime<10){
        intTime="0"+intTime;
    }
    var stringTime=hour+":"+minuate+":"+intTime;
    return stringTime.trim();
}

function recursivelyAddFeature(_this){
    var fatherHeirarchy = $(_this).attr("data-level");
    var father = $(_this).children("option:selected").text();
    if(father == "")
        return;
    if(father == "Choose..."){
        for(var i = 0; i < lowest_feature; i++){
            $("#featuregroup select.feature:last-child").remove();
        }
        lowest_feature = 0
        return;
    }
    var current_feature = (fatherHeirarchy.split(".").length - 1)
    if(current_feature < lowest_feature){
        for(var i = current_feature + 1; i <= lowest_feature; i++){
            $("#featuregroup select.feature:last-child").remove();
        }
        lowest_feature = current_feature
    }

    $.ajax({
        url:'GetFeatures/',
        dataType : "json",
        data : {
            feature : (fatherHeirarchy+father).replace(/ /g,'_'),
            project_id: $.session.get('project_id'),
            team_id: $.session.get('default_team_identity')

        },
        success: function( json ) {
            if(json.length != 1){
                jQuery('<select/>',{
                    'class':'feature',
                    'data-level':fatherHeirarchy+father+'.',
                    change: function(){
                        isAtLowestFeature = false;
                        recursivelyAddFeature(this);
                        $("#feature-flag").removeClass("filled");
                        $("#feature-flag").addClass("unfilled");
                    }
                }).appendTo('#featuregroup');

                $(".feature[data-level='"+fatherHeirarchy+father+".']").append("<option>Choose...</option>");

                var once = true;
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
                $.each(json, function(i, value) {
                    if(i == 0)return;
                    if(once){
                        lowest_feature+=1
                        once = false
                    }
                    $(".feature[data-level='"+fatherHeirarchy+father+".']").append($('<option>').text(value).attr('value', value));
                });
            }else{
                isAtLowestFeature = true;
                $("#feature-flag").removeClass("unfilled");
                $("#feature-flag").addClass("filled");
                var newFeaturePath = $("#featuregroup select.feature:last-child").attr("data-level").replace(/ /g,'_') + $("#featuregroup select.feature:last-child option:selected").val().replace(/ /g,'_');
                $('input[name="step_feature"]').val(newFeaturePath);
            }
        }
    });
}
