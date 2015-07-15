/**
 * Created by Raju on 7/11/2015.
 */
function get_all_data(project_id,team_id){
    $.get('get_all_data_dependency_page',{
        project_id:project_id,
        team_id:team_id
    },function(data){
        $('#name_list').empty();
        $('#version_list').empty();
        $('#bread_crumb').empty();
        $('#control_panel').empty();
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
    });
}
function link_dependency(dependency,project_id,team_id){
    $.get('link_dependency',{
        value:dependency,
        project_id:project_id,
        team_id:team_id
    },function(data){
        if(data['message']){
            alertify.set({ delay: 300000 });
            alertify.success(data['log_message']);
            get_all_data(project_id,team_id);
        }
    })
}
function get_dependency_under_name(value,project_id,team_id,value_name){
    $.get('get_all_name_under_dependency',{
        'value':value,
        'project_id':project_id,
        'team_id':team_id
    },function(data){
        var dependency_list=data['dependency_list'];
        if(data['default_list'].length>0 && data['default_list'][0]!=null){
            var default_list=data['default_list'][0].split(',');
        }
        else{
            var default_list=[];
        }
        if(dependency_list.length>0){
            var message='';
            message+='<table class="two-column-emphasis">';
            for(var i=0;i<dependency_list.length;i++){
                message+='<tr>';
                message+='<td data-id="'+dependency_list[i][0]+'" class="dependency_name">'+dependency_list[i][1]+'</td>';
                if(default_list.indexOf(dependency_list[i][0].toString())!=-1){
                    message+='<td><a class="default_tip notification-indicator tooltipped downwards" data-gotokey="n"><span class="mail-status filled"></span></a></td>';
                }
                else{
                    message+='<td><a class="default_tip notification-indicator tooltipped downwards" data-gotokey="n"><span class="mail-status unfilled"></span></a></td>';
                }
                message+='</tr>';
            }
            message+='</table>';
            $('#version_list').empty();
            $('#name_list').html(message);
            $('.default_tip').on('click',function(){
                var name_value=$(this).parent().parent().find('td:first-child').attr('data-id');
                var name=$(this).parent().parent().find('td:first-child').text().trim();
                if($(this).find('span:eq(0)').hasClass('unfilled')){
                    var tag='make_default';
                    var message="Do you want to make <b>"+name+"</b> default?"
                    alertify.confirm(message,function(e){
                        if(e){
                            $.get('make_default_name',{
                                tag:tag,
                                dependency:value,
                                name:name_value,
                                project_id:project_id,
                                team_id:team_id
                            },function(data){
                                if(data['message']){
                                    alertify.set({ delay: 300000 });
                                    alertify.success(data['log_message'],time_out);
                                    get_dependency_under_name(value,project_id,team_id,value_name);
                                }else{
                                    alertify.set({ delay: 300000 });
                                    alertify.error(data['log_message'],time_out);
                                    get_dependency_under_name(value,project_id,team_id,value_name);
                                }
                            });
                        }else{
                            alertify.alert().close_all();
                        }
                    });
                }
                else{
                    var tag='remove_default';
                    var message="Do you want to remove <b>"+name+"</b> from default?"
                    alertify.confirm(message,function(e){
                        if(e){
                            $.get('make_default_name',{
                                tag:tag,
                                dependency:value,
                                name:name_value,
                                project_id:project_id,
                                team_id:team_id
                            },function(data){
                                if(data['message']){
                                    alertify.set({ delay: 300000 });
                                    alertify.success(data['log_message'],time_out);
                                    get_dependency_under_name(value,project_id,team_id,value_name);
                                }else{
                                    alertify.set({ delay: 300000 });
                                    alertify.error(data['log_message'],time_out);
                                    get_dependency_under_name(value,project_id,team_id,value_name);
                                }
                            });
                        }else{
                            alertify.alert().close_all();
                        }
                    });
                }
            })
            var message='';
            message+='<input type="button" id="add_name" class="m-btn green" value="Add Name"/> ';
            message+='<input type="button" id="rename_dependency" class="m-btn green" value="Rename"/> ';
            message+='<input type="button" class="m-btn green" value="Usage" id="usage_dependency"/> ';
            message+='<input type="button" class="m-btn red" value="Delete" id="delete_dependency"/> ';
            $('#control_panel').html(message);
            initialize_button(value,project_id,team_id,value_name);
            $('#bread_crumb').html('<a href="#" class="bread_crumb_element">'+value_name+'</a>');
            $('.dependency_name').on('click',function(){
                $('.dependency_name').css({'background-color':"#fff"});
                $(this).css({'background-color':'#ccc'});
                $('#extended_div').empty();
                $('#pagination_div').pagination('destroy');
                $('#pagination_div').empty();
                get_all_version($(this).attr('data-id'),$(this).text(),value_name,project_id,team_id);
            });
        }
        else{
            $('#version_list').empty();
            $('#name_list').html('<p><b style="font-size: ">No Name Found</b></p>');
            $('#bread_crumb').html('<a href="#" class="bread_crumb_element">'+value_name+'</a>');
            var message='';
            message+='<input type="button" id="add_name" class="m-btn green" value="Add Name"/> ';
            message+='<input type="button" id="rename_dependency" class="m-btn green" value="Rename"/> ';
            message+='<input type="button" class="m-btn green" value="Usage" id="usage_dependency"/> ';
            message+='<input type="button" class="m-btn red" value="Delete" id="delete_dependency"/> ';
            $('#control_panel').html(message);
            initialize_button(value,project_id,team_id,value_name);
        }
    });
}
function get_all_version(value,text,parent_name,project_id,team_id){
    $.get('get_all_version_bit',{
        value:value
    },function(data){
        console.log(data);
        var version_list=data['version_list'];
        if(version_list.length>0){
            var message='';
            message+='<table class="two-column-emphasis">'
            for(var i=0;i<version_list.length;i++){
                message+='<tr>';
                message+='<td>'+version_list[i][0]+'</td>';
                var version=version_list[i][1].split(',');
                message+='<td><table>';
                for(var j=0;j<version.length;j++){
                    message+='<tr><td class="dependency_version" style="cursor:pointer">'+version[j]+'</td></tr>';
                }

                message+='</table></td>'
                message+='</tr>';
            }
            message+='</table>';
            $('#version_list').html(message);
            $('#bread_crumb').html('<a href="#">'+parent_name+'</a> > <a href="#">'+text+'</a> ');
            initialize_second_level(value,text,parent_name,project_id,team_id);
            $('.dependency_version').on('click',function(){
                $('.dependency_version').css({'background-color':'#fff'});
                $(this).css({'background-color':'#ccc'});
                intialize_third_level(value,text,parent_name,project_id,team_id,$(this).text(),$(this).parent().parent().parent().parent().prev().text().split(" ")[0]);
            });
        }
        else{
            $('#version_list').html('<p style="font-size: 110%;margin-left: 1%;"><b>No Version Present</b></p>');
            $('#bread_crumb').html('<a href="#">'+parent_name+'</a> > <a href="#">'+text+'</a> ');
            initialize_second_level(value,text,parent_name,project_id,team_id);
        }

    })
}
function intialize_third_level(value,text,parent_name,project_id,team_id,version_id,bit){
    var message='';
    //message+='<input type="button" id="add_version" class="m-btn green" value="Add Version"/> ';
    message+='<input type="button" id="rename_version" class="m-btn green" value="Rename"/> ';
    message+='<input type="button" id="delete_version" class="m-btn red" value="Delete"/> ';
    $('#control_panel').html(message);

    $('#delete_version').on('click',function(){
        var message='';
        message+='Do you want to delete <b>'+text+'</b> version <b>'+version_id+'</b> of <b>'+bit+'</b> bit?';
        alertify.confirm(message,function(e){
            if(e){
                $.get('delete_version',{
                    dependency:value,
                    version:version_id,
                    bit: bit
                },function(data){
                    if(data['message']){
                        alertify.set({ delay: 300000 });
                        alertify.success(data['log_message'],time_out);
                        get_all_version(value,text,parent_name,project_id,team_id);
                    }
                    else{
                        alertify.set({ delay: 300000 });
                        alertify.error(data['log_message'],time_out);
                        get_all_version(value,text,parent_name,project_id,team_id);
                    }
                });
            }
            else{

            }
        });
    });

    $('#rename_version').on('click',function(){
        var message='';
        message+='<table width="100%;">';
        message+='<tr><td><b>Old Version:</b></td><td>'+version_id+'</td></tr>';
        message+='<tr><td><b>New Version:</b></td><td><input id="rename_version_dep" style="width: 100%;" class="textbox"/></td></tr>'
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var new_version=$('#rename_version_dep').val().trim();
                if(new_version!=''){
                    $.get('rename_version',{
                        old_name:version_id,
                        dependency:value,
                        new_name:new_version,
                        bit:bit
                    },function(data){
                        if(data['message']){
                            alertify.set({ delay: 300000 });
                            alertify.success(data['log_message'],time_out);
                            get_all_version(value,text,parent_name,project_id,team_id);
                        }
                        else{
                            alertify.set({ delay: 300000 });
                            alertify.error(data['log_message'],time_out);
                            get_all_version(value,text,parent_name,project_id,team_id);
                        }
                    })
                }
                else{
                    return false;
                }
            }
            else{
                alertify.alert().close_all();
            }
        })
    });
}

function initialize_second_level(value,text,parent_name,project_id,team_id){
    var message='';
    message+='<input type="button" id="add_version" class="m-btn green" value="Add Version"/> ';
    message+='<input type="button" id="rename_name" class="m-btn green" value="Rename"/> ';
    message+='<input type="button" class="m-btn green" value="Usage" id="usage_version"/> ';
    message+='<input type="button" class="m-btn red" value="Delete" id="delete_name"/>';
    $('#control_panel').html(message);
    $('#add_version').on('click',function(){
        var message='';
        message+='<table>';
        message+='<tr><td align="right"><b>'+parent_name+' Name:</b></td><td align="left">'+text+'</td></tr>';
        message+='<tr><td align="right"><b>Bit:</b></td><td align="left"><select id="bit"><option value="32">32 Bit</option><option value="64">64 Bit</option></select></td></tr>';
        message+='<tr><td align="right"><b>Version:</b></td><td align="left"><input id="version_name" class="textbox" style="width: 100%;"/></td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var version=$('#version_name').val().trim();
                var bit=$('#bit option:selected').val().trim();
                if(version!=''){
                    add_new_version(value,text,parent_name,version,bit);
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
    $('#rename_name').on('click',function(){
        var message='';
        message+='<table width="100%;">';
        message+='<tr><td><b>Old Name:</b></td><td>'+text+'</td></tr>';
        message+='<tr><td><b>New Name:</b></td><td><input id="rename_dep_name" style="width: 100%;" class="textbox"/></td></tr>'
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var new_name=$('#rename_dep_name').val().trim();

                var main_dependency=$('.dependency.selected').attr('data-id');
                var main_dep_value=$('.dependency.selected').text().trim();
                if(new_name!=''){
                    $.get('rename_name',{
                        'old_name':text,
                        'new_name':new_name,
                        'main_dependency':main_dep_value
                    },function(data){
                        if(data['message']){
                            alertify.set({ delay: 300000 });
                            alertify.success(data['log_message'],time_out);
                            get_dependency_under_name(main_dependency,project_id,team_id,main_dep_value);
                        }
                        else{
                            alertify.set({ delay: 300000 });
                            alertify.error(data['log_message'],time_out);
                            get_dependency_under_name(main_dependency,project_id,team_id,main_dep_value);
                        }
                    });
                }
                else{
                    return false;
                }
            }else{
                alertify.alert().close_all();
            }

        });
    });
    $('#usage_version').on('click',function(){
        var UserText=(text+":").trim();
        var UserText=(text+":").trim();
        var test_case_page_current=1;
        PerformSearch(UserText,project_id,team_id,test_case_per_page,test_case_page_current);
    });
    $('#delete_name').on('click',function(){
        var UserText=(text+":").trim();
        var test_case_page_current=1;
        PerformSearch(UserText,project_id,team_id,test_case_per_page,test_case_page_current,false);
    });
}

function add_new_version(value,text,parent_name,version,bit){
    $.get('add_new_version',{
        value:value,
        bit:bit,
        version:version
    },function(data){
        if(data['message']){
            alertify.set({ delay: 300000 });
            alertify.success(data['log_message'],time_out);
            get_all_version(value,text,parent_name);
        }
        else{
            alertify.set({ delay: 300000 });
            alertify.error(data['log_message'],time_out);
            get_all_version(value,text,parent_name);
        }
    });
}
function initialize_button(value,project_id,team_id,value_name){
    $('#add_name').on('click',function(){
        var message='';
        message+='<table width="100%;">';
        message+='<tr><td><b style="">'+value_name+' Name</b></td></tr><tr><td><input id="new_name" style="width: 100%;" class="textbox" type="text" placeholder="Enter the Name"/></td></tr>';
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var new_name=$('#new_name').val().trim();
                if(new_name!=''){
                    add_new_name_under_dependency(value,project_id,team_id,value_name,new_name);
                }
                else{
                    alertify.error("Name can't be empty",300000);
                    return false;
                }
            }
            else{
                alertify.alert().close_all();
            }
        });
    });
    $('#rename_dependency').on('click',function(){
        var message='';
        message+='<table width="100%;">';
        message+='<tr><td><b>Old Name:</b></td><td>'+value_name+'</td></tr>';
        message+='<tr><td><b>New Name:</b></td><td><input id="rename_dep" style="width: 100%;" class="textbox"/></td></tr>'
        message+='</table>';
        alertify.confirm(message,function(e){
            if(e){
                var new_dep=$('#rename_dep').val().trim();
                if(new_dep!=''){
                    rename_dependency(value,project_id,team_id,value_name,new_dep);
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
    $('#usage_dependency').on('click',function(){
        var UserText=(value_name+":").trim();
        var pageNumber=1;
        performDependencySearches(UserText,project_id,team_id,test_case_per_page,pageNumber);
    });
    $('#delete_dependency').on('click',function(){
        var UserText=(value_name+":").trim();
        var pageNumber=1;
        performDependencySearches(UserText,project_id,team_id,test_case_per_page,pageNumber,false);
    })
}
function rename_dependency(value,project_id,team_id,value_name,new_dep){
    $.get('rename_dependency',{
        old_name:value_name,
        new_name:new_dep,
        project_id:project_id
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
function delete_dependency(name,project_id,team_id){
    $.get('delete_dependency',{
        'name':name,
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
function delete_dependency_name(name,project_id,team_id){
    $.get('delete_dependency_name',{
        'name':name,
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

function add_new_name_under_dependency(value,project_id,team_id,value_name,new_name){
    $.get('add_new_name_dependency',{
        new_name:new_name,
        new_value:value
    },function(data){
        if(data['message']){
            alertify.set({ delay: 300000 });
            alertify.success(data['log_message'],time_out);
            get_dependency_under_name(value,project_id,team_id,value_name);
        }
    });
}
function performDependencySearches(UserText,project_id,team_id,test_case_per_page,test_case_page_current,delete_tag){
    if(delete_tag===undefined){
        delete_tag=true;
    }
    $.get('TableDataDependencyTestCases',{
        Query: UserText,
        test_status_request:true,
        project_id:project_id,
        team_id:team_id,
        test_case_per_page:test_case_per_page,
        test_case_page_current:test_case_page_current
    },function(data){
        if(delete_tag){
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
                    performDependencySearches(UserText,project_id,team_id,test_case_per_page,PageNumber);
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
                        delete_dependency(UserText.split(":")[0],project_id,team_id);
                    }
                }else{
                    alertify.alert().close_all();
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
var time_out=300000;
var name_field_error="Name field can't be empty";
var dep_value="";
var dep_name="";
var test_case_per_page=5;

$(document).ready(function(){
    var project_id= $.session.get('project_id');
    var team_id= $.session.get('default_team_identity');
    get_all_data(project_id,team_id);
    $('#create_dependency').on('click',function(){
        var message='';
        message+='<table>';
        message+='<tr><td><b style="font-size: 125%;">Dependency Name</b> </td></tr>';
        message+='<tr><td><input type="text" class="textbox" id="new_dependency"></td></tr>';
        message+='</table>';
        //alertify.alert().close_all();
        alertify.confirm(message,function(e){
            if(e){
                if($('#new_dependency').val().trim()!=''){
                    $.get('add_new_dependency',{
                        dependency_name:$('#new_dependency').val().trim(),
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
                }else{
                    alertify.set({ delay: 300000 });
                    alertify.error("Dependency can't be empty",time_out);
                    get_all_data(project_id,team_id);
                }
            }
            else{
                alertify.alert().close_all();
            }
        });

    });
});