/**
 * Created by lent400 on 8/14/14.
 */

var lowest_section = 0;
var isAtLowestSection = false;
$(document).ready(function(){
    $('#project_id').text($.session.get('project_id'));
    $('#starting_date').datepicker({ dateFormat: "yy-mm-dd" });
    $('#ending_date').datepicker({ dateFormat: "yy-mm-dd" });
    addingSections();
    status_button_preparation();
    Submit_button_preparation();
});
function Submit_button_preparation(){
    $('#submit').click(function(){
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
            'user_name':$('#user_name').text().trim()

        },function(data){
            //window.location=('/Home/'+ $.session.get('project_id')+'/Task/'+data);
            window.location= ('/Home/ManageTask/');
        });
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
}