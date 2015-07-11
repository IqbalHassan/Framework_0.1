/**
 * Created by Raju on 7/11/2015.
 */
function driver_control_panel(driver_id,driver_text,project_id,team_id){
    var message='';
    message+='<input type="button" id="rename_driver" class="m-btn green" value="Rename Driver"/> ';
    message+='<input type="button" class="m-btn green" value="Usage" id="usage_driver"/> ';
    message+='<input type="button" class="m-btn red" value="Delete" id="delete_driver"/> ';
    $('#driver_control_panel').html(message);
    $("#rename_driver").on('click',function(){
        var message='';
        message+='<table width="100%;">';
        message+='<tr><td><b>Old Name:</b></td><td>'+driver_text.replace(/_/g,' ')+'</td></tr>';
        message+='<tr><td><b>New Name:</b></td><td><input id="new_name" style="width: 100%;" class="textbox"/></td></tr>';
        message+='</table>';
        alertify.confirm(message,function(){
            var new_name=$("#new_name").val().trim();
            if(new_name!=''){
                rename_driver(driver_id,driver_text,new_name,project_id,team_id)
            }else{
                alertify.set({ delay: 300000 });
                alertify.error("You can't give empty name",time_out);
                alertify.alert().close_all();
                return false;
            }
        });
    });
    $("#usage_driver").on('click',function(){
        get_driver_usage(driver_text,project_id,team_id,5,1);
    });
    $('#delete_driver').on('click',function(){
        get_driver_usage(driver_text,project_id,team_id,5,1,true);
    });
}
function rename_driver(driver_id,driver_text,new_name,project_id,team_id){
    $.get('rename_driver',{
        driver_id:driver_id,
        old_name:driver_text,
        new_name:new_name,
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
function get_driver_usage(UserText,project_id,team_id,test_case_per_page,test_case_page_current,delete_tag){
    if(delete_tag===undefined){
        delete_tag=false;
    }
    $.get('DriverUsageTestCase',{
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
                message+='You are about to delete <b>'+UserText.replace(/_/g,' ').trim()+'</b>.Are you sure?';
            }
            alertify.confirm(message,function(e){
                if(e){
                    if(data['Count']>0){
                        alertify.alert().close_all();
                    }else{
                        delete_driver(UserText,project_id,team_id);
                    }
                }else{
                    alertify.alert().close_all();
                }
            });
        }else{
            form_table('driver_extended_div',data['Heading'],data['TableData'],data['Count'],'Test Cases');
            $('#driver_pagination_div').pagination({
                items:data['Count'],
                itemsOnPage:test_case_per_page,
                cssStyle: 'dark-theme',
                currentPage:test_case_page_current,
                displayedPages:2,
                edges:2,
                hrefTextPrefix:'#',
                onPageClick:function(PageNumber){
                    get_driver_usage(UserText,project_id,team_id,test_case_per_page,PageNumber);
                }
            });
        }
    });
}
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
function delete_driver(UserText,project_id,team_id){
    $.get('delete_driver',{
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

function get_all_data(project_id,team_id){
    $.get('get_all_data_dependency_page',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        $('#driver_control_panel').empty();
        $('#driver_extended_div').empty();
        $('#driver_pagination_div').empty();

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
    });
}
var time_out=300000;

$(document).ready(function(){
    $('#create_driver').on('click',function(){
        var message='';
        message+='<table>';
        message+='<tr><td><b>Driver Name:</b></td><td><input style="width:100%" class="textbox" placeholder="Driver Name" id="new_driver"/> </td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var driver_name=$('#new_driver').val().trim();
                $.get('add_new_driver',{
                    'name':driver_name.replace(/ /g,'_'),
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
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    get_all_data(project_id,team_id);
});
