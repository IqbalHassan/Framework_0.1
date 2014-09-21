/**
 * Created by Admin on 9/9/14.
 */
$(document).ready(function(){
    var project_id= $.session.get('project_id').trim();
    var team_id= $.session.get('default_team_identity').trim();
    get_all_dependency(project_id,team_id);
    button_work();
});
function button_work(){
    $('#createNew').click(function(event){
        event.preventDefault();
        if($('#bit_version').attr('value')!="" || $('#bit_version').attr('value')!=undefined){
           var message=InputVersion($('#bit_version').attr('value'));
            alertify.confirm(message,function(e,str){
                if(e){
                }
                else{
                }
            });
        }
    });
}
function InputVersion(name){
    var message="";
    message+='<table width="100" align="center">';
    message+='<tr><td>Name:</td><td>'+name+'</td></tr>';
    message+='<tr><td>Bit:</td><td><select id="Bit"><option value="32">32</option><option value="64">64</option> </select></td></tr>';
    message+='</table>';
    return message;
}
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
            $('#name_tab').attr('value','');
            $('#bit_version').attr('value','');
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
                    $('#bit_version').html("");
                    $('#bit_version').attr('value','');
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
                        $('#bit_version').attr('value',value);
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
