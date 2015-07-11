/**
 * Created by Admin on 9/9/14.
 */
var time_out=300000;
var name_field_error="Name field can't be empty";
var dep_value="";
var dep_name="";
var test_case_per_page=5;
$(document).ready(function(){
    $('body').css({'font-size':'100%'});
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    get_all_data(project_id,team_id);
    $('#create_feature').on('click',function(){
        var message='';
        message+='<table>';
        message+='<tr><td><b style="font-size: 125%;">Feature Name</b> </td></tr>';
        message+='<tr><td><input type="text" class="textbox" id="new_feature"></td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var feature_name=$('#new_feature').val().trim();
                if(feature_name!=''){
                    if(feature_name.indexOf('.')!=-1 || feature_name.indexOf("_")!=-1){
                        alertify.set({ delay: 300000 });
                        alertify.error('You can\'t give "." or "_" in the Feature Name',time_out);
                        return false;
                    }
                    else{
                        $.get('add_new_feature',{
                            feature_path: feature_name.trim(),
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
                                alertify.error(data['log_message'],time_out);
                                get_all_data(project_id,team_id);
                            }
                        });
                    }
                }
                else{
                    return false;
                }
            }
            else{
                alertify.alert().close_all();
            }
        });
    });
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

function get_features(feature_id,project_id,team_id,feature){
    if (feature_id==''){
        var feature_modified=feature;
    }else{
        var feature_modified=(feature_id+'.'+feature).trim();
    }
    $.get('get_all_first_level_sub_feature',{
        'name':feature_modified,
        'team_id':team_id,
        'project_id':project_id
    },function(data){
        var message='';
        message+='<table class="two-column-emphasis">';
        if(data['version_list'].length>0){
            var sub_feature_listing=data['version_list'];
            for(var i=0;i<sub_feature_listing.length;i++){
                message+='<tr>';
                message+='<td data-id="'+sub_feature_listing[i][0]+'" class="sub_feature_first_level">'+sub_feature_listing[i][1].replace(/_/g,' ')+'</td>';
                message+='</tr>';
            }
        }
        else{
            message+='<tr><td><b>No Sub Feature is present</b></td></tr>';
        }
        message+='</table>';
        $('#sub_feature_list').html(message);
        $('#second_level_feature_list').html('&nbsp;');
        $('#third_level_feature_list').html('&nbsp;');
        initialize_feature_tab_button(feature_modified,project_id,team_id,feature);
        $(".sub_feature_first_level").on('click',function(){
            $('#feature_control_panel').empty();
            $('.sub_feature_first_level').css({'background-color':'#fff'});
            $(this).css({'background-color':'#ccc'});
            $('.sub_feature_first_level').removeClass('selected');
            $(this).removeClass('selected');
            $('#feature_extended_div').empty();
            $('#feature_pagination_div').pagination('destroy');
            $('#feature_pagination_div').empty();
            var parent_name=$(this).attr('data-id');
            var child_name=$(this).text().trim().replace(/ /g,'_');
            var modified_name=parent_name+'.'+child_name;
            $.get('get_all_first_level_sub_feature',{
                'name':modified_name,
                'project_id':project_id,
                'team_id':team_id
            },function(data){
                var message='';
                message+='<table class="two-column-emphasis">';
                if(data['version_list'].length>0){
                    var second_level_sub_feature=data['version_list'];
                    for(var i=0;i<second_level_sub_feature.length;i++){
                        message+='<tr>';
                        message+='<td data-id="'+parent_name+'.'+second_level_sub_feature[i][0]+'" class="sub_feature_second_level">'+second_level_sub_feature[i][1].replace(/_/g,' ')+'</td>';
                        message+='</tr>';
                    }
                }
                else{
                    message+='<tr><td><b>No Sub Feature Found</b></td></tr>'
                }
                message+='</table>';
                $('#second_level_feature_list').html(message);
                $('#third_level_feature_list').html('&nbsp;');
                initialize_second_feature_tab_button(modified_name,project_id,team_id,child_name);
                $('.sub_feature_second_level').on('click',function(){
                    $('.sub_feature_second_level').css({'background-color':'#fff'});
                    $(this).css({'background-color':'#ccc'});
                    $('.sub_feature_second_level').removeClass('selected');
                    $(this).addClass('selected');
                    $('#feature_extended_div').empty();
                    $('#feature_pagination_div').pagination('destroy');
                    $('#feature_pagination_div').empty();
                    var parent_name=$(this).attr('data-id');
                    var child_name=$(this).text().trim().replace(/ /g,'_');
                    var modified_name=parent_name+'.'+child_name;
                    $.get('get_all_first_level_sub_feature',{
                        'name':modified_name,
                        'project_id':project_id,
                        'team_id':team_id
                    },function(data){
                        var message='';
                        message+='<table class="two-column-emphasis">';
                        if(data['version_list'].length>0){
                            var second_level_sub_feature=data['version_list'];
                            for(var i=0;i<second_level_sub_feature.length;i++){
                                message+='<tr>';
                                message+='<td data-id="'+parent_name+'.'+second_level_sub_feature[i][0]+'" class="sub_feature_third_level">'+second_level_sub_feature[i][1].replace(/_/g,' ')+'</td>';
                                message+='</tr>';
                            }
                        }
                        else{
                            message+='<tr><td><b>No Sub Feature Found</b></td></tr>'
                        }
                        message+='</table>';
                        $('#third_level_feature_list').html(message);
                        initialize_second_feature_tab_button(modified_name,project_id,team_id,child_name);
                        $('.sub_feature_third_level').on('click',function(){
                            $('.sub_feature_third_level').css({'background-color':'#fff'});
                            $(this).css({'background-color':'#ccc'});
                            $('.sub_feature_third_level').removeClass('selected');
                            $(this).addClass('selected');
                            $('#feature_extended_div').empty();
                            $('#feature_pagination_div').pagination('destroy');
                            $('#feature_pagination_div').empty();
                            var parent_name=$(this).attr('data-id');
                            var child_name=$(this).text().trim().replace(/ /g,'_');
                            var modified_name=parent_name+'.'+child_name;
                            initialize_third_feature_tab_button(modified_name,project_id,team_id,child_name);
                        });
                    });
                });
            });
        });
    });
}
function initialize_third_feature_tab_button(feature_id,project_id,team_id,feature){
    var message='';
    //message+='<input type="button" id="add_sub_feature" class="m-btn green" value="Add Sub Feature"/> ';
    message+='<input type="button" id="rename_feature" class="m-btn green" value="Rename Feature"/> ';
    message+='<input type="button" class="m-btn green" value="Usage" id="feature_usage"/> ';
    message+='<input type="button" class="m-btn red" id="delete_button" value="Delete"/> ';
    $('#feature_control_panel').html(message);
    $('#feature_usage').on('click',function(){
        get_feature_usage(feature_id,project_id,team_id,5,1);
    });$('#delete_button').on('click',function(){
        get_feature_usage(feature_id,project_id,team_id,5,1,true);
    });
    $('#rename_feature').on('click',function(){
        rename_feature(feature_id,project_id,team_id);
    });
}
function initialize_second_feature_tab_button(feature_id,project_id,team_id,feature){
    var message='';
    message+='<input type="button" id="add_sub_feature" class="m-btn green" value="Add Sub Feature"/> ';
    message+='<input type="button" id="rename_feature" class="m-btn green" value="Rename Feature"/> ';
    message+='<input type="button" class="m-btn green" value="Usage" id="feature_usage"/> ';
    message+='<input type="button" class="m-btn red" value="Delete" id="feature_delete"/> ';
    $('#feature_control_panel').html(message);

    $('#add_sub_feature').on('click',function(e){
        e.preventDefault();
        var parent_feature=feature_id.split('.');
        var show_parent_feature=parent_feature[parent_feature.length-1].replace(/_/g,' ');
        var message='';
        message+='<table>';
        message+='<tr><td><b>Parent Feature:</b></td><td>'+show_parent_feature+'</td></tr>';
        message+='<tr><td><b>Sub Feature:</b></td><td><input style="width: 100%" class="textbox" id="sub_feature"/></td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var sub_feature=$('#sub_feature').val().trim();
                if(sub_feature==''){
                    alertify.set({ delay: 300000 });
                    alertify.error("You can't give empty name");
                    return false;
                }
                if(sub_feature==''){
                    alertify.set({ delay: 300000 });
                    alertify.error("You can't give empty name");
                    return false;
                }
                if(sub_feature!=''){
                    if(sub_feature.indexOf('.')!=-1 || sub_feature.indexOf('_')!=-1){
                        alertify.set({ delay: 300000 });
                        alertify.error('You can\'t give "." or "_" in feature name',time_out);
                        return false;
                    }
                    else{
                        var total_input=feature_id+'.'+sub_feature;
                        var feature_id_temp=feature_id.split('.')[0];
                        $.get('add_new_feature',{
                            feature_path: total_input.trim(),
                            project_id:project_id,
                            team_id:team_id,
                            'type':'sub_feature'
                        },function(data){
                            if(data['message']){
                                alertify.set({ delay: 300000 });
                                alertify.success(data['log_message'],time_out);
                                get_features('',project_id,team_id,feature_id_temp);
                            }
                            else{
                                alertify.set({ delay: 300000 });
                                alertify.error(data['log_message'],time_out);
                                get_features('',project_id,team_id,feature_id_temp);
                            }
                        });
                    }
                }
                else{
                    return false;
                }
            }
            else{
                alertify.alert().close_all();
            }
        });
    });
    $('#feature_usage').on('click',function(){
        get_feature_usage(feature_id,project_id,team_id,5,1);
    });
    $('#feature_delete').on('click',function(){
        get_feature_usage(feature_id,project_id,team_id,5,1,true);
    });
    $('#rename_feature').on('click',function(){
        rename_feature(feature_id,project_id,team_id);
    });
}
function get_feature_usage(UserText,project_id,team_id,test_case_per_page,test_case_page_current,delete_tag){
    if(delete_tag===undefined){
        delete_tag=false;
    }
    $.get('FeatureUsageTestCase',{
        Query:UserText,
        project_id:project_id,
        team_id:team_id,
        test_case_per_page:test_case_per_page,
        test_case_page_current:test_case_page_current
    },function(data){
        if(delete_tag){
            var message='';
            if(data['Count']>0){
                message+=data['Count']+' Test Cases are linked.It can\'t be deleted.'
            }
            else{
                message+='You are about to delete <b>'+UserText.split(".")[UserText.split(".").length-1].replace(/_/g,' ').trim()+'</b>.Are you sure?';
            }
            alertify.confirm(message,function(e){
                if(e){
                    if(data['Count']>0){
                        alertify.alert().close_all();
                    }else{
                        delete_feature(UserText,project_id,team_id);
                    }
                }else{
                    alertify.alert().close_all();
                }
            });
        }else{
            form_table('feature_extended_div',data['Heading'],data['TableData'],data['Count'],'Test Cases');
            $('#feature_pagination_div').pagination({
                items:data['Count'],
                itemsOnPage:test_case_per_page,
                cssStyle: 'dark-theme',
                currentPage:test_case_page_current,
                displayedPages:2,
                edges:2,
                hrefTextPrefix:'#',
                onPageClick:function(PageNumber){
                    get_feature_usage(UserText,project_id,team_id,test_case_per_page,PageNumber);
                }
            });
        }
    });
}
function delete_feature(UserText,project_id,team_id){
    $.get('delete_feature',{
        'name':UserText,
        'project_id':project_id,
        'team_id':team_id
    },function(data){
        if(data['message']){
            window.location.reload(true);
        }
        else{
            window.location.reload(false);
        }
    });
}
function initialize_feature_tab_button(feature_id,project_id,team_id,feature){
    var message='';
    message+='<input type="button" id="add_sub_feature" class="m-btn green" value="Add Sub Feature"/> ';
    message+='<input type="button" id="rename_feature" class="m-btn green" value="Rename Feature"/> ';
    message+='<input type="button" class="m-btn green" value="Usage" id="feature_usage"/> ';
    message+='<input type="button" class="m-btn red" value="Delete" id="feature_delete"/> ';
    $('#feature_control_panel').html(message);

    $('#add_sub_feature').on('click',function(e){
        e.preventDefault();
        var parent_feature=feature_id.split('.');
        parent_feature=parent_feature[parent_feature.length-1].replace(/_/g,' ');
        var message='';

        message+='<table>';
        message+='<tr><td><b>Parent Feature:</b></td><td>'+parent_feature+'</td></tr>';
        message+='<tr><td><b>Sub Feature:</b></td><td><input style="width: 100%" class="textbox" id="sub_feature"/></td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var sub_feature=$('#sub_feature').val().trim();
                if(sub_feature==''){
                    alertify.set({ delay: 300000 });
                    alertify.error("You can't give empty name");
                    return false;
                }
                if(sub_feature!=''){
                    if(sub_feature.indexOf('.')!=-1 || sub_feature.indexOf("_")!=-1){
                        alertify.set({ delay: 300000 });
                        alertify.error('You can\'t give "." or "_" in feature name',time_out);
                        return false;
                    }
                    else{
                        var total_input=feature_id+'.'+sub_feature;
                        var feature_id_temp=feature_id.split('.')[0].trim();
                        $.get('add_new_feature',{
                            feature_path: total_input.trim(),
                            project_id:project_id,
                            team_id:team_id,
                            'type':'sub_feature'
                        },function(data){
                            if(data['message']){
                                alertify.set({ delay: 300000 });
                                alertify.success(data['log_message'],time_out);
                                get_features('',project_id,team_id,feature_id_temp);
                            }
                            else{
                                alertify.set({ delay: 300000 });
                                alertify.error(data['log_message'],time_out);
                                get_features('',project_id,team_id,feature_id_temp);
                            }
                        });
                    }
                }
                else{
                    return false;
                }
            }
            else{
                alertify.alert().close_all();
            }
        });
    });
    $('#feature_usage').on('click',function(e){
        get_feature_usage(feature_id,project_id,team_id,5,1);
    });
    $('#feature_delete').on('click',function(){
        get_feature_usage(feature_id,project_id,team_id,5,1,true);
    });
    $('#rename_feature').on('click',function(){
        rename_feature(feature_id,project_id,team_id);
    });
}
function rename_feature(feature_full_path,project_id,team_id){
    //get the last part
    feature_full_path=feature_full_path.replace(/ /g,'_');
    var value_name=feature_full_path.split(".")[feature_full_path.split(".").length-1].replace(/_/g,' ');
    var message='';
    message+='<table width="100%;">';
    message+='<tr><td><b>Old Name:</b></td><td>'+value_name+'</td></tr>';
    message+='<tr><td><b>New Name:</b></td><td><input id="new_feature" style="width: 100%;" class="textbox"/></td></tr>'
    message+='</table>';
    alertify.confirm(message,function(e){
        if(e){
            var new_feature_name=$("#new_feature").val().trim();
            if(new_feature_name==''){
                alertify.set({ delay: 300000 });
                alertify.error("You can't give empty name");
                return false;
            }
            if(new_feature_name.indexOf('.')!=-1 || new_feature_name.indexOf('_')!=-1){
                alertify.set({ delay: 300000 });
                alertify.error("You can not give '.' or '_' in feature name",time_out);
                return false;
            }
            else{
                //form the new name
                value_name=value_name.replace(/ /g,'_');
                var new_content=removeA(feature_full_path.split("."),value_name);
                new_content.push(new_feature_name.replace(/ /g,'_'));
                $.get('rename_feature',{
                    old_feature_name:feature_full_path,
                    new_feature_name:new_content.join("."),
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
                        alertify.error(data['log_message'],1500);
                        alertify.alert().close_all();
                    }
                });
            }
        }else{
            alertify.alert().close_all();
        }
    });
}
function removeA(arr) {
    var what, a = arguments, L = a.length, ax;
    while (L > 1 && arr.length) {
        what = a[--L];
        while ((ax= arr.indexOf(what)) !== -1) {
            arr.splice(ax, 1);
        }
    }
    return arr;
}
function PerformSearch(UserText,project_id,team_id,test_case_per_page,test_case_page_current,usage){
    if(usage==undefined){
        usage=true;
    }
    $.get('TableDataTestCasesOtherPages',{
        Query: UserText,
        test_status_request:true,
        project_id:project_id,
        team_id:team_id,
        total_time:'true',
        test_case_per_page:test_case_per_page,
        test_case_page_current:test_case_page_current
    },function(data){
        if(usage){
            form_table('extended_div',data['Heading'],data['TableData'],data['Count'],'Test Cases');
            $('#pagination_div').pagination({
                items:data['Count'],
                itemsOnPage:test_case_per_page,
                cssStyle: 'dark-theme',
                currentPage:test_case_page_current,
                displayedPages:2,
                edges:2,
                hrefTextPrefix:'#',
                onPageClick:function(PageNumber){
                    PerformSearch(UserText,project_id,team_id,test_case_per_page,PageNumber);
                }
            });
        }else{
            var message='';
            if(data['Count']>0){
                message+=data['Count']+' Test Cases are linked.It can\'t be deleted.'
            }
            else{
                message+='You are about to delete <b>'+UserText.split(":")[0].trim()+'</b>.Are you sure?';
            }
            alertify.confirm(message,function(e){
                if(e){
                    if(data['Count']>0){
                        alertify.alert().close_all();
                    }else{
                        delete_dependency_name(UserText.split(":")[0],project_id,team_id);
                    }
                }else{
                    alertify.alert().close_all();
                }
            });
        }
    });
}
var colors = {
    'pass' : '#65bd10',
    'fail' : '#fd0006',
    'block' : '#ff9e00',
    'submitted' : '#808080',
    'in-progress':'#0000ff',
    'skipped':'#cccccc',
    'dev': '#aaaaaa',
    'ready': '#65bd10'
};

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
        message+='</tr>';
    }
    message+='</table>';
    $('#'+divname).html(message);
}