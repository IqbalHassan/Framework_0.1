/**
 * Created by minar09 on 3/27/14.
 */


var lowest_feature = 0;
var isAtLowestFeature = false;
var user = $.session.get('fullname');
var itemPerPage=10;
var PageCurrent=1;
var project_id = $.session.get('project_id');
var team_id = $.session.get('default_team_identity');
var createpath="CreateStep/";
var editpath="EditStep/";
var operation = 1;
var step_id = 0;
var new_test_step_text = "New test step";


$(document).ready(function(){

    title_box();

    var URL=window.location.pathname;
    var URL = decodeURIComponent(URL);
    var create_index=URL.indexOf(createpath);
    var edit_index=URL.indexOf(editpath);
    var template = URL.length > (URL.lastIndexOf("/")+1) && URL.indexOf(createpath) != -1;
    if(create_index != -1){

        $("#header").html('Create Step');
    }

    if(edit_index!=-1){
        var referred_step=URL.substring((URL.lastIndexOf(editpath)+(editpath).length),(URL.length-1));
        console.log(referred_step);
        $("#header").html('Edit Step / '+referred_step);
        $("#step_name").val(referred_step);
        $("#step_name").select2("data", {"id": "Edit test step", "text": "Edit test step" + ": " + referred_step});
        PopulateStepInfo(referred_step);
        operation=2;
        //req_id = referred_req;
    }


    $('input[name="step_user"]').val(user);
    $('input[name="step_project"]').val(project_id);
    $('input[name="step_team"]').val(team_id);

    description_fill();
    verification_radio();
    Continue_radio();
    TimePicker();
    


    $.ajax({
        url:'GetFeatures/',
        dataType : "json",
        data : {
            feature : '',
            project_id: project_id,
            team_id: team_id
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

    /*$("#step_name").autocomplete({
        source: function(request,response){
            $.ajax({
                url:"TestStep_Auto",
                dataType:"json",
                data:{term:request.term,project_id:project_id},
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
                $("#title_prompt").html(
                    '<p style="text-align: center">You have selected Test Step - ' +
                    '<span style="font-weight: bold;">' + value + '</span>' +
                    '<br/> What do you want to do?' +
                    '</p><br>' +
                    '<div style="padding-left: 23%">' +
                    '<a class="twitter" href="/Home/ManageTestCases/EditStep/'+value+'">Edit Step</a>' +
                    //'<a class="twitter" href="/Home/ManageTestCases/CreateNew/'+tc_id+'">Copy</a>' +
                    '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
                    '</div>'
                );
              $("#title_prompt").modal();
                //PopulateStepInfo(value);
                return false;
            }
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a><strong>" + item[0] + "</strong> - " + item[1] + "</a>" )
            .appendTo( ul );
    };*/

    $("#get_cases").click(function(){
        var UserText=$("#step_name").val();
        console.log(UserText);
        itemPerPage = $("#perpageitem").val();
        get_cases(UserText,itemPerPage, PageCurrent);
        $('#perpageitem').on('change',function(){
            if($(this).val()!=''){
                itemPerPage=$(this).val();
                current_page=1;
                $('#pagination_tab').pagination('destroy');
                window.location.hash = "#1";
                get_cases(UserText,itemPerPage, PageCurrent);
            }
        });
        
        //Env = "PC"
    });

    submit_step();
});

function title_box(){
    $("#step_name").select2({
        placeholder: "Test Step title...",
//      minimumInputLength: 3,
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "TestStepSearch/",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'project_id': $.session.get('project_id')
                    //'team_id': $.session.get('default_team_identity')
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        createSearchChoice: function(term) {
            return {id: new_test_step_text, text: new_test_step_text + ": " + term};
        },
        createSearchChoicePosition: "top",
        formatResult: formatTestSteps
    })
    // Listens for changes so that we can prompt the user if they want to edit or
    // copy existing test cases
    .on("change", function(e) {
//      console.log(JSON.stringify({val: e.val, added: e.added, removed: e.removed}));
        if (e.val === new_test_step_text) {
//          console.log("New test case is being created!");
            var start = $(this).select2("data")["text"].indexOf(":") + 1;
            var length = $(this).select2("data")["text"].length;
            
            var desc = $(this).select2("data")["text"].substr(start, length - 1);
            $("#step_desc").val(desc);
            $("#case_desc").val(desc);
            $("#step_expect").val(desc);
        } else {
//          console.log("Existing test case has been selected.");
            var start = $(this).select2("data")["text"].indexOf(":") + 1;
            var length = $(this).select2("data")["text"].length;
            
            var type = $(this).select2("data")["text"].substr(start, length - 1);
        
            var step_name = $(this).val();
            $("#step_name").val(step_name);
            $("#title_prompt").html(
                    '<p style="text-align: center">You have selected Test Step - ' +
                    '<span style="font-weight: bold;">' + step_name + '</span>' +
                    '<br/> What do you want to do?' +
                    '</p><br>' +
                    '<div style="padding-left: 23%">' +
                    '<a class="twitter" href="/Home/ManageTestCases/EditStep/'+step_name+'">Edit Step</a>' +
                    //'<a class="twitter" href="/Home/ManageTestCases/CreateNew/'+tc_id+'">Copy</a>' +
                    '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
                    '</div>'
            );
          $("#title_prompt").modal();
          return false;
        }

    });    
}

function formatTestSteps(step_details) {
        var start = step_details.text.indexOf(":") + 1;
        var length = step_details.text.length;
        
        var type = step_details.text.substr(start, length - 1);
        var title = step_details.text.substr(0,start-1);
        
        var markup =
            '<div>' +
            '<i class="fa fa-file-text fa-fw"></i> <span style="font-weight: bold;">' + step_details.id + '</span>' +
            ': ' +
            '<span>' + type + '</span>'
            '</div>';
        
        return markup;
    }

function PopulateStepInfo(value){
    $.ajax({
        url:"Populate_info_div",
        dataType:"json",
        data:{term:value},
        success:function(data){
            console.log(data[0])
            //info_div(data[0])
            ready_feature();

            var row=data[0];
            step_id = row[0];
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
}

function get_cases(UserText,itemPerPage,PageCurrent){
    $.get("TestCase_Results",{Query: UserText,itemPerPage:itemPerPage,PageCurrent:PageCurrent},function(data) {

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
                $("#inner").show();
                ResultTable('#search_result',data['Heading'],data['TableData'],"Test Cases");

                $('#pagination_tab').pagination({
                    items:data['count'],
                    itemsOnPage:itemPerPage,
                    cssStyle: 'dark-theme',
                    currentPage:PageCurrent,
                    displayedPages:2,
                    edges:2,
                    hrefTextPrefix:'#',
                    onPageClick:function(PageNumber){
                        //PerformSearch(project_id,team_id,user_text,itemPerPage,PageNumber);
                        get_cases(UserText,itemPerPage,PageNumber);
                    }
                });

                $("#search_result").fadeIn(1000);
                $("p:contains('Show/Hide Test Cases')").fadeIn(0);
                implementDropDown("#search_result");
                // add edit btn
                var indx = 0;
                $('#search_result tr>td:nth-child(3)').each(function(){
                    var ID = $("#search_result tr>td:nth-child(1):eq("+indx+")").text().trim();

                    $(this).after('<i class="fa fa-copy fa-2x templateBtn" id="'+ID+'" style="cursor:pointer"></i>');
                    $(this).after('<i class="fa fa-pencil fa-2x editBtn" id="'+ID+'" style="cursor:pointer"></i>');

                    indx++;
                });

                $(".editBtn").click(function (){
                    window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
                });
                $(".templateBtn").click(function (){
                    window.location = '/Home/ManageTestCases/CreateNew/'+ $(this).attr("id");
                });
                //VerifyQueryProcess();
                //$(".Buttons[title='Verify Query']").fadeIn(2000);
                //$(".Buttons[title='Select User']").fadeOut();
            }

        });

}

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
                //var newFeaturePath = $("#featuregroup select.feature:last-child").attr("data-level").replace(/ /g,'_') + $("#featuregroup select.feature:last-child option:selected").val().replace(/ /g,'_');
                //$('input[name="step_feature"]').val(newFeaturePath);
            }
        }
    });
}


function submit_step(){

    $("#submit_button").live('click',function(e){
        if ($("#step_name").select2("val") === "" || $("#step_name").select2("val") === []) {
                e.preventDefault();

                alertify.error("Please provide the <span style='font-weight: bold;'>Test Step title</span>", 2500);

                $("#step_name").select2("open");

//                setTimeout(function() {
//                    $("#titlebox").css({
//                        "border-color": "",
//                        "box-shadow": ""
//                    });
//                }, 1500);

                return false;
            }

        var start = $("#step_name").select2("data")["text"].indexOf(":") + 1;
        var length = $("#step_name").select2("data")["text"].length;
        
        var step_name = $("#step_name").select2("data")["text"].substr(start, length - 1);
        var step_desc = $("#step_desc").val().trim();
        var step_data = $("#step_data").val().trim();
        var step_type = $("#step_type").val().trim();
        var step_driver = $("#step_driver").val().trim();
        var step_enable = $("#step_enable").val().trim();
        var case_desc = $("#case_desc").val().trim();
        var step_expect = $("#step_expect").val().trim();
        var verify_radio = $("#verify_radio").val().trim();
        var continue_radio = $("#continue_radio").val().trim();
        var step_time = $("#step_time").val().trim();
        var automata = $("#automata").val().trim();
        var newFeaturePath = $("#featuregroup select.feature:last-child").attr("data-level").replace(/ /g,'_') + $("#featuregroup select.feature:last-child option:selected").val().replace(/ /g,'_');

        $.get("CreateEditStep/",{
            'step_name' : step_name,
            'step_desc' : step_desc,
            'step_feature' : newFeaturePath,
            'step_data' : step_data,
            'step_type' : step_type,
            'step_driver' : step_driver,
            'step_enable' : step_enable,
            'case_desc' : case_desc,
            'step_expect' : step_expect,
            'verify_radio' : verify_radio,
            'continue_radio' : continue_radio,
            'step_time' : step_time,
            'automata' : automata,
            'user' : user,
            'project_id' : project_id,
            'team_id' : team_id,
            'operation' : operation,
            'step_id' : step_id
        },function(data) {
            if (operation==1) {
                alertify.success("Test Step '"+data+"' successfully created!","",0);
                desktop_notify("Test Step -'"+data+"' successfully created!");
            };
            if (operation==2) {
                alertify.success("Test Step '"+data+"' successfully updated!","",0);
                desktop_notify("Test Step -'"+data+"' successfully updated!");
            };
            
            var location='/Home/ManageTestCases/EditStep/'+data;
            window.location=location;
        });
    });
}


function desktop_notify(message){
    // At first, let's check if we have permission for notification
    // If not, let's ask for it
    if (Notification && Notification.permission !== "granted") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }
        });
    }

    var button = document.getElementById('submit_button');

    // If the user agreed to get notified
    if (Notification && Notification.permission === "granted") {
        var n = new Notification("Test Step Created/Updated!",{body:message, icon:"/site_media/noti.ico"});
    }

    // If the user hasn't told if he wants to be notified or not
    // Note: because of Chrome, we are not sure the permission property
    // is set, therefore it's unsafe to check for the "default" value.
    else if (Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function (status) {
            if (Notification.permission !== status) {
                Notification.permission = status;
            }

            // If the user said okay
            if (status === "granted") {
                var n = new Notification("Test Case Created/Updated!",{body:message, icon:"/site_media/noti.ico"});
            }

            // Otherwise, we can fallback to a regular modal alert
            else {
                alertify.log(message,"",0);
            }
        });
    }

    // If the user refuses to get notified
    else {
        // We can fallback to a regular modal alert
        alertify.log(message,"",0);
    }


}