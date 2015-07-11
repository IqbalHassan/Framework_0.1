/**
 * Created by Raju on 7/11/2015.
 */
var time_out=300000;
var name_field_error="Name field can't be empty";
var dep_value="";
var dep_name="";
var test_case_per_page=5;
function get_all_data(project_id,team_id){
    $.get('get_all_data_dependency_page',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        $('#name_list').empty();
        $('#version_list').empty();
        $('#bread_crumb').empty();
        $('#control_panel').empty();
        $('#branch_version_list').empty();
        $('#branch_control_panel').empty();
        $("#sub_feature_list").empty();
        $("#second_level_feature_list").empty();
        $("#third_level_feature_list").empty();
        $("#feature_control_panel").empty();
        $('#driver_control_panel').empty();
        $('#driver_extended_div').empty();
        $('#driver_pagination_div').empty();
        var dependency_list=data['dependency_list'];
        console.log(dependency_list);
        var  message='';
        message+='<table class="two-column-emphasis">';
        message+='<caption><b style="font-size: 150%;">Dependency Assigned</b></caption>'
        if(dependency_list.length>0){
            for(var i=0;i<dependency_list.length;i++){
                message+='<tr>';
                message+='<td data-id="'+dependency_list[i][0]+'" class="dependency" width=90%;>'+dependency_list[i][1]+'</td>';
                message+='</tr>';
            }
        }
        else{
            message+='<tr><td><b>No Dependency Present</b></td></tr>';
        }
        message+='</table> ';
        $('#dependency_list').html(message);
        $('.dependency').on('click',function(){
            $('.global_dependency').removeClass('selected');
            $('.global_dependency').css({'background-color':'#fff'});
            $('.dependency').removeClass('selected');
            $('.dependency').css({'background-color':'#fff'});
            $(this).addClass('selected');
            $(this).css({'background-color':'#ccc'});
            $('#extended_div').empty();
            $('#pagination_div').pagination('destroy');
            $('#pagination_div').empty();
            get_dependency_under_name($(this).attr('data-id'),project_id,team_id,$(this).text());
        });
        var global_dependency_list=data['unused_dependency_list'];
        var message='';
        message+='<table class="two-column-emphasis">';
        message+='<caption><b style="font-size: 150%;"> Global Dependency</b></caption>';
        if(global_dependency_list.length>0){
            for(var i=0;i<global_dependency_list.length;i++){
                message+='<tr>';
                message+='<td data-id="'+global_dependency_list[i][0]+'" class="global_dependency">'+global_dependency_list[i][1]+'</td>';
                message+='<td class="add_global_dependency"><img src="/site_media/plus1.png" style="cursor: pointer" width="20px" height="20px"/></td>';
                message+='</tr>';
            }
        }
        else{
            message+='<tr><td><b>No Global Dependency</b></td></tr>';
        }
        message+='</table>';
        $('#global_dependency_list').html(message);
        $('.global_dependency').on('click',function(){
            $('.dependency').removeClass('selected');
            $('.dependency').css({'background-color':'#fff'});
            $('.global_dependency').removeClass('selected');
            $('.global_dependency').css({'background-color':'#fff'});
            $(this).addClass('selected');
            $(this).css({'background-color':'#ccc'});
        });
        $('.add_global_dependency').on('click',function(){
            var dependency=$(this).parent().find('td:first-child').attr('data-id');
            link_dependency(dependency,project_id,team_id);
        });

        console.log(data['feature_list']);
        var feature_list=data['feature_list'];
        var message='';
        message+='<table class="two-column-emphasis">';
        message+='<caption><b style="font-size: 150%;">Feature Assigned</b></caption>'
        if(feature_list.length>0){
            for(var i=0;i<feature_list.length;i++){
                message+='<tr><td data-id="'+feature_list[i][0]+'" class="feature" style="cursor:pointer" >'+feature_list[i][1].replace(/_/g,' ')+'</td></tr>';
            }
        }
        else{
            message+=('<tr><td><b>No Feature Found</b></td></tr>')
        }
        message+='</table>';
        $('#feature_list').empty();
        $('#feature_list').html(message);

        $('.feature').on('click',function(){
            $('.feature').css({'background-color':'#fff'});
            $(this).css({'background-color':'#ccc'});
            $('.feature').removeClass('selected');
            $(this).addClass('selected');
            $('#feature_extended_div').empty();
            $('#feature_pagination_div').pagination('destroy');
            $('#feature_pagination_div').empty();
            var feature_id=$(this).attr('data-id');
            var feature=$(this).text().trim();
            get_features(feature_id,project_id,team_id,feature);
        });
        var global_feature_list=data['unused_feature_list'];
        console.log(global_feature_list);
        var message='';
        message+='<table class="two-column-emphasis">';
        message+='<caption><b style="font-size: 150%;">Global Feature</b></caption>';
        if(global_feature_list.length>0){
            for(var i=0;i<global_feature_list.length;i++){
                message+='<tr><td data-id="'+global_feature_list[i][0]+'">'+global_feature_list[i][1].replace(/_/g,' ')+'</td>';
                message+='<td class="add_global_feature"><img src="/site_media/plus1.png" style="cursor: pointer" width="20px" height="20px"/></td>';
            }
        }else{
            message+='<tr><td><b>No Global Feature</b></td></tr>'
        }
        message+='</table>';
        $('#global_feature_list').html(message);
        $('.add_global_feature').on('click',function(){
            var feature_id=$(this).prev().attr('data-id');
            var feature=$(this).prev().text().trim();
            var message='Do you want to link feature <b>'+feature+'</b>?';
            alertify.confirm(message,function(e){
                if(e){
                    $.get('link_feature',{
                        value:feature,
                        project_id:project_id,
                        team_id:team_id
                    },function(data){
                        if(data['message']){
                            alertify.set({ delay: 300000 });
                            alertify.success(data['log_message'],time_out);
                            get_all_data(project_id,team_id);
                        }else{
                            alertify.set({ delay: 300000 });
                            alertify.error(data['log_message'],time_out);
                            get_all_data(project_id,team_id);
                        }
                    });
                }else{
                    alertify.alert().close_all();
                }
            });
        });

        var driver_list=data['driver_list'];
        var message='';
        message+='<table class="two-column-emphasis"><caption><b style="font-size: 150%;">Assigned Driver</b></caption>';
        if(driver_list.length>0){
            for(var i=0;i<driver_list.length;i++){
                message+='<tr><td style="cursor: pointer" class="driver" data-id="'+driver_list[i][0]+'">'+driver_list[i][1].replace(/_/g,' ')+'</td></tr>';
            }
        }
        else{
            message+='<tr><td><b>No Driver Available</b></td></tr>'
        }
        message+='</table>';
        $('#driver_list').html(message);
        $('.driver').on('click',function(){
            $('.driver').removeClass('selected');
            $(this).addClass('selected');
            $('.driver').css({'background-color':'#fff'});
            $(this).css({'background-color':'#ccc'});
            $('#driver_control_panel').empty();
            $('#driver_extended_div').empty();
            $('#driver_pagination_div').pagination('destroy');
            $("#driver_pagination_div").empty();
            var driver_id=$(this).attr('data-id');
            var driver_text=$(this).text().replace(/ /g,'_').trim();
            driver_control_panel(driver_id,driver_text,project_id,team_id);
        });
        var global_driver_list=data['unused_driver_list'];
        var message='';
        message+='<table class="two-column-emphasis">';
        message+='<caption><b style="font-size: 150%;">Global Driver</b></caption>';
        if(global_driver_list.length>0){
            for(var i=0;i<global_driver_list.length;i++){
                message+='<tr><td data-id="'+global_driver_list[i][0]+'">'+global_driver_list[i][1].replace(/_/g,' ')+'</td>';
                message+='<td class="add_global_driver"><img src="/site_media/plus1.png" style="cursor: pointer" width="20px" height="20px"/></td>';
            }
        }else{
            message+='<tr><td><b>No Global Driver</b></td></tr>'
        }
        message+='</table>';
        $('#global_driver_list').html(message);

        $('.add_global_driver').on('click',function(){
            var driver_id=$(this).prev().attr('data-id');
            var driver=$(this).prev().text().replace(/ /g,'_').trim();
            var message='Do you want to link Driver <b>'+driver.replace(/_/g,' ')+'</b>?';
            alertify.confirm(message,function(e){
                if(e){
                    $.get('link_driver',{
                        value:driver,
                        project_id:project_id,
                        team_id:team_id
                    },function(data){
                        if(data['message']){
                            alertify.set({ delay: 300000 });
                            alertify.success(data['log_message'],time_out);
                            get_all_data(project_id,team_id);
                        }else{
                            alertify.set({ delay: 300000 });
                            alertify.error(data['log_message'],time_out);
                            get_all_data(project_id,team_id);
                        }
                    });
                }else{
                    alertify.alert().close_all();
                }
            });
        });

        var branch_list=data['branch_list'];
        var message='';
        message+='<table class="two-column-emphasis">';
        message+='<caption><b style="font-size: 150%;">Assigned Branch</b></caption>';
        if(branch_list.length>0){
            for(var i=0;i<branch_list.length;i++){
                message+='<tr><td data-id="'+branch_list[i][0]+'" class="branch">'+branch_list[i][1]+'</td></tr>';
            }
        }
        else{
            message+='<tr><td><b>No Branch Available</b></td></tr>';
        }
        message+='</table>';
        $('#branch_list').html(message);
        $('.branch').on('click',function(){
            $('.branch').removeClass('selected');
            $(this).addClass('selected');
            $('.branch').css({'background-color':'#fff'});
            $(this).css({'background-color':'#ccc'});
            var branch_id=$(this).attr('data-id');
            var branch=$(this).text().trim();
            get_version(branch_id,project_id,team_id,branch);
        });
        var global_branch_list=data['unused_branch_list'];
        var message='';
        message+='<table class="two-column-emphasis">';
        message+='<caption><b style="font-size: 150%;">Global Branch</b></caption>';
        if(global_branch_list.length>0){
            for(var i=0;i<global_branch_list.length;i++){
                message+='<tr><td data-id="'+global_branch_list[i][0]+'">'+global_branch_list[i][1]+'</td>';
                message+='<td class="add_global_branch"><img src="/site_media/plus1.png" style="cursor: pointer" width="20px" height="20px"/></td>';
            }
        }else{
            message+='<tr><td><b>No Global Branch</b></td></tr>'
        }
        message+='</table>';
        $('#global_branch_list').html(message);

        $('.add_global_branch').on('click',function(){
            var branch_id=$(this).prev().attr('data-id');
            var branch=$(this).prev().text().trim();
            var message='Do you want to link Branch <b>'+branch+'</b>?';
            alertify.confirm(message,function(e){
                if(e){
                    $.get('link_branch',{
                        value:branch_id,
                        project_id:project_id,
                        team_id:team_id
                    },function(data){
                        if(data['message']){
                            alertify.set({ delay: 300000 });
                            alertify.success(data['log_message'],time_out);
                            get_all_data(project_id,team_id);
                        }else{
                            alertify.set({ delay: 300000 });
                            alertify.error(data['log_message'],time_out);
                            get_all_data(project_id,team_id);
                        }
                    });
                }else{
                    alertify.alert().close_all();
                }
            });
        });
    });
}
function get_version(branch_id,project_id,team_id,branch){
    $.get('get_all_version_under_branch',{
        value:branch_id,
        project_id:project_id,
        team_id:team_id
    },function(data){
        var version_list=data['version_list'];

        var message='';
        message+='<table class="two-column-emphasis">';
        if(version_list.length>0){
            for(var i=0;i<version_list.length;i++){
                message+='<tr><td>'+version_list[i]+'</td></tr>';
            }
        }
        else{
            message+='<tr><td><b>No version is found</b></td></tr>';
        }
        message+='</table>';
        $('#branch_version_list').html(message);
        buttonConfig(branch_id,project_id,team_id,branch);
    });
}

function buttonConfig(branch_id,project_id,team_id,branch){
    var message='';
    message+='<input type="button" id="add_branch_version" class="m-btn green" value="Add Version"/> ';
    message+='<input type="button" id="rename_branch" class="m-btn green" value="Rename Branch"/> ';
    message+='<input type="button" class="m-btn red" value="Delete"/> ';
    $('#branch_control_panel').html(message);
    $('#add_branch_version').on('click',function(){
        var message='';
        message+='<table>';
        message+='<tr><td><b>Branch Name:</b></td><td>'+branch+'</td></tr>';
        message+='<tr><td><b>Version:</b></td><td><input style="width: 100%" class="textbox" id="new_version"/></td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var version=$('#new_version').val().trim();
                $.get('add_new_version_branch',{
                    new_name:version,
                    new_value:branch_id
                },function(data){
                    if(data['message']){
                        alertify.set({ delay: 300000 });
                        alertify.success(data['log_message'],time_out);
                        get_all_data(project_id,team_id);
                    }else{
                        alertify.set({ delay: 300000 });
                        alertify.error(data['log_message'],time_out);
                        get_all_data(project_id,team_id);
                    }
                });
            }
            else{
                alertify.alert().close_all();
            }
        });
    });
    $('#rename_branch').on('click',function(){
        var message='';
        message+='<table width="100%;">';
        message+='<tr><td><b>Old Name:</b></td><td>'+branch+'</td></tr>';
        message+='<tr><td><b>New Name:</b></td><td><input id="new_branch" style="width: 100%;" class="textbox"/></td></tr>'
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var new_branch=$("#new_branch").val().trim();
                if(new_branch==''){
                    alertify.set({ delay: 300000 });
                    alertify.error("You can't give empty name");
                    return false;
                }else{
                    $.get('rename_branch',{
                        old_name:branch,
                        new_name:new_branch,
                        project_id:project_id,
                        team_id:team_id
                    },function(data){
                        if(data['message']){
                            alertify.set({ delay: 300000 });
                            alertify.success(data['log_message'],time_out);
                            get_all_data(project_id,team_id);
                        }
                        else{
                            alertify.set({ delay: 300000 });
                            alertify.error(data['log_message']);
                            alertify.alert().close_all();
                        }
                    });
                }
            }else{
                alertify.alert().close_all();
            }
        });
    });
}

$(document).ready(function(){
    $('body').css({'font-size':'100%'});
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    get_all_data(project_id,team_id);
    $('#create_branch').on('click',function(){
        var message='';
        message+='<table>';
        message+='<tr><td><b>Branch Name:</b></td><td><input style="width:100%" class="textbox" placeholder="Branch Name" id="new_branch"/> </td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var branch_name=$('#new_branch').val().trim();
                $.get('add_new_branch',{
                    'name':branch_name,
                    'project_id':project_id,
                    'team_id':team_id
                },function(data){
                    if(data['message']){
                        alertify.set({ delay: 300000 });
                        alertify.success(data['log_message'],time_out);
                        get_all_data(project_id,team_id);
                    }
                    else{
                        alertify.set({ delay: 300000 });
                        alertify.error(data['log_message'],time_out);
                        get_all_data(project_id,team_id);
                    }
                });
            }
            else{
                alertify.alert().close_all();
            }
        });
    });
    //DependencyTabButtons(project_id,team_id);
});
