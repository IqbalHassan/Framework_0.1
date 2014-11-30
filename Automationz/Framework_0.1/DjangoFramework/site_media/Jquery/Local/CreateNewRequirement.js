

var createpath="CreateRequirement/";
var editpath="EditRequirement/";
var childpath="ChildRequirement/";
var operation = 1;
var req_id = "";
var sectionpath = "";



var lowest_section = 0;
var isAtLowestSection = false;
var lowest_feature = 0;
var isAtLowestFeature = false;


$(document).ready(function(){

    AutoCompleteTask();

    var URL=window.location.pathname;
    var create_index=URL.indexOf(createpath);
    var edit_index=URL.indexOf(editpath);
    var child_index=URL.indexOf(childpath);
    var template = URL.length > (URL.lastIndexOf("/")+1) && URL.indexOf(createpath) != -1;
    if(create_index != -1){

        $("#header").html($.session.get('project_id')+' / Create Requirement');
    }

    if(edit_index!=-1){
        var referred_req=URL.substring((URL.lastIndexOf(editpath)+(editpath).length),(URL.length-1));
        $("#header").html($.session.get('project_id')+' / Edit Requirement / '+referred_req);
        PopulateReqInfo(referred_req);
        operation=2;
        req_id = referred_req;
    }
    if(child_index!=-1){
        var referred_req=URL.substring((URL.lastIndexOf(childpath)+(childpath).length),(URL.length-1));
        $("#header").html($.session.get('project_id')+' / Create Child Requirement');
        //PopulateReqInfo(referred_req);
        operation=3;
        sectionpath = referred_req;
    }

    //Button Preparation
    addingSections();
    //status_button_preparation();
    $('#project_id').text($.session.get('project_id'));
    $('#starting_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#ending_date').datepicker({ dateFormat: "yy-mm-dd" });

    if(edit_index != -1 && template){

    }
    if(!template){
        $('#form_parent_selection').css({'display':'none'});
    }
    else{
        $('#form_parent_selection').css({'display':'block'});
    }
    $('#submit').click(function(){

        /*if($('#feature-flag').hasClass('unfilled')){
         alertify.error("Feature Path is not defined Correctly","",0);
         return false;
         }*/

        //get the statuses
        //var status="";
        /*if($('a[value="not_started"]').hasClass('selected'))
         status = "not_started";
         if($('a[value="started"]').hasClass('selected'))
         status = "started";
         if($('a[value="complete"]').hasClass('selected'))
         status = "complete";
         if($('a[value="over_due"]').hasClass('selected'))
         status = "over_due";*/
        var status = $("#status").val();
        //var requirement_description="";
        var requirement_description=$('#description').val();
        //var start_date="";
        var start_date=$('#starting_date').val();
        //var end_date="";
        var end_date=$('#ending_date').val();
        var team=[];
        $('input[name="team"]:checked').each(function(){
            team.push($(this).val());
        });
        //var priority="";
        var priority=$('input[name="priority"]:checked').val();
        var milestone=$('#milestone option:selected').val();
        var title=$('#title').val();
        var newFeaturePath = $("#featuregroup select.feature:last-child").attr("data-level").replace(/ /g,'_') + $("#featuregroup select.feature:last-child option:selected").val().replace(/ /g,'_');

        var labels=[];
        $('input[name="labels"]:checked').each(function(){
            labels.push($(this).val());
        });

        var tasks=[];
        $('input[name="tasks"]:checked').each(function(){
            tasks.push($(this).val());
        });


        if(operation==1){
            $.get("SubmitCreateRequirement/",{
                'title':title.trim(),
                'description':requirement_description.trim(),
                'status':status.trim(),
                'start_date':start_date.trim(),
                'end_date':end_date.trim(),
                'team':team.join("|").trim(),
                'priority':priority.trim(),
                'milestone':milestone.trim(),
                'project_id': $.session.get('project_id'),
                'user_name':$.session.get('fullname'),
                'feature_path':newFeaturePath,
                'labels':labels.join("|"),
                'tasks':tasks.join("|")
            },function(data){
                window.location=('/Home/'+ $.session.get('project_id')+'/EditRequirement/'+data);
            });
        }
        else if(operation==2){
            $.get("SubmitEditRequirement/",{
                'req_id':req_id,
                'title':title.trim(),
                'description':requirement_description.trim(),
                'status':status.trim(),
                'start_date':start_date.trim(),
                'end_date':end_date.trim(),
                'team':team.join("|").trim(),
                'priority':priority.trim(),
                'milestone':milestone.trim(),
                'project_id': $.session.get('project_id'),
                'user_name':$.session.get('fullname'),
                'feature_path':newFeaturePath,
                'labels':labels.join("|"),
                'tasks':tasks.join("|")
            },function(data){
                window.location=('/Home/'+ $.session.get('project_id')+'/EditRequirement/'+data);
            });
        }
        else if(operation==3){
            $.get("SubmitChildRequirement/",{
                'title':title.trim(),
                'description':requirement_description.trim(),
                'status':status.trim(),
                'start_date':start_date.trim(),
                'end_date':end_date.trim(),
                'team':team.join("|").trim(),
                'priority':priority.trim(),
                'milestone':milestone.trim(),
                'project_id': $.session.get('project_id'),
                'user_name':$.session.get('fullname'),
                'feature_path':newFeaturePath,
                'requirement_id':sectionpath,
                'labels':labels.join("|"),
                'tasks':tasks.join("|")
            },function(data){
                window.location=('/Home/'+ $.session.get('project_id')+'/EditRequirement/'+data);
            });
        }
    });
});

function PopulateReqInfo(req_id){

    $("#relation").show();
    $("#create_child").click(function(){
        window.location = '/Home/'+$.session.get('project_id')+'/ChildRequirement/'+req_id
    });

    $.get("Selected_Requirement_Analaysis",{req_id : req_id},function(data) {
        $("#title").val(data['Req_Info'][0][0]);
        $("#status").val(data['Req_Info'][0][1]);
        $("#description").val(data['Req_Info'][0][2]);

        $('input[name="team"]').each(function(){
            $(this).prop('checked',false);
        });
        $('input[name="team"]').each(function(){
            if(data['teams'].indexOf($(this).val())>-1){
                $(this).prop('checked',true);
            }
        });

        $("#starting_date").val(data['Req_Info'][0][3]);
        $("#ending_date").val(data['Req_Info'][0][4]);

        $('input[name="priority"]').each(function(){
            $(this).prop('checked',false);
        });
        $('input[name="priority"]').each(function(){
            if(data['Req_Info'][0][5]==$(this).val()){
                $(this).prop('checked',true);
            }
        });

        $("#milestone").val(data['Req_Info'][0][6]);

        $('input[name="labels"]').each(function(){
            $(this).prop('checked',false);
        });
        $('input[name="labels"]').each(function(){
            if(data['labels'].indexOf($(this).val())>-1){
                $(this).prop('checked',true);
            }
        });



        $(data['tasks']).each(function(i){
            $(".task_linking").append('<tr>' +
            '<td><!--img class="delete" id = "DeleteCase" title = "TestCaseDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/--></td>'
            + '<td>'
            + '<input type="checkbox" checked="true" name="tasks" value="'
            + data['tasks'][i][0]
            + '"/>' +
            '</td><td>'
            + data['tasks'][i][1]
            + "</td>" +
            "</tr>");
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
                                    //$("#feature-flag").removeClass("filled");
                                    //$("#feature-flag").addClass("unfilled");
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
                        //$("#feature-flag").removeClass("unfilled");
                        //$("#feature-flag").addClass("filled");
                    }
                }
            });

            dataId += featureArray[index] + '.'
        }


    });

}
/*function status_button_preparation(){
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
}*/


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

function AutoCompleteTask(){
    $('.search_task').autocomplete({
        source:function(request,response){
            $.ajax({
                url:"AutoCompleteTask/",
                dataType:"json",
                data:{
                    term:request.term,
                    project_id:$.session.get('project_id')
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select:function(request,ui){
            console.log(ui);
            var id=ui.item[0].trim();
            var name=ui.item[1].trim();
            if(id!=""){
                $(".task_linking").append('<tr>' +
                '<td><!--img class="delete" id = "DeleteCase" title = "TestCaseDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/--></td>'
                + '<td>'
                + '<input type="checkbox" checked="true" name="tasks" value="'
                + id
                + '"/>' +
                '</td><td>'
                + name
                + "</td>" +
                "</tr>");
            }
            return false;
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "<strong> - " + item[1] + "</strong></a>" )
            .appendTo( ul );
    };
    $(".search_task").keypress(function(event) {
        if (event.which == 13) {
            event.preventDefault();

        }
    });
}
