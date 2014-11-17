/**
 * Created by lent400 on 8/14/14.
 */
var operation = 1;
var lowest_section = 0;
var isAtLowestSection = false;
var lowest_feature = 0;
var isAtLowestFeature = false;

$(document).ready(function(){
    $('#project_id').text($.session.get('project_id'));
    $('#starting_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#ending_date').datepicker({ dateFormat: "yy-mm-dd" });
    addingSections();
    status_button_preparation();
    Submit_button_preparation();

    URL = window.location.pathname;
    console.log("url:"+URL);
    indx = URL.indexOf("EditTask");
    console.log("Edit Index:"+indx);
    if(indx!=-1){
        var referred_task=URL.substring((URL.lastIndexOf("EditTask/")+("EditTask/").length),(URL.length-1));
        $("#header").html($.session.get('project_id')+' / '+$('#default_team_identity :selected').text()+' / Edit Task / '+referred_task);
        PopulateTaskInfo(referred_task);
        operation=2;
        //bugid=referred_task;
    }
    else{
        $("#header").html($.session.get('project_id')+' / '+$('#default_team_identity :selected').text()+' / Create Task');
    }
    console.log("Url Length:"+URL.length);

});

function PopulateTaskInfo(task_id){

    $.get("Selected_TaskID_Analaysis",{Selected_Task_Analysis : task_id},function(data){

        $("#title").val(data['Task_Info'][0][0]);

        if(data['Task_Info'][0][11]=="not_started")
        {
            $('a[value="not_started"]').addClass('selected')
            $('a[value="started"]').removeClass('selected')
            $('a[value="complete"]').removeClass('selected')
            $('a[value="over_due"]').removeClass('selected')
        }
        else if(data['Task_Info'][0][11]=="started")
        {
            $('a[value="not_started"]').removeClass('selected')
            $('a[value="started"]').addClass('selected')
            $('a[value="complete"]').removeClass('selected')
            $('a[value="over_due"]').removeClass('selected')
        }
        else if(data['Task_Info'][0][11]=="complete")
        {
            $('a[value="not_started"]').removeClass('selected')
            $('a[value="started"]').removeClass('selected')
            $('a[value="complete"]').addClass('selected')
            $('a[value="over_due"]').removeClass('selected')
        }
        else if(data['Task_Info'][0][11]=="over_due")
        {
            $('a[value="not_started"]').removeClass('selected')
            $('a[value="started"]').removeClass('selected')
            $('a[value="complete"]').removeClass('selected')
            $('a[value="over_due"]').addClass('selected')
        }

        $("#description").val(data['Task_Info'][0][1]);
        $("#starting_date").val(data['Task_Info'][0][2]);
        $("#ending_date").val(data['Task_Info'][0][3]);
        $("#tester").html('<td><img class="delete" id = "DeleteTester" title = "TesterDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/></td>'
        + '<td class="Text selected">'
        + data['tester']
            //+ "&nbsp"
        + '</td>');
        $("#task_info").show();
        $("#created_by").text(data['Task_Info'][0][6]);
        $("#created_date").text(data['Task_Info'][0][7]);
        $("#modified_by").text(data['Task_Info'][0][8]);
        $("#modified_date").text(data['Task_Info'][0][9]);

        $("#milestone").val(data['Task_Info'][0][5]);


        $('input[name="priority"]').each(function(){
            $(this).prop('checked',false);
        });
        $('input[name="priority"]').each(function(){
            if(data['Task_Info'][0][4]==$(this).val()){
                $(this).prop('checked',true);
            }
        });

        //FeaturePath
        var features=data['Feature'];
        console.log(features);
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
                                $('#featuregroup select[id=1]').after(tag)

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
                    }
                }
            });

            dataId += featureArray[index] + '.'
        }


    });


}

function Submit_button_preparation(){
    $('#submit').click(function(){

        if($('#project_identity option:selected').val()==""){
            alertify.error("Please select a project topbar",1500);
            return false;
        }
        if($('#default_team_identity option:selected').val()==""){
            alertify.error("Please select a team from topbar",1500);
            return false;
        }

        if($('#feature-flag').hasClass('unfilled')){
            //alert("Feature Path is not defined Correctly");
            alertify.error("Feature Path is not defined Correctly","",0);
            return false;
        }

        var title=$('#title').val().trim();

        if(title==""){
            alertify.error("Title is empty!");
        }
        if($("#section-flag").hasClass("unfilled")){
            alertify.error("You need to choose a section!");
        }

        if($('a[value="not_started"]').hasClass('selected'))
            var status = "not_started";
        if($('a[value="started"]').hasClass('selected'))
            var status = "started";
        if($('a[value="complete"]').hasClass('selected'))
            var status = "complete";
        if($('a[value="over_due"]').hasClass('selected'))
            var status = "over_due";

        var description=$('#description').val().trim();
        var team=[];
        $('input[name="team"]:checked').each(function(){
            team.push($(this).val());
        });
        var tester=[];
        $('input[name="tester"]:checked').each(function(){
            tester.push($(this).val());
        });
        var starting_date=$('#starting_date').val().trim();
        var ending_date=$('#ending_date').val().trim();
        var priority=$('input[name="priority"]:checked').val();
        var milestone=$('#milestone option:selected').val();
        var project_id= $.session.get('project_id');
        var newSectionPath = $("#sectiongroup select.section:last-child").attr("data-level").replace(/ /g,'_') + $("#sectiongroup select.section:last-child option:selected").val().replace(/ /g,'_');
        var newFeaturePath = $("#featuregroup select.feature:last-child").attr("data-level").replace(/ /g,'_') + $("#featuregroup select.feature:last-child option:selected").val().replace(/ /g,'_');

        if(operation==1){
            $.get('SubmitNewTask/',{
                'title':title,
                'status':status,
                'description':description,
                'team':team.join("|"),
                'tester':tester.join("|"),
                'starting_date':starting_date,
                'ending_date':ending_date,
                'priority':priority,
                'milestone':milestone,
                'project_id':project_id,
                'section_path':newSectionPath,
                'feature_path':newFeaturePath,
                'user_name':$.session.get('fullname')

            },function(data){
                window.location=('/Home/'+ $.session.get('project_id')+'/EditTask/'+data);
                //window.location= ('/Home/ManageTask/');
            });
        }
    });
}
function status_button_preparation(){
    $("#not_started").click(function(){
        $(this).addClass("selected");
        $('#started').removeClass("selected");
        $('#over_due').removeClass("selected");
        $('#complete').removeClass("selected");
    });
    $("#started").click(function(){
        $(this).addClass("selected");
        $('#not_started ').removeClass("selected");
        $('#over_due').removeClass("selected");
        $('#complete').removeClass("selected");
    });
    $("#over_due").click(function(){
        $(this).addClass("selected");
        $('#complete').removeClass("selected");
        $('#not_started').removeClass("selected");
        $('#started').removeClass("selected");
    });
    $("#complete").click(function(){
        $(this).addClass("selected");
        $('#started').removeClass("selected");
        $('#over_due').removeClass("selected");
        $('#not_started').removeClass("selected");
    });
}
function recursivelyAddSection(_this){
    var fatherHeirarchy = $(_this).attr("data-level");
    var father = $(_this).children("option:selected").text();
    if(father == "")
        return;
    if(father == "Choose..."){
        for(var i = 0; i < lowest_section; i++){
            $("#sectiongroup select.section:last-child").remove();
        }
        lowest_section = 0
        return;
    }
    if(father == "No Parent"){
        for(var i = 0; i < lowest_section; i++){
            $("#sectiongroup select.section:last-child").remove();
        }
        isAtLowestSection = true;
        $("#section-flag").removeClass("unfilled");
        $("#section-flag").addClass("filled");
    }
    if(father == "No More"){
        for(var i = 0; i < lowest_section; i++){
            $("#sectiongroup select.section:last-child").remove();
        }
        isAtLowestSection = true;
        $("#section-flag").removeClass("unfilled");
        $("#section-flag").addClass("filled");
    }
    var current_section = (fatherHeirarchy.split(".").length - 1)
    if(current_section < lowest_section){
        for(var i = current_section + 1; i <= lowest_section; i++){
            $("#sectiongroup select.section:last-child").remove();
        }
        lowest_section = current_section
    }

    $.ajax({
        url:'Get_RequirementSections/',
        dataType : "json",
        data : {
            section : (fatherHeirarchy+father).replace(/ /g,'_')
        },
        success: function( json ) {
            if(json.length != 1){
                jQuery('<select/>',{
                    'class':'section',
                    'data-level':fatherHeirarchy+father+'.',
                    change: function(){
                        isAtLowestSection = false;
                        recursivelyAddSection(this);
                        $("#section-flag").removeClass("filled");
                        $("#section-flag").addClass("unfilled");
                    }
                }).appendTo('#sectiongroup');

                //$(".section[data-level='"+fatherHeirarchy+father+".']").append("<option>Choose...</option>");

                var once = true;
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
                $.each(json, function(i, value) {
                    if(i == 0)return;
                    if(once){
                        lowest_section+=1
                        once = false
                    }
                    $(".section[data-level='"+fatherHeirarchy+father+".']").append($('<option>').text(value).attr('value', value));
                });
                $(".section[data-level='"+fatherHeirarchy+father+".']").append("<option>No More</option>");
            }else{
                isAtLowestSection = true;
                $("#section-flag").removeClass("unfilled");
                $("#section-flag").addClass("filled");
            }
        }
    });
}

function addingSections(){
    //Sections
    $.ajax({
        url:'Get_RequirementSections/',
        dataType : "json",
        data : {
            section : ''
        },
        success: function( json ) {
            if(json.length > 1)
                for(var i = 1; i < json.length; i++)
                    json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                if(i == 0)return;
                $(".section[data-level='']").append($('<option>').text(value.replace(/_/g,'-')).attr('value', value.replace(/_/g,'-')));
            });
        }
    });
    $(".section[data-level='']").append($('<option>').text('No Parent'));
    $(".section[data-level='']").change(function(){
        isAtLowestSection = false;
        recursivelyAddSection(this);
        $("#section-flag").removeClass("filled");
        $("#section-flag").addClass("unfilled");
    });

    //Features
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
        }
    });
    $(".feature[data-level='']").change(function(){
        isAtLowestFeature = false;
        recursivelyAddFeature(this);
        $("#feature-flag").removeClass("filled");
        $("#feature-flag").addClass("unfilled");
    });

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
            }
        }
    });
}

