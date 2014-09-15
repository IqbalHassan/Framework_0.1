/**
 * Created by Admin on 9/9/14.
 */
$(document).ready(function(){
    get_all_dependency();
    set_button_behaviour();
});
function get_all_dependency(){
    var project_id= $.session.get('project_id')
    var team_id= $.session.get('default_team_identity')
    $.get("get_all_dependency/",{
        'project_id':project_id.trim(),
        'team_id':team_id.trim()
    },function(data){
        $('#dependency_list').html(make_table(data));
    });
}
function make_table(data){
    var message="";
    message+='<table>';
    for(var i=0;i<data.length;i++){
        message+=('<tr><td>'+data[i]+'</td></tr>');
    }
    message+='</table>';
    return message;
}
function set_button_behaviour(){
    $('#default_team_identity').on('change',function(){
        $.session.set('default_team_identity',$(this).val().trim());
        window.location=('/Home/AssignSettings/');
    });
    $('#project_identity').on('change',function(){
        $.session.set('project_id',$(this).val().trim());
        window.location=('/Home/AssignSettings/');
    });
    $('#new_dependency_button').on('click',function(){
        $(this).css({'display':'none'});
        $('#name_row').css({'margin-left':'45%'});
        $('#name_row').slideDown('slow');
        $('#button_row').slideDown('slow');
    });
    $('#new_dependency_cancel').on('click',function(){
        $('#button_row').css({'display':'none'});
        $('#name_row').css({'display':'none'});
        $('#new_dependency_button').css({'display':'block'});
    });
    $('#new_dependency_submit').on('click',function(){
        var dependency=$('#new_dependency_name').val().trim();
        var project_id=$('#project_identity option:selected').val().trim();
        var team_id=$('#default_team_identity option:selected').val().trim();

        $.get("enlist_new_dependency/",{
            dependency:dependency.trim(),
            project_id:project_id.trim(),
            team_id:team_id.trim()
        },function(data){

        });
    });
}