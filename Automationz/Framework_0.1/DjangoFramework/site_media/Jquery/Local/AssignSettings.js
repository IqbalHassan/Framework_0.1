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
    message+='<table>' +
            '<thead>' +
                '<td><b class="Text">Type</b></td>' +
                '<td><b class="Text">Name</b></td>' +
                '<td><b class="Text">Bit</b></td>' +
                '<td><b class="Text">Version</b></td>' +
                '<td>&nbsp;</td>' +
            '</thead>';
    for(var i=0;i<data.length;i++){
        var sub_array=data[i];
        message+='<tr>';
        message+=('<td><b>'+sub_array[0]+'</b></td>');
        var browser_tuple=sub_array[1];
        if (browser_tuple.length<0){
            message+=('<td colspan="4">&nbsp;</td>');
        }
        else{
            message+=('<td colspan="3">');
            message+=('<table>');
            for(var j=0;j<browser_tuple.length;j++){
                message+=('<tr>');
                message+=('<td>'+browser_tuple[j][0]+'</td>');
                message+=('<td>');
                message+=('<table>');
                if(browser_tuple[j][1].length>0){
                    for(var k=0;k<browser_tuple[j][1].length;k++){
                        message+=('<tr>');
                        message+=('<td>'+browser_tuple[j][1][k][0]+'</td>');
                        if(browser_tuple[j][1][k][1].length>0){
                            message+=('<td>');
                            message+=('<table>');
                            var version_list=browser_tuple[j][1][k][1].split(",");
                            for(var l=0;l<version_list.length;l++){
                                message+=('<tr><td>'+version_list[l]+'</td></tr>');
                            }
                            message+=('</table>');
                            message+=('</td>');
                        }
                        else{
                            message+=('<td>&nbsp;</td>');
                        }
                        message+=('</tr>');
                    }
                }
                else{
                    message+=('<td colspan="2">&nbsp;</td> ');
                }

                message+=('</table>');
                message+=('</td>');
                message+=('<td><input type="button" value="Mark as default"></td>');
                message+=('</tr>');
            }
            message+=('</table>');
            message+=('</td>');
        }
        message+=('<td><input type="button" value="Add New"></td>');
        message+='</tr>';
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