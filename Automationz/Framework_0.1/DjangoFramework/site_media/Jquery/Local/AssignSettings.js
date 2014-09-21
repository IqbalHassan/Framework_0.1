/**
 * Created by Admin on 9/9/14.
 */
/*$(document).ready(function(){
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
    message+='<table class="ScheduledLeaveCalendar">' +
            '<thead>' +
                '<th>Type</th>' +
                '<th>Name</th>' +
                '<th>Bit</th>' +
                '<th>Version</th>' +
                '<th>&nbsp;</th>' +
                '<th>&nbsp;</th>' +
                '<th>Add</th>' +
            '</thead>';
    for(var i=0;i<data.length;i++){
        var sub_array=data[i];
        message+='<tr>';
        message+=('<td><b>'+sub_array[0]+'</b></td>');
        var browser_tuple=sub_array[1];
        if (browser_tuple.length<0){
            message+=('<td colspan="5">&nbsp;</td>');
        }
        else{
            message+=('<td colspan="5"><table width="100%">');
            for(var j=0;j<browser_tuple.length;j++){
                message+=('<tr>');
                message+=('<td style="padding-right: 20%;">'+browser_tuple[j][0]+'</td>');
                if(browser_tuple[j][1].length>0){
                    message+=('<td colspan="4"><table width="100%">');
                    for(var k=0;k<browser_tuple[j][1].length;k++){
                        message+=('<tr>');
                        message+=('<td>'+browser_tuple[j][1][k][0]+'</td>');
                        message+=('<td><table width="100%">');
                        var version_list=browser_tuple[j][1][k][1].split(",");
                        for(var l=0;l<version_list.length;l++){
                            message+=('<tr><td>'+version_list[l]+'</td></tr>');
                        }
                        message+=('</table></td>');
                        message+=('</tr>');
                    }
                    message+=('</table></td>');
                }
                else{
                    message+=('<td colspan="2">&nbsp;</td>')
                }
                message+=('<td><table width="100%"><tr><td width="50%"><a class="notification-indicator tooltipped downwards" data-gotokey="n"><span id="type-flag" class="mail-status unfilled"></span></a></td><td width="50%"><input type="button" value="make default"/></td></tr></table></td>')
                message+=('</tr>');
            }
            message+=('</table></td> ');
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
}*/

$(document).ready(function(){
    var project_id= $.session.get('project_id').trim();
    var team_id= $.session.get('default_team_identity').trim();
    get_all_dependency(project_id,team_id);
});
function get_all_dependency(project_id,team_id){
    $.get('get_all_dependency',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        var team_name=data['team_name'][0];
        $('#team_id').html('<b>'+project_id+'<br>'+team_name+'</b>');
        $('#dependency_tab').html(populate_upper_div(data['dependency_list']));
        $('#unused_tab').html(populate_lower_div(data['unused_list']));
        $('.dependency').on('click',function(){
            $('.dependency').css({'background':'none'});
            $('.dependency').removeClass('selected');
            $(this).css({'background':'#ccc'});
            $(this).addClass('selected');
            var value=$(this).attr('value');
            $.get('get_all_names_dependency',{
               'project_id':project_id,
                'team_id':team_id,
                'selected_dependency':value
            },function(data){
                $('#name_tab').attr('value',value);
                $('#bit_version').html("");
                var name_list=data['name_list'];
                $('#name_tab').html(populate_name_div(name_list));
                $('.name').click(function(){
                    $('.name').css({'background':'none'});
                    $(this).css({'background':'#ccc'});
                    var value=$(this).attr('value');
                    $.get('get_all_version_dependency',{
                        'project_id':project_id,
                        'team_id':team_id,
                        'selected_dependency':$('#name_tab').attr('value'),
                        'selected_name':value
                    },function(data){
                        var name_list=data['version_list'];
                        $('#bit_version').html(populate_version_list(name_list));

                    });
                });
            });
        });
    });
}
function populate_version_list(array_list){
    var message="";
    message+='<table width="100%" class="one-column-emphasis">';
    for(var i=0;i<array_list.length;i++){
        message+='<tr><td  style="cursor:pointer;">'+array_list[i][0]+'</td>';
        message+='<td><table width="100%" style="border-top: none;">';
        var version_list=array_list[i][1].split(",");
        for(var j=0;j<version_list.length;j++){
            message+='<tr><td>'+version_list[j]+'</td></tr>';
        }
        message+='</table></td>'
        message+='</tr>';
    }
    message+='</table>';
    return message;
}
function populate_name_div(array_list){
    var message="";
    message+='<table width="100%" class="one-column-emphasis">';
    for(var i=0;i<array_list.length;i++){
        message+=('<tr><td  style="cursor:pointer;" class="name" value="'+array_list[i][0]+'">'+array_list[i][1]+'</td></tr>');
    }
    message+='</table>';
    return message;
}
function populate_lower_div(array_list){
    var message="";
    message+='<table width="100%" class="one-column-emphasis">';
    for(var i=0;i<array_list.length;i++){
        message+='<tr>';
        message+='<td>'+array_list[i][1]+'</td>';
        message+='<td value="'+array_list[i][0]+'"><a class="button primary">Add</a></td>';
        message+='</tr>';
    }
    message+='</table>';
    return message;
}
function populate_upper_div(array_list){
    var message="";
    message+='<table width="100%" class="one-column-emphasis">';
    for(var i=0;i<array_list.length;i++){
        message+=('<tr><td  style="cursor:pointer;" class="dependency" value="'+array_list[i][0]+'">'+array_list[i][1]+'</td></tr>');
    }
    message+='</table>';
    return message;
}
