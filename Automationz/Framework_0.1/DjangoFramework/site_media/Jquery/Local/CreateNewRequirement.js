

var createpath="CreateRequirement";
var editpath="EditRequirement";


var lowest_section = 0;
var isAtLowestSection = false;
var lowest_feature = 0;
var isAtLowestFeature = false;


$(document).ready(function(){
    var URL=window.location.pathname;
    var create_index=URL.indexOf(createpath);
    var edit_index=URL.indexOf(editpath);
    $("#header").html($.session.get('project_id')+' / Create Requirement');
    var template = URL.length > (URL.lastIndexOf("/")+1) && URL.indexOf(createpath) != -1;
    if(create_index != -1 || edit_index != -1){
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
                'labels':labels.join("|")
            },function(data){
                window.location=('/Home/'+ $.session.get('project_id')+'/Requirements/'+data);
            });
        });
    }
});

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

