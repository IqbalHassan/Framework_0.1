/**
 * Created by lent400 on 8/14/14.
 */

var lowest_section = 0;
var isAtLowestSection = false;
$(document).ready(function(){
    $('#project_id').text($.session.get('project_id'));
    addingSections();
});

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

                $(".section[data-level='"+fatherHeirarchy+father+".']").append("<option>Choose...</option>");

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
    $(".section[data-level='']").change(function(){
        isAtLowestSection = false;
        recursivelyAddSection(this);
        $("#section-flag").removeClass("filled");
        $("#section-flag").addClass("unfilled");
    });
}