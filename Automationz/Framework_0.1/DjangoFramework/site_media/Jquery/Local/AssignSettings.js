/**
 * Created by Admin on 9/9/14.
 */
var dep="";
var nam="";
$(document).ready(function(){
    var project_id= $.session.get('project_id').trim();
    var team_id= $.session.get('default_team_identity').trim();
    get_all_dependency(project_id,team_id);
    button_work();
});

function button_work(){
    $('#createNew').click(function(){
        var message=InputDependency();
        alertify.confirm(message,function(e,str){
            if(e){
                var name=$('#dependency_name').val().trim();
                var project_id=$('#project_identity').val().trim();
                var team_id=$('#default_team_identity').val().trim();
                $.get("register_new_dependency",{
                    'name':name.trim()
                },function(data){
                    if(data['message']==true){
                        alertify.success(data['log_message']);
                        get_all_dependency(project_id,team_id);
                    }
                    else{
                        alertify.error(data['log_message'],3000);
                    }
                });
            }
            else{

            }
        });
    });
    $('#project_identity').on('change',function(){
        var team_id=$('#default_team_identity option:selected').val().trim();
        get_all_dependency($(this).val().trim(),team_id);
    });
    $('#default_team_identity').on('change',function(){
        var project_id=$('#project_identity option:selected').val().trim();
        get_all_dependency(project_id,$(this).val().trim());
    });
}
function InputDependency(){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td align="right"><b>Name:</b></td><td align="left"><input class="textbox" id="dependency_name"/></td></tr>'
    message+='</table>';
    return message;
}
function get_all_dependency(project_id,team_id){
    $.get('get_all_dependency',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        var team_name=data['team_name'][0];
        $('#dependency_tab').html(populate_upper_div(data['dependency_list'],project_id,team_name));
        $('#unused_tab').html(populate_lower_div(data['unused_list']));
        $('#name_tab').attr('value','');
        $('#name_tab').html("");
        $('#bit_version').attr('value','');
        $('#bit_version').html('');
        $('.dependency').on('click',function(){
            dep=$(this).text().trim();
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
                        //$('#bit_version').attr('value',value);
                        $('#bit_version').html(populate_version_list(name_list));

                    });
                });
                $('.name').bind("contextmenu",function(eventy){
                    eventy.preventDefault();
                    $(this).trigger('click');
                    $(".custom-menu-name").toggle(100).
                        // In the right position (the mouse)
                        css({
                            top: event.pageY + "px",
                            left: event.pageX + "px"
                        });
                    nam=$(this).text().trim();
                });
                $(document).bind("mousedown", function (e) {
                    console.log(!$(e.target).parents(".custom-menu").length > 0);
                    if (!$(e.target).parents(".custom-menu").length > 0)
                        $(".custom-menu").hide(100);
                });

                $(".custom-menu-name li").click(function(){
                    $(".custom-menu").hide();
                    switch($(this).attr("data-action")) {
                        case "version": inputVersion(dep,nam,project_id,team_id); break;
                        case "rename":inputRenameVersion(nam,project_id,team_id); break;
                        case "delete": alert("third"); break;
                    }

                });
            });
        });
        $(".dependency").bind("contextmenu", function (event) {
            // Avoid the real one
            event.preventDefault();
            // Show contextmenu
            $(this).trigger('click');
            $(".custom-menu-dependency").toggle(100).
                // In the right position (the mouse)
                css({
                    top: event.pageY + "px",
                    left: event.pageX + "px"
                });
            dep=$(this).text().trim();
        });

        // If the document is clicked somewhere
        $(document).bind("mousedown", function (e) {
            console.log(!$(e.target).parents(".custom-menu").length > 0);
            if (!$(e.target).parents(".custom-menu").length > 0)
                $(".custom-menu").hide(100);
        });

        $(".custom-menu-dependency li").click(function(){
            $(".custom-menu").hide();
            switch($(this).attr("data-action")) {
                case "first": takeInputForNewName(dep,project_id,team_id); break;
                case "second":takeInputForRename(dep,project_id,team_id); break;
                case "third": alert("third"); break;
            }

        });
        $('.add_dependency').on('click',function(){
            $.get("link_with_project_team",{
                project_id:project_id,
                team_id:team_id,
                dependency:$(this).attr('value')
            },function(data){
                if(data['message']==true){
                    alertify.success(data['log_message']);
                    get_all_dependency(project_id,team_id);
                }
                else{
                    alertify.error(data['log_message']);
                }
            });
        });
    });
}
function inputRenameVersion(nam,project_id,team_id){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td align="right"><b>Old Name:</b></td><td><input type="text" class="textbox" id="old_name" value="'+nam+'"style="width:100%" readonly="readonly" /></td></tr>'
    message+='<tr><td align="right"><b>New Name:</b></td><td><input type="text" class="textbox" id="new_name" style="width:100%"/></td></tr>';
    message+='</table>'
    alertify.confirm(message,function(e){
        if(e){
            var old_name=$('#old_name').val().trim();
            var new_name=$('#new_name').val().trim();
            $.get('rename_name',{
                'old_name':old_name,
                'new_name':new_name
            },function(data){
                if(data['message']==true){
                    alertify.success(data['log_message']);
                    get_all_dependency(project_id,team_id);
                }
                else{
                    alertify.error(data['log_message']);
                }
            });
        }
        else{

       }
    });
}
function inputVersion(dep,name,project_id,team_id){
    var message="";
    message+='<table width="100%" align="center">';
    message+='<tr><td align="right"><b>Type:</b></td><td align="left"><b>'+dep+'</b></td></tr>';
    message+='<tr><td align="right"><b>Name:</b></td><td align="left" id="name"><b>'+name+'</b></td></tr>';
    message+='<tr><td align="right"><b>Bit:</b></td><td align="left"><select id="bit"><option value="32">32 Bit</option><option value="64">64 Bit</option></select></td></tr>';
    message+='<tr><td align="right"><b>Version:</b></td><td align="left"><input id="version" type="text" class="textbox" style="width:100%;"/></td></tr>';
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            var dependency=$('#name_tab').attr('value');
            var name=$('#name').text().trim();
            var bit=$('#bit option:selected').val().trim();
            var version=$('#version').val().trim();

            $.get('add_new_version',{
                dependency:dependency,
                name:name,
                bit:bit,
                version:version
            },function(data){
                if(data['message']==true){
                    alertify.success(data['log_message']);
                    get_all_dependency(project_id,team_id);
                }
                else{
                    alertify.error(data['log_message']);
                }
            });
        }
        else{

        }
    });
}
function takeInputForRename(dep,project_id,team_id){
    var message="";
    message+='<table width="100%">';
    message+='<tr><td align="right"><b>Old Name:</b></td><td><input type="text" class="textbox" id="old_name" value="'+dep+'"style="width:100%" readonly="readonly" /></td></tr>'
    message+='<tr><td align="right"><b>New Name:</b></td><td><input type="text" class="textbox" id="new_name" style="width:100%"/></td></tr>';
    message+='</table>'
    alertify.confirm(message,function(e){
        if(e){
            var old_name=dep.trim();
            var new_name=$('#new_name').val().trim();
            $.get("rename_dependency",{
                old_name:old_name.trim(),
                new_name:new_name.trim()
            },function(data){
                if(data['message']==true){
                    alertify.success(data['log_message']);
                    get_all_dependency(project_id,team_id);
                }
                else{
                    alertify.error(data['log_message']);
                }

            });
        }
        else{

        }
    });
}
function takeInputForNewName(dep,project_id,team_id){
    var message="";
    message+='<table>';
    message+='<tr>';
    message+='<td align="right"><b>Dependency Name:</b></td>';
    message+='<td align="left"><b id="dependency">'+dep+'</b></td>';
    message+='</tr>';
    message+='<tr>';
    message+='<td align="right"><b>Name:</b></td>';
    message+='<td align="left"><input id="name" type="text" class="textbox" style="width:100%;"/></td>';
    message+='</tr>';
    message+='<tr><td align="right"><b>Bit:</b></td><td align="left"><select id="bit"><option value="32">32 Bit</option><option value="64">64 Bit</option></select></td></tr>';
    message+='<tr><td align="right"><b>Version:</b></td><td align="left"><input id="version" type="text" class="textbox" style="width:100%;"/></td></tr>';
    message+='</table>';
    alertify.confirm(message,function(e){
       if(e){
           var dependency=$('#dependency').text().trim();
           var name=$('#name').val().trim();
           var bit=$('#bit option:selected').val().trim();
           var version=$('#version').val().trim();
           $.get('enlist_new_name',{
               dependency:dependency,
               name:name,
               version:version,
               bit:bit
           },function(data){
                if(data['message']==true){
                    alertify.success(data['log_message'],1500);
                    get_all_dependency(project_id,team_id);
                }
                else{
                    alertify.error(data['log_message'],1500);
                }
           });
       }
       else{

       }
    });
}
function populate_version_list(array_list){
    if(array_list.length==0){
        var message="";
        message+='<table width="100%" class="one-column-emphasis">';
        message+='<tr><td><b>No Bit/Version is found</b></td></tr>'
        message+='</table> ';
        return message;
    }
    else{
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
}
function populate_name_div(array_list){
    if(array_list.length==0){
        var message="";
        message+='<table width="100%" class="one-column-emphasis">';
        message+='<tr><td><b>No Name is found</b></td></tr>'
        message+='</table> ';
        return message;
    }
    else{
        var message="";
        message+='<table width="100%" class="one-column-emphasis">';
        for(var i=0;i<array_list.length;i++){
            message+=('<tr><td  style="cursor:pointer;" class="name" value="'+array_list[i][0]+'">'+array_list[i][1]+'</td></tr>');
        }
        message+='</table>';
        return message;
    }
}
function populate_lower_div(array_list){
    var message="";
    message+='<table width="100%" class="one-column-emphasis">';
    for(var i=0;i<array_list.length;i++){
        message+='<tr>';
        message+='<td>'+array_list[i][1]+'</td>';
        message+='<td><a class="button primary add_dependency" value="'+array_list[i][0]+'">Add</a></td>';
        message+='</tr>';
    }
    message+='</table>';
    return message;
}
function populate_upper_div(array_list,project_id,team_name){
    if(array_list.length==0){
        $('#team_id').html('<b>'+project_id+'<br>'+team_name+'</b>');
        var message="";
        message+='<tr><td><b>No Dependency is Found</b></td></tr>'
        return message;
    }
    else{
        $('#team_id').html('<b>'+project_id+'<br>'+team_name+'</b>');
        var message="";
        message+='<table width="100%" class="one-column-emphasis">';
        for(var i=0;i<array_list.length;i++){
            message+=('<tr><td  style="cursor:pointer;" class="dependency" value="'+array_list[i][0]+'">'+array_list[i][1]+'</td></tr>');
        }
        message+='</table>';
        return message;
    }

}
