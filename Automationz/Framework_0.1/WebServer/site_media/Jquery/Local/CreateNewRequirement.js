

var createpath="CreateRequirement/";
var editpath="EditRequirement/";
var childpath="ChildRequirement/";
var operation = 1;
var req_id = "";
var sectionpath = "";

var test_case_per_page=5;
var test_case_page_current=1;
var project_id = $.session.get('project_id');
var team_id = $.session.get('default_team_identity');
var user = $.session.get('fullname');



var lowest_section = 0;
var isAtLowestSection = false;
var lowest_feature = 0;
var isAtLowestFeature = false;


var new_test_step_text = "New Requirement";


$(document).ready(function(){

    $("#title").select2({
        placeholder: "Enter the title...",
//      minimumInputLength: 3,
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "RequirementSearch/",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'project_id': project_id,
                    'team_id': team_id
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
            
            var title = $(this).select2("data")["text"].substr(start, length - 1);
        
            var step_name = $(this).val();
            $("#step_name").val(step_name);
            $("#title_prompt").html(
                    '<p style="text-align: center">You have selected requirement - ' +
                    '<span style="font-weight: bold;">' + step_name + ' - ' + title + '</span>' +
                    '<br/> What do you want to do?' +
                    '</p><br>' +
                    '<div style="padding-left: 18%">' +
                    '<a class="twitter" href="/Home/'+ project_id+'/EditRequirement/'+step_name+'">Edit Requirement</a>' +
                    //'<a class="twitter" href="/Home/ManageTestCases/CreateNew/'+tc_id+'">Copy</a>' +
                    '<a class="dribble" href="#" rel="modal:close">Cancel</a>' +
                    '</div>'
            );
          $("#title_prompt").modal();
          return false;
        }

    });

    function formatTestSteps(step_details) {
        var start = step_details.text.indexOf(":") + 1;
        var length = step_details.text.length;
        
        var title = step_details.text.substr(start, length - 1);
        
        var markup =
            '<div>' +
            '<i class="fa fa-file-text fa-fw"></i> <span style="font-weight: bold;">' + step_details.id + '</span>' +
            ': ' +
            '<span><b>' + title + '</b> - ' + step_details.status + '</span>'+
            '</div>';
        
        return markup;
    }


    AutoCompleteTask();

    $.ajax({
        url:'Get_Filtered_MileStone/',
        dataType : "json",
        data : {
            project_id: project_id,
            team_id: team_id
        },
        success: function( json ) {
            //if(json.length > 0)
                //for(var i = 0; i < json.length; i++)
                    //json[i] = json[i][0].replace(/_/g,' ')
            $.each(json, function(i, value) {
                //if(i == 0)return;
                $(".milestone").append($('<option>').text(value[1]).attr('value', value[0]));
            });
        }
    });

    BugLinking(project_id,team_id);


    $("#searchbox").select2({
        placeholder: "Search & Select Filter Here..",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "AutoCompleteTestCasesSearchTestSet/",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page,
                    'project_id': $.session.get('project_id'),
                    'team_id': $.session.get('default_team_identity')
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        formatResult: formatTestCasesSearch
    }).on("change", function(e) {
        var tag_id=$(this).select2('data')['id'];
        $("#searchedFilter").append('<td><img class="delete" title = "Delete" src="/site_media/deletebutton.png" /></td>'
            + '<td name = "submitquery" class = "Text" style = "size:10">'
            + tag_id
            + ":&nbsp"
            + '</td>'
        );
        PerformSearch(project_id,team_id,test_case_per_page,test_case_page_current);
        DeleteFilterData(project_id,team_id);
        $(this).select2('val','');
        return false;
    });
    function formatTestCasesSearch(test_case_details) {
        var tag_select=test_case_details.text.split(' - ');
        tag_select=tag_select[tag_select.length-1].trim();
        if (tag_select=='Test Case'){
            var markup ='<div><i class="fa fa-file-text-o"></i><span style="font-weight: bold;"><span>' + '  ' + test_case_details.text + '</span></div>';
        }
        else if(tag_select=='Section'){
            var markup ='<div><i class="fa fa-folder-o"></i><span style="font-weight: bold;"><span>' + '  ' + test_case_details.text.replace('Section','Folder') + '</span></div>';
        }
        else{
            var markup ='<div><i class="fa fa-file"></i><span style="font-weight: bold;"><span>' + '  ' + test_case_details.text + '</span></div>';
        }
        return markup;
    }

    Buttons();

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
        /*var team=[];
        $('input[name="team"]:checked').each(function(){
            team.push($(this).val());
        });*/

        var start = $("#title").select2("data")["text"].indexOf(":") + 1;
        var length = $("#title").select2("data")["text"].length;
        
        var title = $("#title").select2("data")["text"].substr(start, length - 1);
        

        //var priority="";
        //var priority=$('input[name="priority"]:checked').val();
        var priority=$('input[name="priority"]:checked').val();
        var milestone=$('.milestone option:selected').val();
        //var title=$('#title').val();
        //var title = $('#title').select2("val");
        var newFeaturePath = $("#featuregroup select.feature:last-child").attr("data-level").replace(/ /g,'_') + $("#featuregroup select.feature:last-child option:selected").val().replace(/ /g,'_');

        var labels=[];
        $('input[name="labels"]:checked').each(function(){
            labels.push($(this).val());
        });

        var tasks=[];
        $('input[name="tasks"]:checked').each(function(){
            tasks.push($(this).val());
        });

        var test_cases=[];
        $('input[name="test_cases"]:checked').each(function(){
            test_cases.push($(this).val());
        });

        var bugs=[];
        $('input[name="bugs"]:checked').each(function(){
            bugs.push($(this).val());
        });

        if($("#title").select2("val") === "" || $("#title").select2("val") === []) {
                //e.preventDefault();
                alertify.set({ delay: 300000 });
                alertify.error("Please provide the <span style='font-weight: bold;'>Requirement title</span>");

                $("#title").select2("open");
                return false;
            }
        /*if(title==""){
            alertify.set({ delay: 300000 });
            alertify.error("Title is empty!");
        }*/
        else if(newFeaturePath.indexOf("Choose")!=-1){
            alertify.set({ delay: 300000 });
            alertify.error("Feature is to be selected to the lowest path!");
        }
        else if(requirement_description==""){
            alertify.set({ delay: 300000 });
            alertify.error("Description is empty!");
        }
        else if(start_date=="" || end_date==""){
            alertify.set({ delay: 300000 });
            alertify.error("Dates are required!");
        }
        else if(milestone==""){
            alertify.set({ delay: 300000 });
            alertify.error("Please select a milestone!");
        }
        else if(operation==1){
            $.get("SubmitCreateRequirement/",{
                'title':title.trim(),
                'description':requirement_description.trim(),
                'status':status.trim(),
                'start_date':start_date.trim(),
                'end_date':end_date.trim(),
                'team':$.session.get('default_team_identity'),
                'priority':priority.trim(),
                'milestone':milestone.trim(),
                'project_id': $.session.get('project_id'),
                'user_name':$.session.get('fullname'),
                'feature_path':newFeaturePath,
                'labels':labels.join("|"),
                'tasks':tasks.join("|"),
                'bugs':bugs.join("|"),
                'test_cases':test_cases.join("|")
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
                'team':$.session.get('default_team_identity'),
                'priority':priority.trim(),
                'milestone':milestone.trim(),
                'project_id': $.session.get('project_id'),
                'user_name':$.session.get('fullname'),
                'feature_path':newFeaturePath,
                'labels':labels.join("|"),
                'tasks':tasks.join("|"),
                'bugs':bugs.join("|"),
                'test_cases':test_cases.join("|")
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
                'team':$.session.get('default_team_identity'),
                'priority':priority.trim(),
                'milestone':milestone.trim(),
                'project_id': $.session.get('project_id'),
                'user_name':$.session.get('fullname'),
                'feature_path':newFeaturePath,
                'requirement_id':sectionpath,
                'labels':labels.join("|"),
                'tasks':tasks.join("|"),
                'bugs':bugs.join("|"),
                'test_cases':test_cases.join("|")
            },function(data){
                window.location=('/Home/'+ $.session.get('project_id')+'/EditRequirement/'+data);
            });
        }
    });
});

function DeleteFilterData(project_id,team_id){
    $('#searchedFilter td .delete').live('click',function(){
        $(this).parent().next().remove();
        $(this).remove();
        PerformSearch(project_id,team_id,test_case_per_page,test_case_page_current);
    });
}

function PopulateReqInfo(req_id){

    $("#relation").show();
    $("#create_child").click(function(){
        window.location = '/Home/'+$.session.get('project_id')+'/ChildRequirement/'+req_id
    });

    $.get("Selected_Requirement_Analaysis",{req_id : req_id},function(data) {
        //$("#title").val(data['Req_Info'][0][0]);
        $("#title").select2("data", {"id": req_id , "text": req_id + ": "+ data['Req_Info'][0][0]});
        $("#title").val(req_id);
        $("#status").val(data['Req_Info'][0][1]);
        $("#description").val(data['Req_Info'][0][2]);

        /*$('input[name="team"]').each(function(){
            $(this).prop('checked',false);
        });
        $('input[name="team"]').each(function(){
            if(data['teams'].indexOf($(this).val())>-1){
                $(this).prop('checked',true);
            }
        });*/

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

        $(".milestone").val(data['Req_Info'][0][6]);

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
            '</td><td>' +
            data['tasks'][i][0] +
            '</td>' +
            '<td>'
            + data['tasks'][i][1]
            + "</td>" +
            '<td>'
            + data['tasks'][i][2]
            + "</td>" +
            '<td>'
            + data['tasks'][i][3]
            + "</td>" +
            '<td>'
            + data['tasks'][i][4]
            + "</td>" +
            '<td>'
            + data['tasks'][i][5]
            + "</td>" +
            '<td>'
            + data['tasks'][i][6]
            + "</td>" +
            "</tr>");
        });


        $(data['bugs']).each(function(i){
            $(".bug_linking").append('<tr>' +
            '<td><!--img class="delete" id = "DeleteCase" title = "TestCaseDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/--></td>'
            + '<td>'
            + '<input type="checkbox" class="Buttons" checked="true" name="bugs" value="'
            + data['bugs'][i][0]
            + '"/>' +
            '</td><td>'
            + data['bugs'][i][0]
            + "</td><td>" +
            data['bugs'][i][1] +
            '</td><td>' +
            data['bugs'][i][2] +
            '</td><td>' +
            data['bugs'][i][3] +
            '</td>' +
            "</tr>");
        });


        get_test_cases(req_id,project_id,team_id,test_case_per_page,test_case_page_current);


        /*$(data['cases']).each(function(i){
            $(".tc_linking").append('<tr>' +
            '<td><!--img class="delete" id = "DeleteCase" title = "TestCaseDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/--></td>'
            + '<td>'
            + '<input type="checkbox" class="Buttons" checked="true" name="test_cases" value="'
            + data['cases'][i][0]
            + '"/>' +
            '</td><td>'
            + data['cases'][i][0]
            + "</td><td>" +
            data['cases'][i][1] +
            "</td>" +
            "</tr>");
        });*/

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
                    project_id:$.session.get('project_id'),
                    team_id: $.session.get('default_team_identity')
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
                '</td><td>' +
                id +
                '</td><td>'
                + name
                + '</td>' +
                '<td>' +
                ui.item[2] +
                '</td>' +
                '<td>' +
                ui.item[3] +
                '</td>' +
                '<td>' +
                ui.item[4] +
                '</td>' +
                '<td>' +
                ui.item[5] +
                '</td>' +
                '<td>' +
                ui.item[6] +
                '</td>' +
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

function BugLinking(project_id,team_id){

    $(".search_bug").autocomplete({

        source:function(request,response){
            $.ajax({
                url:"AutoCompleteBugs/",
                dataType:"json",
                data:{
                    term:request.term,
                    project_id:project_id,
                    team_id:team_id
                },
                success:function(data){
                    response(data);
                }
            });
        },
        select : function(event, ui) {

            //var value = ui.item[0]
            //var name = ui.item[1]

            /*var tc_id_name = ui.item[0].split(" - ");
             var value = "";
             if (tc_id_name != null)
             {
             value = tc_id_name[0].trim();
             name = tc_id_name[1].trim();
             }*/

            var value=ui.item[0].trim();
            //var name=ui.item[1].trim();

            if(value!=""){
                $(".bug_linking").append('<tr>' +
                '<td><!--img class="delete" id = "DeleteCase" title = "TestCaseDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/--></td>'
                + '<td>'
                + '<input type="checkbox" class="Buttons" checked="true" name="bugs" value="'
                + ui.item[0]
                + '"/>' +
                '</td><td>'
                + ui.item[0]
                + "</td><td>" +
                ui.item[1] +
                '</td><td>' +
                ui.item[2] +
                '</td><td>' +
                ui.item[3] +
                '</td>' +
                "</tr>");
            }

            //$(".search_case").remove();

            /*$("#test_cases").append('<tr class="linking">' +
             '<td><input class="search_case textbox" placeholder="Search Test Case" style="width: auto" /></td>' +
             '</tr>');
             TestCaseLinking();*/

            //$("#tester th").css('display', 'block');

            $(".search_bug").val("");
            return false;

        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
            .data( "ui-autocomplete-item", item )
            .append( "<a>" + item[0] + "<strong> - " + item[1] + "</strong></a>" )
            .appendTo( ul );
    };

    $(".search_bug").keypress(function(event) {
        if (event.which == 13) {

            event.preventDefault();

        }
    });
    $("#DeleteCase").live('click', function() {

        $(this).parent().next().remove();
        $(this).remove();

    });
}

function PerformSearch(project_id,team_id,test_case_per_page,test_case_page_current){
    $("#searchedFilter").each(function() {
        var UserText = $(this).find("td").text();
        UserText = UserText.replace(/(\r\n|\n|\r)/gm, "").replace(/^\s+/g, "")
        $.get('TableDataTestCasesOtherPages/',{Query:UserText,test_status_request:false,project_id:project_id,team_id:team_id,
            test_case_per_page:test_case_per_page,
            test_case_page_current:test_case_page_current},function(data){
            if(data['TableData'].length!=0){
                ResultTable("#RunTestResultTable",data['Heading'],data['TableData'],'Test Cases');
                implementDropDown("#RunTestResultTable");
                $('#RunTestResultTable tr>td:nth-child(7)').each(function(){
                    var id=$(this).closest('tr').find('td:first-child').text().trim();
                    $(this).after('<div><input id="'+id+'" type="checkbox" class="Buttons add"/></div>');
                });
                $('#RunTestResultTable').css({'display':'block'});
                $('#add_button').css({'display':'block'});
                $('#pagination_div').pagination({
                    items:data['Count'],
                    itemsOnPage:test_case_per_page,
                    cssStyle: 'dark-theme',
                    currentPage:test_case_page_current,
                    displayedPages:2,
                    edges:2,
                    hrefTextPrefix:'#',
                    onPageClick:function(PageNumber){
                        PerformSearch(project_id,team_id,test_case_per_page,PageNumber);
                    }
                });

            }
            else{
                $('#RunTestResultTable').html('<p style="font-weight: bold; text-align: center;" class="Text">There is no test cases for this filter</p>');
                $('#RunTestResultTable').css({'display':'block'});
                $('#add_button').css({'display':'none'});
                $('#pagination_div').pagination('destroy');
            }
        });
    });
}

function get_test_cases(stepname,project_id,team_id,itemPerPage,PageCurrent){
    //$('#step_name').html("Test cases for step: "+ stepname);
    $.get("TestCases_PerRequirement",{
        Query: stepname,
        test_case_per_page:itemPerPage,
        test_case_page_current:PageCurrent,
        project_id:project_id,
        team_id:team_id,
        test_status_request:true
    },function(data) {
        form_table("usage_div",data['Heading'],data['TableData'],data['Count'],"Test Cases");
        implementDropDown('#usage_div');
        $('#usage_pagination_div').pagination({
            items:data['Count'],
            itemsOnPage:test_case_per_page,
            cssStyle: 'dark-theme',
            currentPage:test_case_page_current,
            displayedPages:2,
            edges:2,
            hrefTextPrefix:'#',
            onPageClick:function(PageNumber){
                get_test_cases(stepname,project_id,team_id,itemPerPage,PageNumber);
            }
        });
        var indx = 0;
        $('#usage_div tr>td:nth-child(7)').each(function(){
            var ID = $("#usage_div tr>td:nth-child(1):eq("+indx+")").text().trim();

            $(this).after('<span style="cursor: pointer; margin-left: 8px;" class="hint--left hint--bounce hint--rounded" data-hint="Copy Test Case"><i class="fa fa-copy fa-2x templateBtn" id="'+ID+'" style="cursor:pointer"></i></span>');
            //$(this).after('&nbsp;&nbsp;');
            $(this).after('<span style="cursor: pointer; margin-left: 8px;" class="hint--left hint--bounce hint--rounded" data-hint="Edit Test Case"><i class="fa fa-pencil fa-2x editBtn" id="'+ID+'" style="cursor:pointer"></i></span>');

            indx++;
        });

        $(".editBtn").click(function (){
            window.location = '/Home/ManageTestCases/Edit/'+ $(this).attr("id");
        });
        $(".templateBtn").click(function (){
            window.location = '/Home/ManageTestCases/CreateNew/'+ $(this).attr("id");
        });
    });
}
function implementDropDown(wheretoplace){
    $(wheretoplace+" tr td:nth-child(1)").css({'color' : 'blue','cursor' : 'pointer'});
    $(wheretoplace+" tr td:nth-child(1)").each(function() {
        var ID=$(this).closest('tr').find('td:nth-child(1)').text().trim();
        var name=$(this).text().trim();
        $(this).html('<div id="'+ID+'name">'+name+'</div><div id="'+ID+'detail" style="display:none;"></div>');
        $.get("TestStepWithTypeInTable",{RunID: ID},function(data) {
            var data_list=data['Result'];
            var column=data['column'];
            ResultTable('#'+ID+'detail',column,data_list,"");
            $('#'+ID+'detail tr').each(function(){
                $(this).css({'textAlign':'left'});
            });
        });
        $(this).live('click',function(){
            $('#'+ID+'detail').slideToggle("slow");
        });
    });
}
function form_table(divname,column,data,total_data,type_case){
    var tooltip=type_case||':)';
    var message='';
    message+= "<p class='Text hint--right hint--bounce hint--rounded' data-hint='" + tooltip + "' style='color:#0000ff; font-size:14px; padding-left: 12px;'>" + total_data + " " + type_case+"</p>";
    message+='<table class="two-column-emphasis">';
    message+='<tr>';
    for(var i=0;i<column.length;i++){
        message+='<th>'+column[i]+'</th>';
    }
    message+='</tr>';
    for(var i=0;i<data.length;i++){
        message+='<tr>';
        
        for(var j=0;j<data[i].length;j++){
            switch(data[i][j]){
                case 'Dev':
                    message+='<td style="background-color: ' + colors['dev'] + '; color: #fff;">' + data[i][j] + '</td>';
                    continue;
                case 'Ready':
                    message+='<td style="background-color: ' + colors['ready'] + '; color: #fff;">' + data[i][j] + '</td>';
                    continue;
                default :
                    message+='<td>'+data[i][j]+'</td>';
                    continue;
            }
        }
        message+='<td>' 
            + '<input type="checkbox" class="Buttons" checked="true" name="test_cases" value="'
            + data[i][0]
            + '"/>' +
            '</td>';
        message+='</tr>';
    }
    message+='</table>';
    $('#'+divname).html(message);
}

function Buttons(){
    $('#add_button').click(function(event){
        event.preventDefault();
        var list=[]
        $('.add:checked').each(function(){
            list.push($(this).attr('id').trim());
        });
        if(list.length==0){
            alertify.log('No Test Case selected',"",0);
            return false;
        }
        else{
            $("#link_new").show();
            $.each(list, function(index, value) {
                $(".tc_linking").append('<tr>' +
                '<td><!--img class="delete" id = "DeleteCase" title = "TestCaseDelete" src="/site_media/delete4.png" style="width: 30px; height: 30px"/--></td>'
                + '<td>'
                + '<input type="checkbox" class="Buttons" checked="true" name="test_cases" value="'
                + value
                + '"/>' +
                '</td><td>'
                + value
                + "</td>" +
                "</tr>");
            });
            /*$.get('AddTestCasesSetTag',{type:type.toLocaleUpperCase().trim(),name:name.trim(),list:list.join('|')},function(data){
                alertify.success(data,"",3);
                var location='/Home/ManageSetTag/'+type+'/'+name+'/';
                window.location=location;
            });*/

        }

    });

}
